# 🌐 SphereVista360 - WordPress Content Management Platform# 📘 WordPress Bulk Markdown Uploader (`wp_agent_bulk.py`)



A comprehensive WordPress automation and content management system with advanced publishing tools, security enhancements, and SEO optimization.Automate posting to WordPress using Markdown files with YAML front matter.  

Supports **categories, SEO fields, and embedded images** — ideal for blogs like *SphereVista360*.

## 🚀 Quick Start

---

### Content Publishing

```bash## 🚀 Features

cd wordpress-enhancements/scripts- 📝 Converts Markdown → HTML automatically  

python smart_publisher.py- 🏷️ Reads YAML front matter (`title`, `category`, `tags`, `publish`, `seo_title`, etc.)  

# Select: E (Smart bulk publishing)- 🧠 Auto-routes categories by keywords if not specified  

```- 🖼️ Embeds the **first image** (local `.jpg`/`.png` or remote URL)  

- ⚙️ Supports **RankMath SEO fields**  

### Content Analysis & Cleanup- 🔗 Optional **UTM tracking** and **forced category**  

```bash- 🗂️ Command-line options for placement, publishing, and control

cd wordpress-enhancements/scripts  

python post_analyzer.py---

```

## ⚙️ Setup

## 📁 Project Structure```bash

pip install requests markdown pyyaml python-slugify

```export WP_SITE="https://spherevista360.com"

spherevista360/export WP_USER="your_editor_username"

├── README.md                      # This file - main project overviewexport WP_APP_PASS="your application password WITH SPACES"

├── docs/                         # Project documentation```

├── wordpress-enhancements/       # Core WordPress tools & enhancements> 💡 Create the Application Password in WordPress:  

│   ├── scripts/                  # Production tools> **Users → Profile → Application Passwords → Add New.**

│   │   ├── smart_publisher.py    # ⭐ Main publishing system

│   │   ├── post_analyzer.py      # ⭐ Analysis & cleanup tool---

│   │   └── SMART_PUBLISHER_GUIDE.md

│   └── archive/                  # Specialized & legacy tools## 📁 Folder structure

├── spherevista360_week1_final/   # Content repository```

└── temp_images/                  # Temporary image processing/posts_to_upload/

```  ai-trends-2025.md

  ai-trends-2025.jpg

## 🎯 Core Tools  nri-investing-guide.md

```

### 🚀 WordPress Enhancement SuiteExample Markdown front matter:

Located in `wordpress-enhancements/`:```yaml

- **Smart Publisher** - Intelligent content publishing with bulk operations---

- **Post Analyzer** - Content analysis, duplicate detection, and cleanuptitle: "AI Trends in 2025"

- **Archive Tools** - Specialized SEO, security, and plugin management toolsexcerpt: "Emerging innovations shaping the future."

category: "Tech"

### 📝 Content Managementtags: ["AI","Innovation"]

- **Bulk Publishing** - Process multiple categories with duplicate detectionpublish: false

- **Content Analysis** - Identify and manage existing posts  slug: "ai-trends-2025"

- **Category Organization** - Finance, Technology, Politics, Travel, World, Businessseo_title: "AI Trends in 2025 - Tech Insights"

- **SEO Optimization** - Automated SEO enhancements and image optimizationseo_description: "Discover what AI will look like in 2025 — from generative tools to regulation."

image: "https://example.com/image.jpg"

## 🛠️ Setup & Configurationimage_caption: "AI model visualization"

---

### Prerequisites## Overview

1. **WordPress Site** with REST API enabledMain Markdown content starts here...

2. **Application Password** for WordPress authentication```

3. **Python Environment** with required dependencies

---

### Environment Setup

```bash## 🧭 Usage

export WP_SITE='https://spherevista360.com'

export WP_USER='your-username'  | Command | Action |

export WP_APP_PASS='your-app-password'|----------|---------|

```| `python wp_agent_bulk.py posts_to_upload` | Create drafts (default image after `<h2>`) |

| `python wp_agent_bulk.py posts_to_upload --top-image` | Embed image at top |

### First-Time Setup| `python wp_agent_bulk.py posts_to_upload --no-image` | Skip image embedding |

```bash| `python wp_agent_bulk.py posts_to_upload --publish` | Publish immediately |

# Navigate to tools directory| `python wp_agent_bulk.py posts_to_upload --category Finance` | Force all posts into Finance |

cd wordpress-enhancements/scripts| `python wp_agent_bulk.py posts_to_upload --utm "?utm_source=spherevista360&utm_medium=blog"` | Append UTM tags to all links |



# Test connection---

python post_analyzer.py

# Select: D (Check existing posts only)## 🧩 Example workflow

```bash

# Publish contentmkdir ~/spherevista360

python smart_publisher.py  cd ~/spherevista360

# Select: E (Smart bulk publishing)python wp_agent_bulk.py posts_to_upload --top-image --publish --utm "?utm_source=spherevista360&utm_medium=blog"

``````



## 📚 Documentation---



### Core Documentation## 🩺 Troubleshooting

- **Main Guide** - `wordpress-enhancements/README.md`| Problem | Solution |

- **User Manual** - `wordpress-enhancements/scripts/SMART_PUBLISHER_GUIDE.md`|----------|-----------|

- **Archive Guide** - `wordpress-enhancements/archive/README.md`| 401 Unauthorized | Regenerate Application Password and ensure HTTPS. |

| File is empty | Delete or replace zero-byte `.jpg`/.png files. |

### Project Documentation| rest_upload_unknown_error | Increase PHP upload limits in hPanel or `.htaccess`. |

- **Project Structure** - `docs/project/PROJECT_STRUCTURE.md`| Script exits immediately | Check folder path and credentials. |

- **Quick Reference** - `docs/project/QUICK_REFERENCE.md`

- **Security Notes** - `docs/security/`---

- **Archived Guides** - `docs/archive/`

## 🧠 Notes

## 🔧 Common Workflows- Default category routing keywords are defined in the script.  

- Use front matter to override title, category, and SEO meta.  

### 1. Publishing New Content- RankMath SEO fields auto-populate if plugin is active.  

```bash- Re-running the script is safe; it won’t overwrite published posts.

cd wordpress-enhancements/scripts

python smart_publisher.py---

# Option E: Analyzes all categories, publishes only new content

```## 🏁 Quick Test

```bash

### 2. Content Audit & Cleanuppython wp_agent_bulk.py posts_to_upload --no-image

```bash```

cd wordpress-enhancements/scriptsCheck WordPress → Posts → Drafts — your content should appear!

python post_analyzer.py

# Interactive analysis and cleanup options---

```

**Author:** SphereVista360 Automation  

### 3. Specialized Tasks**Version:** 1.2.0  

```bash**License:** MIT  

# SEO optimization**Purpose:** Effortless, SEO-ready WordPress content publishing ✨

cd wordpress-enhancements/archive/seo
python seo_optimizer.py

# Plugin management  
cd wordpress-enhancements/archive/plugins
python wp_plugin_installer.py

# Security hardening
cd wordpress-enhancements/archive/security
python wp_security_hardener.py
```

## ✨ Key Features

### 🎯 Smart Publishing
- **Bulk Operations** - Process all categories at once
- **Duplicate Detection** - Prevents duplicate posts automatically
- **Content Analysis** - Shows what's new vs existing
- **Safety Confirmations** - Interactive prompts before publishing

### 🔍 Advanced Analysis
- **Post Detection** - Identify content by indicators and categories  
- **Targeted Cleanup** - Remove specific posts or entire categories
- **Detailed Reports** - Comprehensive breakdowns and statistics

### 🛡️ Enterprise Features
- **Security Hardening** - WordPress security automation
- **SEO Optimization** - Automated SEO enhancements
- **Plugin Management** - Automated installation and configuration
- **Content Organization** - Professional content management workflows

## 🏆 Professional Results

### Before Enhancement
- Manual content publishing
- Duplicate post issues
- Scattered tools and documentation
- Security vulnerabilities

### After Enhancement
- ✅ **Automated bulk publishing** with duplicate prevention
- ✅ **Professional tool organization** with clear workflows  
- ✅ **Comprehensive documentation** and user guides
- ✅ **Security hardening** and credential protection
- ✅ **SEO optimization** and content management
- ✅ **Scalable architecture** for future enhancements

## 🆘 Support & Troubleshooting

### Common Issues
- **Authentication**: Test with `post_analyzer.py` → Option D
- **Duplicates**: Use `post_analyzer.py` for cleanup
- **Missing Content**: Check with `smart_publisher.py` → Option H

### Getting Help
1. Check the detailed guides in `wordpress-enhancements/`
2. Review project documentation in `docs/`
3. Use interactive tool options for guidance

---

## 🎯 Mission Statement

**SphereVista360** provides a professional-grade WordPress content management platform that automates publishing workflows, prevents content issues, and maintains enterprise-level security and SEO standards.

**Ready for production use! 🚀**