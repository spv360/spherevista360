import requests, json

SITE = "https://spherevista360.com"
API = f"{SITE}/wp-json/wp/v2"
USER = "JK"
APP_PASS = "R8sj tOZG 8ORr ntSZ XlPt qTE9"   # as generated in WP

def create_category(name):
    # Check if exists
    r = requests.get(f"{API}/categories", params={"search": name}, auth=(USER, APP_PASS))
    r.raise_for_status()
    for cat in r.json():
        if cat["name"].lower() == name.lower():
            return cat["id"]
    # Create if not found
    r = requests.post(f"{API}/categories",
                      auth=(USER, APP_PASS),
                      json={"name": name})
    r.raise_for_status()
    return r.json()["id"]

def upload_featured_image(path, filename="cover.jpg"):
    with open(path, "rb") as f:
        r = requests.post(
            f"{API}/media",
            auth=(USER, APP_PASS),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            files={"file": (filename, f, "image/jpeg")}
        )
    r.raise_for_status()
    return r.json()["id"]  # media attachment ID

def create_post(title, html_content, excerpt, category_names, tags=[], featured_image_path=None, publish=False):
    cat_ids = [create_category(c) for c in category_names]
    featured_id = upload_featured_image(featured_image_path) if featured_image_path else None
    payload = {
        "status": "publish" if publish else "draft",
        "title": title,
        "content": html_content,
        "excerpt": excerpt,
        "categories": cat_ids,
        "tags": [],
    }
    if featured_id:
        payload["featured_media"] = featured_id

    r = requests.post(f"{API}/posts", auth=(USER, APP_PASS), json=payload)
    r.raise_for_status()
    return r.json()

# === Example usage ===
post = create_post(
    title="How NRIs Can Start Investing in U.S. Stocks (2025 Guide)",
    html_content="""
      <h2>Step-by-step</h2>
      <p>Everything you need to know to get started…</p>
      <h3>Documents</h3><ul><li>Passport</li><li>W-8BEN</li></ul>
    """,
    excerpt="NRI investing in U.S. made simple: brokers, docs, taxes.",
    category_names=["Finance", "World"],
    featured_image_path=None,   # e.g. "/path/to/cover.jpg"
    publish=False               # True to publish immediately
)
print("Created post ID:", post["id"])