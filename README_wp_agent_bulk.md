# 📘 WordPress Bulk Markdown Uploader (`wp_agent_bulk.py`)# 📘 WordPress Bulk Markdown Uploader (`wp_agent_bulk.py`)



Automate posting to WordPress using Markdown files with YAML front matter.  Automate posting to WordPress using Markdown files with YAML front matter.  

Supports **categories, SEO fields, and embedded images** — ideal for blogs like *SphereVista360*.Supports **categories, SEO fields, and embedded images** — ideal for blogs like *SphereVista360*.



------



## 🚀 Features## 🚀 Features

- 📝 Converts Markdown → HTML automatically  - 📝 Converts Markdown → HTML automatically  

- 🏷️ Reads YAML front matter (`title`, `category`, `tags`, `publish`, `seo_title`, etc.)  - 🏷️ Reads YAML front matter (`title`, `category`, `tags`, `publish`, `seo_title`, etc.)  

- 🧠 Smart category detection:- 🧠 Auto-routes categories by keywords if not specified  

  - From folder name (NEW!)- 🖼️ Embeds the **first image** (local `.jpg`/`.png` or remote URL)  

  - From YAML front matter- ⚙️ Supports **RankMath SEO fields**  

  - From content keywords- 🔗 Optional **UTM tracking** and **forced category**  

- 🖼️ Embeds the **first image** (local `.jpg`/`.png` or remote URL)  - 🗂️ Command-line options for placement, publishing, and control

- ⚙️ Supports **RankMath SEO fields**  

- 🔗 Optional **UTM tracking** and **forced category**  ---

- 🗂️ Command-line options for placement, publishing, and control

- 🚫 Automatically skips README.md files (NEW!)## ⚙️ Setup

- 📂 Recursively processes subfolders (NEW!)```bash

pip install requests markdown pyyaml python-slugify

---export WP_SITE="https://spherevista360.com"

export WP_USER="your_editor_username"

## ⚙️ Setupexport WP_APP_PASS="your application password WITH SPACES"

```bash```

pip install requests markdown pyyaml python-slugify> 💡 Create the Application Password in WordPress:  

export WP_SITE="https://spherevista360.com"> **Users → Profile → Application Passwords → Add New.**

export WP_USER="your_editor_username"

export WP_APP_PASS="your application password WITH SPACES"---

```

> 💡 Create the Application Password in WordPress:  ## 📁 Folder structure

> **Users → Profile → Application Passwords → Add New.**```

/posts_to_upload/

---  ai-trends-2025.md

  ai-trends-2025.jpg

## 📁 Folder structure  nri-investing-guide.md

``````

/posts_to_upload/Example Markdown front matter:

  Finance/```yaml

    nri-investing-guide.md---

    nri-investing-guide.jpgtitle: "AI Trends in 2025"

    high-dividend-stocks.mdexcerpt: "Emerging innovations shaping the future."

  Tech/category: "Tech"

    ai-trends-2025.mdtags: ["AI","Innovation"]

    ai-trends-2025.jpgpublish: false

  README.md (automatically skipped)slug: "ai-trends-2025"

```seo_title: "AI Trends in 2025 - Tech Insights"

seo_description: "Discover what AI will look like in 2025 — from generative tools to regulation."

Example Markdown front matter:image: "https://example.com/image.jpg"

```yamlimage_caption: "AI model visualization"

------

title: "AI Trends in 2025"## Overview

excerpt: "Emerging innovations shaping the future."Main Markdown content starts here...

category: "Tech"  # Optional: will use folder name if not specified```

tags: ["AI","Innovation"]

publish: false---

slug: "ai-trends-2025"

seo_title: "AI Trends in 2025 - Tech Insights"## 🧭 Usage

seo_description: "Discover what AI will look like in 2025 — from generative tools to regulation."

image: "https://example.com/image.jpg"| Command | Action |

image_caption: "AI model visualization"|----------|---------|

---| `python wp_agent_bulk.py posts_to_upload` | Create drafts (default image after `<h2>`) |

## Overview| `python wp_agent_bulk.py posts_to_upload --top-image` | Embed image at top |

Main Markdown content starts here...| `python wp_agent_bulk.py posts_to_upload --no-image` | Skip image embedding |

```| `python wp_agent_bulk.py posts_to_upload --publish` | Publish immediately |

| `python wp_agent_bulk.py posts_to_upload --category Finance` | Force all posts into Finance |

---| `python wp_agent_bulk.py posts_to_upload --utm "?utm_source=spherevista360&utm_medium=blog"` | Append UTM tags to all links |



## 🧭 Usage---



| Command | Action |## 🧩 Example workflow

|----------|---------|```bash

| `python wp_agent_bulk.py posts_to_upload` | Create drafts (default image after `<h2>`) |mkdir ~/spherevista360

| `python wp_agent_bulk.py posts_to_upload --top-image` | Embed image at top |cd ~/spherevista360

| `python wp_agent_bulk.py posts_to_upload --no-image` | Skip image embedding |python wp_agent_bulk.py posts_to_upload --top-image --publish --utm "?utm_source=spherevista360&utm_medium=blog"

| `python wp_agent_bulk.py posts_to_upload --publish` | Publish immediately |```

| `python wp_agent_bulk.py posts_to_upload --category Finance` | Force all posts into Finance |

| `python wp_agent_bulk.py posts_to_upload --utm "?utm_source=spherevista360&utm_medium=blog"` | Append UTM tags to all links |---



---## 🩺 Troubleshooting

| Problem | Solution |

## 🧩 Example workflow|----------|-----------|

```bash| 401 Unauthorized | Regenerate Application Password and ensure HTTPS. |

mkdir -p ~/spherevista360/posts_to_upload/{Finance,Tech,World}| File is empty | Delete or replace zero-byte `.jpg`/.png files. |

cd ~/spherevista360| rest_upload_unknown_error | Increase PHP upload limits in hPanel or `.htaccess`. |

# Create your .md files in appropriate folders| Script exits immediately | Check folder path and credentials. |

python wp_agent_bulk.py posts_to_upload --top-image --publish --utm "?utm_source=spherevista360&utm_medium=blog"

```---



---## 🧠 Notes

- Default category routing keywords are defined in the script.  

## 🩺 Troubleshooting- Use front matter to override title, category, and SEO meta.  

| Problem | Solution |- RankMath SEO fields auto-populate if plugin is active.  

|----------|-----------|- Re-running the script is safe; it won’t overwrite published posts.

| 401 Unauthorized | Regenerate Application Password and ensure HTTPS. |

| File is empty | Delete or replace zero-byte `.jpg`/.png files. |---

| rest_upload_unknown_error | Increase PHP upload limits in hPanel or `.htaccess`. |

| Script exits immediately | Check folder path and credentials. |## 🏁 Quick Test

| README.md published | Use latest version - READMEs are now auto-skipped. |```bash

| Category issues | Check folder name, YAML front matter, or keyword mapping. |python wp_agent_bulk.py posts_to_upload --no-image

```

---Check WordPress → Posts → Drafts — your content should appear!



## 🧠 Notes---

- Files named README.md are automatically skipped

- Categories are determined in this order:**Author:** SphereVista360 Automation  

  1. Command-line `--category` override**Version:** 1.2.0  

  2. YAML front matter `category`**License:** MIT  

  3. Parent folder name**Purpose:** Effortless, SEO-ready WordPress content publishing ✨

  4. Keyword-based auto-detection
- Default category routing keywords are defined in the script
- Use front matter to override title, category, and SEO meta
- RankMath SEO fields auto-populate if plugin is active
- Re-running the script is safe; it won't overwrite published posts

---

## 🏁 Quick Test
```bash
python wp_agent_bulk.py posts_to_upload --no-image
```
Check WordPress → Posts → Drafts — your content should appear!

---

**Author:** SphereVista360 Automation  
**Version:** 1.3.0  
**License:** MIT  
**Purpose:** Effortless, SEO-ready WordPress content publishing ✨

## 💎 Pro Version
Looking for more advanced features? Check out [SphereVista360 Pro](./PREMIUM_FEATURES.md):
- 🤖 AI-powered content enhancement
- 📊 Advanced SEO & Analytics
- 🔄 Workflow automation
- 🖼️ Advanced media handling
- 🔒 Security & backup features
- 📧 Premium support

## ❤️ Support This Project
If you find this tool useful, consider:
- ⭐ Starring the repository
- 💖 [Becoming a sponsor](https://github.com/sponsors/YOUR_USERNAME)
- ☕ [Buying me a coffee](https://www.buymeacoffee.com/spherevista360)
- 🤝 Contributing code or documentation