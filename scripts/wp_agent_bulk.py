"""
WordPress Bulk Markdown Uploader (recursive + folder-based categories)
---------------------------------------------------------------------
Creates draft or published posts from Markdown files with optional YAML front matter.

Features:
- Markdown ➜ HTML
- YAML front matter for title, excerpt, tags, category, publish, slug, SEO
- Smart keyword-based category routing (auto)
- NEW: Recursively scans subfolders
- NEW: Auto-category from folder name if not provided in YAML
- Front matter image or local sibling image embedding (after <h2> by default or top with flag)
- Optional RankMath SEO fields
- Command-line flags for flexibility
"""

import os, sys, re, base64, requests, argparse, yaml
from pathlib import Path
from slugify import slugify
import markdown as md

SITE = os.getenv("WP_SITE", "https://spherevista360.com")
USER = os.getenv("WP_USER", "EDITOR_USERNAME")
APP_PASS = os.getenv("WP_APP_PASS", "APPLICATION PASSWORD WITH SPACES")
API = f"{SITE.rstrip('/')}/wp-json/wp/v2"
TIMEOUT = 25

CATEGORY_MAP = {
    "Finance": ["stock", "market", "invest", "fund", "nri"],
    "Tech": ["ai", "cloud", "saas", "startup", "github", "linux", "app"],
    "World": ["election", "policy", "global", "geopolitic"],
    "Travel": ["travel", "visa", "hotel"],
    "Politics": ["parliament", "president", "minister"],
}
DEFAULT_CATEGORY = "World"

def auth_header():
    token = base64.b64encode(f"{USER}:{APP_PASS}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

def get_json(url, **kw):
    r = requests.get(url, headers=auth_header(), timeout=TIMEOUT, **kw)
    r.raise_for_status()
    return r.json()

def post_json(url, payload, files=None):
    headers = auth_header()
    if files:
        r = requests.post(url, headers=headers, files=files, timeout=TIMEOUT)
    else:
        headers["Content-Type"] = "application/json"
        r = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def ensure_category(name):
    res = get_json(f"{API}/categories", params={"search": name})
    for c in res:
        if c["name"].lower() == name.lower():
            return c["id"]
    created = post_json(f"{API}/categories", {"name": name})
    return created["id"]

def detect_category(text):
    t = text.lower()
    for cat, keys in CATEGORY_MAP.items():
        for k in keys:
            if k in t:
                return cat
    return DEFAULT_CATEGORY

def read_markdown(p: Path):
    text = p.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            return fm, parts[2].strip()
    return {}, text

def md_to_html(md_text): 
    return md.markdown(md_text, extensions=["extra", "fenced_code", "tables"])

def first_sentence(t, limit=155):
    parts = re.split(r"(?<=[.!?])\s+", t.strip())
    return (parts[0] if parts else t[:limit])[:limit]

# ---- Image embedding ----
def upload_media_return_url(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        return None, None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    files = {"file": (path.name, path.read_bytes(), mime)}
    resp = post_json(f"{API}/media", None, files=files)
    return resp.get("id"), resp.get("source_url")

def pick_first_image(md_path, fm):
    if (img := fm.get("image", "")) and img.startswith("http"):
        return "remote", img
    for ext in (".jpg", ".jpeg", ".png"):
        c = md_path.with_suffix(ext)
        if c.exists() and c.stat().st_size > 0:
            return "local", c
    return None, None

def wrap_with_figure(url, alt="", caption=""):
    alt = alt.replace('"', "&quot;")
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure style="text-align:center;margin:1rem 0;"><img src="{url}" alt="{alt}" style="max-width:100%;height:auto;">{cap}</figure>'

def inject_after_first_h2(html, block):
    if not block: return html
    m = re.search(r"(</h2>)", html, flags=re.I)
    return f"{html[:m.end()]}\n\n{block}\n\n{html[m.end():]}" if m else f"{block}\n\n{html}"

def create_post(title, html, excerpt, category_name, publish=False, slug=None, rank_title=None, rank_desc=None):
    cid = ensure_category(category_name)
    payload = {
        "status": "publish" if publish else "draft",
        "title": title, "content": html, "excerpt": excerpt, "categories": [cid]
    }
    if slug: payload["slug"] = slugify(slug)[:60]
    meta = {}
    if rank_title: meta["rank_math_title"] = rank_title[:58]
    if rank_desc: meta["rank_math_description"] = rank_desc[:155]
    if meta: payload["meta"] = meta
    return post_json(f"{API}/posts", payload)

def process(md_dir: Path, place_top=False, disable_image=False, force_publish=False, force_category=None, utm=None):
    # Self-test
    name = get_json(f"{SITE}/wp-json/").get("name")
    me = get_json(f"{API}/users/me")
    print(f"✅ Connected to {name} as {me.get('name')} (roles: {me.get('roles')})")

    # RECURSIVE scan (excluding README.md files)
    md_files = [f for f in sorted(md_dir.rglob("*.md")) if f.name.lower() != "readme.md"]
    if not md_files:
        print("No .md files found (excluding READMEs, including subfolders).")
        return

    for p in md_files:
        print(f"— {p.relative_to(md_dir)}")
        fm, body = read_markdown(p)
        title = fm.get("title") or p.stem.replace("-", " ").title()
        excerpt = fm.get("excerpt") or first_sentence(body)

        # Auto-category from folder if no YAML category
        folder_cat = p.parent.name.strip()
        auto_cat = folder_cat if folder_cat not in (".", "") else None
        cat = force_category or fm.get("category") or auto_cat or detect_category(title + " " + body)

        publish = bool(force_publish or fm.get("publish", False))
        slug = fm.get("slug") or title

        embedded = ""
        if not disable_image:
            kind, val = pick_first_image(p, fm)
            if kind == "remote":
                embedded = wrap_with_figure(val, alt=title, caption=fm.get("image_caption", ""))
            elif kind == "local":
                print(f"📸 Uploading {val.name} ...")
                _, url = upload_media_return_url(val)
                if url: embedded = wrap_with_figure(url, alt=title, caption=fm.get("image_caption", ""))

        html = md_to_html(body)
        if utm:
            html = re.sub(r"(https?://[^ \"'<>]+)", lambda m: m.group(1) + utm, html)
        html = f"{embedded}\n\n{html}" if (place_top and embedded) else inject_after_first_h2(html, embedded)

        rank_title, rank_desc = fm.get("seo_title") or title, fm.get("seo_description") or excerpt
        post = create_post(title, html, excerpt, cat, publish, slug, rank_title, rank_desc)
        print(f"✅ {post['status'].upper()} — {title} → {SITE}/wp-admin/post.php?post={post['id']}&action=edit")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk-upload Markdown posts to WordPress (recursive).")
    parser.add_argument("folder", help="Folder containing .md files (scans subfolders recursively)")
    parser.add_argument("--top-image", action="store_true", help="Embed image at very top (default after first <h2>).")
    parser.add_argument("--no-image", action="store_true", help="Skip image embedding entirely.")
    parser.add_argument("--publish", action="store_true", help="Publish posts (default drafts).")
    parser.add_argument("--category", help="Force all posts into a specific category (overrides folder & YAML).")
    parser.add_argument("--utm", help="Append UTM string to all links (e.g., '?utm_source=spherevista360').")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists():
        sys.exit(f"Folder not found: {folder}")

    try:
        process(
            folder,
            place_top=bool(args.top_image),
            disable_image=bool(args.no_image),
            force_publish=bool(args.publish),
            force_category=args.category,
            utm=args.utm
        )
    except requests.HTTPError as err:
        print("❌ HTTP error:", err.response.status_code, err.response.text[:500])
        print("\nTroubleshoot:")
        print("- Regenerate Application Password (Users → Profile).")
        print("- Ensure HTTPS is enabled in Settings → General.")
        print("- If Apache, pass Authorization header to PHP via .htaccess.")
        print("- Temporarily disable security/WAF plugins and retry.")
        sys.exit(1)
