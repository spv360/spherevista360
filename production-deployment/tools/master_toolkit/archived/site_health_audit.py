import argparse
import csv
import re
import sys
import time
from collections import defaultdict, Counter, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

# ---- Config defaults ----
DEFAULT_TIMEOUT = 12
HEADERS = {"User-Agent": "SphereVista360-SiteAuditor/1.0 (+https://example.com)"}

# ---- Data models ----
@dataclass
class PageInfo:
    url: str
    status: int = 0
    title: str = ""
    meta_desc: str = ""
    canonical: str = ""
    h1: str = ""
    internal_links: Set[str] = field(default_factory=set)
    external_links: Set[str] = field(default_factory=set)
    images: List[Tuple[str, str]] = field(default_factory=list)  # (src, alt)
    mixed_content: bool = False
    # Enhanced post validation fields
    word_count: int = 0
    headings: List[str] = field(default_factory=list)  # H2, H3, etc.
    has_featured_image: bool = False
    publish_date: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    content_quality_score: float = 0.0
    readability_score: str = ""
    social_meta: Dict[str, str] = field(default_factory=dict)
    schema_markup: bool = False

# ---- Helpers ----
def same_host(u1: str, u2: str) -> bool:
    return urlparse(u1).netloc.lower() == urlparse(u2).netloc.lower()

def normalize_link(base: str, href: str) -> str:
    if not href:
        return ""
    href = href.strip()
    if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
        return ""
    absu = urljoin(base, href)
    absu, _ = urldefrag(absu)  # drop #fragments
    return absu

def is_http(u: str) -> bool:
    return urlparse(u).scheme in ("http", "https")

def get(session: requests.Session, url: str):
    try:
        r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        return r
    except requests.RequestException:
        return None

def head_or_get_status(session: requests.Session, url: str) -> Tuple[int, str]:
    try:
        r = session.head(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        if r is not None and r.status_code >= 200:
            return r.status_code, r.url
    except requests.RequestException:
        pass
    try:
        r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        if r is None:
            return 0, url
        return r.status_code, r.url
    except requests.RequestException:
        return 0, url

def extract_seo(soup: BeautifulSoup) -> Tuple[str, str, str, str]:
    title = (soup.title.string.strip() if soup.title and soup.title.string else "")
    md_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = (md_tag["content"].strip() if md_tag and md_tag.has_attr("content") else "")
    can_tag = soup.find("link", rel=lambda v: v and "canonical" in v)
    canonical = (can_tag.get("href", "").strip() if can_tag else "")
    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(strip=True) if h1_tag else ""
    return title, meta_desc, canonical, h1

def calculate_content_quality_score(soup: BeautifulSoup, word_count: int, images: List, headings: List) -> float:
    """Calculate a content quality score based on various factors."""
    score = 0.0
    
    # Word count scoring (ideal range: 800-2500 words)
    if 800 <= word_count <= 2500:
        score += 25
    elif 500 <= word_count < 800:
        score += 15
    elif word_count > 2500:
        score += 20
    elif word_count < 300:
        score += 0
    else:
        score += 10
    
    # Image scoring
    if len(images) >= 3:
        score += 20
    elif len(images) >= 1:
        score += 15
    else:
        score += 0
    
    # Image alt text scoring
    images_with_alt = sum(1 for _, alt in images if alt.strip())
    if images and images_with_alt == len(images):
        score += 10
    elif images and images_with_alt > 0:
        score += 5
    
    # Heading structure scoring
    if len(headings) >= 3:
        score += 15
    elif len(headings) >= 1:
        score += 10
    else:
        score += 0
    
    # Content structure scoring
    paragraphs = soup.find_all('p')
    if len(paragraphs) >= 5:
        score += 10
    elif len(paragraphs) >= 3:
        score += 5
    
    # Lists and structured content
    lists = soup.find_all(['ul', 'ol'])
    if len(lists) >= 2:
        score += 10
    elif len(lists) >= 1:
        score += 5
    
    # Internal links scoring
    internal_link_count = len(soup.find_all('a', href=lambda href: href and 'spherevista360.com' in href))
    if internal_link_count >= 3:
        score += 10
    elif internal_link_count >= 1:
        score += 5
    
    return min(score, 100.0)  # Cap at 100

def extract_post_metadata(soup: BeautifulSoup) -> Tuple[Optional[str], List[str], Dict[str, str], bool]:
    """Extract publish date, categories, social meta, and schema markup."""
    publish_date = None
    categories = []
    social_meta = {}
    schema_markup = False
    
    # Try to find publish date in various places
    date_selectors = [
        'time[datetime]',
        '[data-testid="publish-date"]',
        '.entry-date',
        '.post-date',
        '.published',
        'meta[property="article:published_time"]'
    ]
    
    for selector in date_selectors:
        element = soup.select_one(selector)
        if element:
            if element.name == 'meta':
                publish_date = element.get('content', '')
            else:
                publish_date = element.get('datetime') or element.get_text(strip=True)
            if publish_date:
                break
    
    # Extract categories
    category_selectors = [
        '.entry-categories a',
        '.post-categories a', 
        '.category a',
        '[rel="category tag"]',
        'meta[property="article:section"]'
    ]
    
    for selector in category_selectors:
        elements = soup.select(selector)
        for element in elements:
            if element.name == 'meta':
                categories.append(element.get('content', ''))
            else:
                categories.append(element.get_text(strip=True))
    
    # Social meta tags
    social_tags = {
        'og:title': soup.find('meta', attrs={'property': 'og:title'}),
        'og:description': soup.find('meta', attrs={'property': 'og:description'}),
        'og:image': soup.find('meta', attrs={'property': 'og:image'}),
        'twitter:title': soup.find('meta', attrs={'name': 'twitter:title'}),
        'twitter:description': soup.find('meta', attrs={'name': 'twitter:description'}),
        'twitter:image': soup.find('meta', attrs={'name': 'twitter:image'}),
    }
    
    for key, tag in social_tags.items():
        if tag and tag.get('content'):
            social_meta[key] = tag.get('content')
    
    # Check for schema markup
    schema_scripts = soup.find_all('script', type='application/ld+json')
    schema_markup = len(schema_scripts) > 0
    
    return publish_date, categories, social_meta, schema_markup

def calculate_readability_score(text: str) -> str:
    """Simple readability assessment based on sentence and word length."""
    if not text:
        return "Unknown"
    
    sentences = re.split(r'[.!?]+', text)
    words = text.split()
    
    if not sentences or not words:
        return "Unknown"
    
    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(word) for word in words) / len(words)
    
    # Simple scoring
    if avg_sentence_length < 15 and avg_word_length < 5:
        return "Easy"
    elif avg_sentence_length < 20 and avg_word_length < 6:
        return "Medium"
    else:
        return "Hard"

def find_links_and_images(base_url: str, soup: BeautifulSoup) -> Tuple[Set[str], Set[str], List[Tuple[str, str]], bool]:
    internal, external = set(), set()
    mixed = False
    base_is_https = base_url.startswith("https://")

    # links
    for a in soup.find_all("a"):
        href = normalize_link(base_url, a.get("href"))
        if not href or not is_http(href):
            continue
        if same_host(base_url, href):
            internal.add(href)
        else:
            external.add(href)

    # images
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        src = normalize_link(base_url, src)
        alt = img.get("alt") or ""
        if src:
            images.append((src, alt))
            if base_is_https and src.startswith("http://"):
                mixed = True

    # CSS/JS mixed content quick check
    for tag, attr in (("link", "href"), ("script", "src")):
        for el in soup.find_all(tag):
            v = el.get(attr) or ""
            v = normalize_link(base_url, v)
            if not v:
                continue
            if base_is_https and v.startswith("http://"):
                mixed = True

    return internal, external, images, mixed

def extract_content_analysis(soup: BeautifulSoup) -> Tuple[int, List[str], bool]:
    """Extract word count, headings, and check for featured image."""
    # Word count from main content
    content_selectors = [
        'article', 
        '.entry-content', 
        '.post-content', 
        '.content',
        'main',
        '[role="main"]'
    ]
    
    content_text = ""
    for selector in content_selectors:
        content_area = soup.select_one(selector)
        if content_area:
            content_text = content_area.get_text()
            break
    
    if not content_text:
        # Fallback to body text, excluding nav and footer
        for elem in soup(['nav', 'footer', 'header', 'aside']):
            elem.decompose()
        content_text = soup.get_text()
    
    words = content_text.split()
    word_count = len(words)
    
    # Extract headings
    headings = []
    for heading in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
        headings.append(heading.get_text(strip=True))
    
    # Check for featured image
    featured_image_selectors = [
        '.featured-image img',
        '.post-thumbnail img',
        '.entry-image img',
        'meta[property="og:image"]',
        '.wp-post-image'
    ]
    
    has_featured_image = False
    for selector in featured_image_selectors:
        if soup.select_one(selector):
            has_featured_image = True
            break
    
    return word_count, headings, has_featured_image

# ---- Crawler ----
def crawl(start_url: str, max_pages: int, same_domain_only: bool) -> Dict[str, PageInfo]:
    session = requests.Session()
    visited: Dict[str, PageInfo] = {}
    queue = deque([start_url])
    root = start_url

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue

        r = get(session, url)
        status = r.status_code if r is not None else 0
        pi = PageInfo(url=url, status=status)

        if r and r.headers.get("content-type", "").lower().startswith("text/html"):
            soup = BeautifulSoup(r.text, "html.parser")
            title, meta_desc, canonical, h1 = extract_seo(soup)
            pi.title, pi.meta_desc, pi.canonical, pi.h1 = title, meta_desc, canonical, h1

            internal, external, images, mixed = find_links_and_images(url, soup)
            pi.internal_links, pi.external_links, pi.images, pi.mixed_content = internal, external, images, mixed

            # Enhanced content analysis
            word_count, headings, has_featured_image = extract_content_analysis(soup)
            pi.word_count, pi.headings, pi.has_featured_image = word_count, headings, has_featured_image
            
            # Extract post metadata
            publish_date, categories, social_meta, schema_markup = extract_post_metadata(soup)
            pi.publish_date, pi.categories, pi.social_meta, pi.schema_markup = publish_date, categories, social_meta, schema_markup
            
            # Calculate content quality score
            pi.content_quality_score = calculate_content_quality_score(soup, word_count, images, headings)
            
            # Calculate readability
            content_text = soup.get_text()
            pi.readability_score = calculate_readability_score(content_text)

            # queue internal links
            for link in internal:
                if same_domain_only and not same_host(root, link):
                    continue
                if link not in visited and len(visited) + len(queue) < max_pages:
                    queue.append(link)

        visited[url] = pi

    return visited

# ---- Link & image status checks ----
def check_urls_status(urls: Set[str], max_workers: int = 16) -> Dict[str, Tuple[int, str]]:
    results: Dict[str, Tuple[int, str]] = {}
    session = requests.Session()
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        future_to_url = {ex.submit(head_or_get_status, session, u): u for u in urls}
        for fut in as_completed(future_to_url):
            u = future_to_url[fut]
            try:
                code, final_url = fut.result()
            except Exception:
                code, final_url = 0, u
            results[u] = (code, final_url)
    return results

# ---- Reporting ----
def write_csv(path: str, rows: List[Dict], fieldnames: List[str]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def generate_reports(data: Dict[str, PageInfo], start_url: str):
    pages = []
    links = []
    images = []
    issues = []

    # Collect global sets for status checks & inbound links map
    all_links: Set[str] = set()
    all_images: Set[str] = set()
    inbound: Dict[str, Set[str]] = defaultdict(set)

    # Track recent posts (last 30 days) and posts without images
    recent_cutoff = datetime.now() - timedelta(days=30)
    recent_posts_without_images = []
    low_quality_posts = []
    posts_without_featured_images = []

    for url, pi in data.items():
        # Enhanced pages data
        pages.append({
            "url": url,
            "status": pi.status,
            "title": pi.title,
            "title_length": len(pi.title),
            "meta_desc": pi.meta_desc,
            "meta_desc_len": len(pi.meta_desc),
            "canonical": pi.canonical,
            "h1": pi.h1,
            "word_count": pi.word_count,
            "headings_count": len(pi.headings),
            "has_featured_image": "yes" if pi.has_featured_image else "no",
            "internal_links": len(pi.internal_links),
            "external_links": len(pi.external_links),
            "images": len(pi.images),
            "images_with_alt": sum(1 for _, alt in pi.images if alt.strip()),
            "mixed_content": "yes" if pi.mixed_content else "no",
            "publish_date": pi.publish_date or "",
            "categories": ", ".join(pi.categories),
            "content_quality_score": round(pi.content_quality_score, 1),
            "readability_score": pi.readability_score,
            "has_og_image": "yes" if pi.social_meta.get('og:image') else "no",
            "has_schema_markup": "yes" if pi.schema_markup else "no",
        })
        
        # Check for recent posts without images
        if pi.publish_date:
            try:
                # Try to parse the date
                pub_date = None
                for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"]:
                    try:
                        pub_date = datetime.strptime(pi.publish_date[:19], fmt[:len(pi.publish_date[:19])])
                        break
                    except ValueError:
                        continue
                
                if pub_date and pub_date > recent_cutoff:
                    if len(pi.images) == 0:
                        recent_posts_without_images.append(url)
                    if not pi.has_featured_image:
                        posts_without_featured_images.append(url)
            except:
                pass
        
        # Check for low quality content
        if pi.content_quality_score < 60:
            low_quality_posts.append((url, pi.content_quality_score))
        
        for l in pi.internal_links:
            all_links.add(l)
            inbound[l].add(url)
            links.append({"from": url, "to": l, "type": "internal"})
        for l in pi.external_links:
            all_links.add(l)
            links.append({"from": url, "to": l, "type": "external"})
        for src, alt in pi.images:
            all_images.add(src)
            images.append({
                "page": url, 
                "src": src, 
                "alt": alt,
                "has_alt": "yes" if alt.strip() else "no",
                "alt_length": len(alt)
            })

    # Check statuses
    print("🔍 Checking link and image statuses...")
    link_statuses = check_urls_status(all_links)
    img_statuses = check_urls_status(all_images)

    # Duplicate titles / duplicate canonicals
    title_index = defaultdict(list)
    canon_index = defaultdict(list)

    for url, pi in data.items():
        if pi.title:
            title_index[pi.title.strip()].append(url)
        if pi.canonical:
            canon_index[pi.canonical.strip()].append(url)

    # Build comprehensive issues list
    print("📋 Analyzing content quality issues...")
    
    for url, pi in data.items():
        # Page status issues
        if pi.status != 200:
            issues.append({"url": url, "type": "page_status", "severity": "high", "detail": f"HTTP {pi.status}"})
        
        # SEO issues
        if not pi.title:
            issues.append({"url": url, "type": "seo", "severity": "high", "detail": "Missing <title>"})
        elif len(pi.title) > 60:
            issues.append({"url": url, "type": "seo", "severity": "medium", "detail": f"Long <title> ({len(pi.title)} chars)"})
        elif len(pi.title) < 30:
            issues.append({"url": url, "type": "seo", "severity": "medium", "detail": f"Short <title> ({len(pi.title)} chars)"})
        
        if not pi.meta_desc:
            issues.append({"url": url, "type": "seo", "severity": "high", "detail": "Missing meta description"})
        elif len(pi.meta_desc) > 160:
            issues.append({"url": url, "type": "seo", "severity": "medium", "detail": f"Long meta description ({len(pi.meta_desc)} chars)"})
        elif len(pi.meta_desc) < 120:
            issues.append({"url": url, "type": "seo", "severity": "low", "detail": f"Short meta description ({len(pi.meta_desc)} chars)"})
        
        # Content quality issues
        if pi.word_count < 300:
            issues.append({"url": url, "type": "content_quality", "severity": "high", "detail": f"Very short content ({pi.word_count} words)"})
        elif pi.word_count < 500:
            issues.append({"url": url, "type": "content_quality", "severity": "medium", "detail": f"Short content ({pi.word_count} words)"})
        
        if len(pi.headings) == 0:
            issues.append({"url": url, "type": "content_structure", "severity": "medium", "detail": "No subheadings (H2-H6)"})
        elif len(pi.headings) < 2:
            issues.append({"url": url, "type": "content_structure", "severity": "low", "detail": "Few subheadings (less than 2)"})
        
        # Image issues
        if len(pi.images) == 0:
            issues.append({"url": url, "type": "images", "severity": "high", "detail": "No images found"})
        else:
            images_without_alt = sum(1 for _, alt in pi.images if not alt.strip())
            if images_without_alt > 0:
                issues.append({"url": url, "type": "accessibility", "severity": "medium", "detail": f"{images_without_alt} images missing alt text"})
        
        if not pi.has_featured_image:
            issues.append({"url": url, "type": "images", "severity": "medium", "detail": "No featured image detected"})
        
        # Social media optimization
        if not pi.social_meta.get('og:image'):
            issues.append({"url": url, "type": "social_media", "severity": "medium", "detail": "Missing Open Graph image"})
        if not pi.social_meta.get('og:title'):
            issues.append({"url": url, "type": "social_media", "severity": "low", "detail": "Missing Open Graph title"})
        if not pi.social_meta.get('og:description'):
            issues.append({"url": url, "type": "social_media", "severity": "low", "detail": "Missing Open Graph description"})
        
        # Technical issues
        if pi.mixed_content:
            issues.append({"url": url, "type": "security", "severity": "high", "detail": "Mixed content (HTTP assets on HTTPS page)"})
        
        if not pi.schema_markup:
            issues.append({"url": url, "type": "seo", "severity": "low", "detail": "No structured data (schema markup)"})
        
        # Content quality score
        if pi.content_quality_score < 50:
            issues.append({"url": url, "type": "content_quality", "severity": "high", "detail": f"Low content quality score ({pi.content_quality_score:.1f}/100)"})
        elif pi.content_quality_score < 70:
            issues.append({"url": url, "type": "content_quality", "severity": "medium", "detail": f"Medium content quality score ({pi.content_quality_score:.1f}/100)"})
        
        # Orphan risk (no internal inbound links) → except start page
        if url != start_url and url.startswith("http") and len(inbound.get(url, set())) == 0:
            issues.append({"url": url, "type": "internal_linking", "severity": "medium", "detail": "No internal inbound links (orphan risk)"})

    # Broken links/images
    for link, (code, final_u) in link_statuses.items():
        if code >= 400 or code == 0:
            issues.append({"url": link, "type": "broken_link", "severity": "high", "detail": f"HTTP {code} (final: {final_u})"})
    for img, (code, final_u) in img_statuses.items():
        if code >= 400 or code == 0:
            issues.append({"url": img, "type": "broken_image", "severity": "high", "detail": f"HTTP {code} (final: {final_u})"})

    # Duplicate titles (ignore empty)
    for title, urls in title_index.items():
        if title and len(urls) > 1:
            issues.append({"url": ", ".join(urls), "type": "duplicate_title", "severity": "medium", "detail": f'"{title}" appears on {len(urls)} pages'})

    # Duplicate canonicals (conflict)
    for can, urls in canon_index.items():
        if can and len(urls) > 1:
            issues.append({"url": ", ".join(urls), "type": "duplicate_canonical", "severity": "high", "detail": f'Canonical {can} used by {len(urls)} pages'})

    # Write enhanced CSVs
    print("📊 Generating comprehensive reports...")
    write_csv("pages_detailed.csv", pages, list(pages[0].keys()) if pages else [])
    write_csv("links.csv", links, list(links[0].keys()) if links else [])
    write_csv("images_detailed.csv", images, list(images[0].keys()) if images else [])
    write_csv("issues_prioritized.csv", issues, list(issues[0].keys()) if issues else [])

    # robots.txt & sitemap
    print("🔍 Checking robots.txt and sitemap...")
    robots_ok, sitemap_ok = False, False
    try:
        rr = requests.get(f"{start_url.rstrip('/')}/robots.txt", headers=HEADERS, timeout=DEFAULT_TIMEOUT)
        robots_ok = rr.status_code == 200
    except requests.RequestException:
        pass
    # Common sitemap locations to try
    sitemap_urls = [
        f"{start_url.rstrip('/')}/sitemap.xml",
        f"{start_url.rstrip('/')}/sitemap_index.xml",
        f"{start_url.rstrip('/')}/sitemap1.xml",
        f"{start_url.rstrip('/')}/wp-sitemap.xml",
    ]
    for su in sitemap_urls:
        try:
            sr = requests.get(su, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
            if sr.status_code == 200 and ("<urlset" in sr.text or "<sitemapindex" in sr.text):
                sitemap_ok = True
                break
        except requests.RequestException:
            continue

    # Enhanced analysis and summary
    broken_links = [i for i in issues if i["type"] == "broken_link"]
    broken_imgs = [i for i in issues if i["type"] == "broken_image"]
    orphan_pages = [i for i in issues if i["type"] == "internal_linking"]
    dup_titles = [i for i in issues if i["type"] == "duplicate_title"]
    dup_canons = [i for i in issues if i["type"] == "duplicate_canonical"]
    
    # Content quality analysis
    posts_without_images = [i for i in issues if i["type"] == "images" and "No images found" in i["detail"]]
    posts_without_featured = [i for i in issues if i["type"] == "images" and "featured image" in i["detail"]]
    low_quality_content = [i for i in issues if i["type"] == "content_quality" and i["severity"] == "high"]
    missing_alt_text = [i for i in issues if i["type"] == "accessibility"]
    
    # SEO issues
    seo_issues = [i for i in issues if i["type"] == "seo"]
    social_media_issues = [i for i in issues if i["type"] == "social_media"]
    
    # Content statistics
    total_pages = len(data)
    pages_with_images = sum(1 for _, pi in data.items() if len(pi.images) > 0)
    pages_with_featured_images = sum(1 for _, pi in data.items() if pi.has_featured_image)
    avg_word_count = sum(pi.word_count for _, pi in data.items()) / total_pages if total_pages > 0 else 0
    avg_quality_score = sum(pi.content_quality_score for _, pi in data.items()) / total_pages if total_pages > 0 else 0

    # Enhanced markdown summary
    summary = []
    summary.append(f"# 🔍 Comprehensive Site Health Audit Report\n")
    summary.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"**Start URL:** {start_url}")
    summary.append(f"**Pages Analyzed:** {total_pages}")
    summary.append(f"**robots.txt:** {'✅ Found' if robots_ok else '❌ Missing'}")
    summary.append(f"**Sitemap:** {'✅ Found' if sitemap_ok else '❌ Missing'}\n")

    summary.append("## 📊 Content Quality Overview")
    summary.append(f"- **Average Word Count:** {avg_word_count:.0f} words")
    summary.append(f"- **Average Quality Score:** {avg_quality_score:.1f}/100")
    summary.append(f"- **Pages with Images:** {pages_with_images}/{total_pages} ({(pages_with_images/total_pages*100):.1f}%)")
    summary.append(f"- **Pages with Featured Images:** {pages_with_featured_images}/{total_pages} ({(pages_with_featured_images/total_pages*100):.1f}%)")
    summary.append("")

    summary.append("## 🚨 Critical Issues Summary")
    
    def line(label, seq, severity=""):
        severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(severity, "")
        return f"- **{label}:** {len(seq)} {severity_emoji}"

    summary.append(line("Broken Links", broken_links, "high"))
    summary.append(line("Broken Images", broken_imgs, "high"))
    summary.append(line("Posts Without Images", posts_without_images, "high"))
    summary.append(line("Posts Without Featured Images", posts_without_featured, "medium"))
    summary.append(line("Low Quality Content", low_quality_content, "high"))
    summary.append(line("Missing Alt Text Issues", missing_alt_text, "medium"))
    summary.append("")

    summary.append("## 🎯 SEO & Social Media Issues")
    summary.append(line("SEO Issues", seo_issues))
    summary.append(line("Social Media Issues", social_media_issues))
    summary.append(line("Duplicate Titles", dup_titles, "medium"))
    summary.append(line("Duplicate Canonicals", dup_canons, "high"))
    summary.append(line("Orphaned Pages", orphan_pages, "medium"))
    summary.append("")

    if recent_posts_without_images:
        summary.append("## 🕒 Recent Posts Without Images (Last 30 Days)")
        for url in recent_posts_without_images[:10]:  # Show first 10
            summary.append(f"- {url}")
        if len(recent_posts_without_images) > 10:
            summary.append(f"- ... and {len(recent_posts_without_images) - 10} more")
        summary.append("")

    if low_quality_posts:
        summary.append("## 📉 Lowest Quality Posts")
        sorted_low_quality = sorted(low_quality_posts, key=lambda x: x[1])[:10]
        for url, score in sorted_low_quality:
            summary.append(f"- {url} (Score: {score:.1f}/100)")
        summary.append("")

    summary.append("## 📁 Generated Files")
    summary.append("- `pages_detailed.csv` — Complete page analysis with quality metrics")
    summary.append("- `images_detailed.csv` — Image analysis with alt text status")
    summary.append("- `issues_prioritized.csv` — All issues with severity levels")
    summary.append("- `links.csv` — Internal/external link mapping")
    summary.append("")

    summary.append("## 🔧 Priority Action Items")
    summary.append("1. **Fix Broken Content:** Address broken links and images immediately")
    summary.append("2. **Add Missing Images:** Ensure all posts have relevant images and featured images")
    summary.append("3. **Improve Alt Text:** Add descriptive alt text to all images for accessibility")
    summary.append("4. **Enhance Content Quality:** Focus on posts with quality scores below 70")
    summary.append("5. **SEO Optimization:** Fix missing titles, meta descriptions, and social media tags")
    summary.append("6. **Content Structure:** Add proper headings and improve readability")

    with open("comprehensive_audit_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(summary))

    print("✅ Generated comprehensive audit report:")
    print("   📄 comprehensive_audit_report.md")
    print("   📊 pages_detailed.csv")
    print("   🖼️ images_detailed.csv") 
    print("   🚨 issues_prioritized.csv")
    print("   🔗 links.csv")
    print(f"\n📈 Summary: {total_pages} pages analyzed, {len(issues)} issues found")
    print(f"🎯 Priority: {len([i for i in issues if i.get('severity') == 'high'])} high-severity issues")
    
    # Quick stats
    if posts_without_images:
        print(f"🖼️ Image Alert: {len(posts_without_images)} pages have no images!")
    if posts_without_featured:
        print(f"🎭 Featured Image Alert: {len(posts_without_featured)} pages missing featured images!")
    if low_quality_content:
        print(f"📝 Content Alert: {len(low_quality_content)} pages have low content quality!")

# ---- CLI ----
def main():
    ap = argparse.ArgumentParser(description="SphereVista360 — Site Health Auditor")
    ap.add_argument("--start", required=True, help="Start URL, e.g., https://spherevista360.com")
    ap.add_argument("--max-pages", type=int, default=400, help="Max pages to crawl")
    ap.add_argument("--same-domain", action="store_true", help="Restrict crawl to same domain")
    args = ap.parse_args()

    start = args.start.rstrip("/")
    if not start.startswith("http"):
        print("Start URL must include scheme, e.g., https://example.com")
        sys.exit(1)

    t0 = time.time()
    data = crawl(start, max_pages=args.max_pages, same_domain_only=args.same_domain)
    generate_reports(data, start_url=start)
    print(f"⏱  Done in {time.time() - t0:.1f}s")

if __name__ == "__main__":
    main()
