# wp_agent_post.py
# Creates WordPress DRAFT posts via REST API (safe for beginners).
# Requires: pip install requests

import requests
from pathlib import Path

SITE = "https://spherevista360.com"                 # ← your site
USER = "JK"                            # ← WP editor user
APP_PASS = "R8sj tOZG 8ORr ntSZ XlPt qTE9"       # ← WP Application Password

API = f"{SITE}/wp-json/wp/v2"

def ensure_category(name):
    r = requests.get(f"{API}/categories", params={"search": name}, auth=(USER, APP_PASS))
    r.raise_for_status()
    for cat in r.json():
        if cat["name"].lower() == name.lower():
            return cat["id"]
    r = requests.post(f"{API}/categories", auth=(USER, APP_PASS), json={"name": name})
    r.raise_for_status()
    return r.json()["id"]

def upload_media(local_path, filename=None, mime="image/jpeg"):
    p = Path(local_path)
    if not p.exists():
        return None
    if not filename:
        filename = p.name
    with p.open("rb") as f:
        r = requests.post(
            f"{API}/media",
            auth=(USER, APP_PASS),
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            files={"file": (filename, f, mime)},
        )
    r.raise_for_status()
    return r.json()["id"]  # media ID

def create_post(title, html, excerpt, categories=("Finance",), featured=None, publish=False):
    cat_ids = [ensure_category(c) for c in categories]
    payload = {
        "status": "publish" if publish else "draft",
        "title": title,
        "content": html,
        "excerpt": excerpt,
        "categories": cat_ids,
        # Optional RankMath SEO meta (uncomment if you use RankMath)
        "meta": {
            "rank_math_title": title[:58],  # keep under ~60 chars
            "rank_math_description": excerpt[:155]  # keep under ~160 chars
        }
    }
    if featured:
        media_id = upload_media(featured)
        if media_id:
            payload["featured_media"] = media_id

    r = requests.post(f"{API}/posts", auth=(USER, APP_PASS), json=payload)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    html = """
      <h2>Overview</h2>
      <p>This draft was created via the WordPress REST API.</p>
      <h3>Key Points</h3>
      <ul><li>Step-by-step guide</li><li>Documents & brokers</li><li>Simple first trade</li></ul>
    """.strip()

    post = create_post(
        title="NRI Investing in U.S. (2025 Guide)",
        html=html,
        excerpt="NRI investing in U.S. made simple: brokers, docs, taxes, first steps.",
        categories=("Finance","World"),
        featured=None,           # e.g. "cover.jpg"
        publish=False            # change to True after you trust workflow
    )
    print("Draft created:", f"{SITE}/wp-admin/post.php?post={post['id']}&action=edit")
