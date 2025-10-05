# 📘 WordPress Bulk Markdown Uploader (`wp_agent_bulk.py`)

Automate posting to WordPress using Markdown files with YAML front matter.  
Supports **categories, SEO fields, and embedded images** — ideal for blogs like *SphereVista360*.

---

## 🚀 Features
- 📝 Converts Markdown → HTML automatically  
- 🏷️ Reads YAML front matter (`title`, `category`, `tags`, `publish`, `seo_title`, etc.)  
- 🧠 Auto-routes categories by keywords if not specified  
- 🖼️ Embeds the **first image** (local `.jpg`/`.png` or remote URL)  
- ⚙️ Supports **RankMath SEO fields**  
- 🔗 Optional **UTM tracking** and **forced category**  
- 🗂️ Command-line options for placement, publishing, and control

---

## ⚙️ Setup
```bash
pip install requests markdown pyyaml python-slugify
export WP_SITE="https://spherevista360.com"
export WP_USER="your_editor_username"
export WP_APP_PASS="your application password WITH SPACES"
```
> 💡 Create the Application Password in WordPress:  
> **Users → Profile → Application Passwords → Add New.**

---

## 📁 Folder structure
```
/posts_to_upload/
  ai-trends-2025.md
  ai-trends-2025.jpg
  nri-investing-guide.md
```
Example Markdown front matter:
```yaml
---
title: "AI Trends in 2025"
excerpt: "Emerging innovations shaping the future."
category: "Tech"
tags: ["AI","Innovation"]
publish: false
slug: "ai-trends-2025"
seo_title: "AI Trends in 2025 - Tech Insights"
seo_description: "Discover what AI will look like in 2025 — from generative tools to regulation."
image: "https://example.com/image.jpg"
image_caption: "AI model visualization"
---
## Overview
Main Markdown content starts here...
```

---

## 🧭 Usage

| Command | Action |
|----------|---------|
| `python wp_agent_bulk.py posts_to_upload` | Create drafts (default image after `<h2>`) |
| `python wp_agent_bulk.py posts_to_upload --top-image` | Embed image at top |
| `python wp_agent_bulk.py posts_to_upload --no-image` | Skip image embedding |
| `python wp_agent_bulk.py posts_to_upload --publish` | Publish immediately |
| `python wp_agent_bulk.py posts_to_upload --category Finance` | Force all posts into Finance |
| `python wp_agent_bulk.py posts_to_upload --utm "?utm_source=spherevista360&utm_medium=blog"` | Append UTM tags to all links |

---

## 🧩 Example workflow
```bash
mkdir ~/spherevista360
cd ~/spherevista360
python wp_agent_bulk.py posts_to_upload --top-image --publish --utm "?utm_source=spherevista360&utm_medium=blog"
```

---

## 🩺 Troubleshooting
| Problem | Solution |
|----------|-----------|
| 401 Unauthorized | Regenerate Application Password and ensure HTTPS. |
| File is empty | Delete or replace zero-byte `.jpg`/.png files. |
| rest_upload_unknown_error | Increase PHP upload limits in hPanel or `.htaccess`. |
| Script exits immediately | Check folder path and credentials. |

---

## 🧠 Notes
- Default category routing keywords are defined in the script.  
- Use front matter to override title, category, and SEO meta.  
- RankMath SEO fields auto-populate if plugin is active.  
- Re-running the script is safe; it won’t overwrite published posts.

---

## 🏁 Quick Test
```bash
python wp_agent_bulk.py posts_to_upload --no-image
```
Check WordPress → Posts → Drafts — your content should appear!

---

**Author:** SphereVista360 Automation  
**Version:** 1.2.0  
**License:** MIT  
**Purpose:** Effortless, SEO-ready WordPress content publishing ✨
