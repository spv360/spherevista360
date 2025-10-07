import zipfile, textwrap
from pathlib import Path

BASE_DIR = Path("spherevista360_week2_final")
FOLDERS = ["Finance", "Technology", "World", "Travel", "Politics", "Entertainment", "Business"]
for f in FOLDERS:
    (BASE_DIR / f).mkdir(parents=True, exist_ok=True)

def md(s: str) -> str:
    return textwrap.dedent(s).strip() + "\n"

# All Unsplash URLs normalized for 800x500 with good quality
POSTS = {
# =========================
# Finance (2)
# =========================
"Finance/01-ai-agents-in-retail-investing-2025.md": md("""\
---
title: "AI Agents in Retail Investing: What Actually Works in 2025"
excerpt: "From rebalancing to alerts, here’s how everyday investors use AI agents without taking dumb risks."
category: "Finance"
tags: ["AI", "Investing", "Automation", "2025"]
seo_title: "AI Agents for Investors (2025): Practical Uses and Risks"
seo_description: "A practical guide to AI agents for retail investing in 2025—use cases, guardrails, and how to avoid common pitfalls."
publish: true
image: "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&w=800&h=500&q=80"
alt: "AI assistant overlaying stock charts – Finance"
---

AI agents are moving from demos to daily tools. The best automate grunt work—screening, alerts, and simple rebalancing—without handing over full control.
Use them to extend your process, not replace your judgment.

## Where AI Agents Help
- **Signal triage:** Filter noise and surface notable moves.  
- **Rules-based rebalancing:** Execute guardrails you set.  
- **Portfolio hygiene:** Fees, drift, and tax awareness.

## Guardrails
Set position limits, confirm orders manually, and review logs weekly.

**Related reading:**  
- [Digital Banking Revolution: The Future of FinTech](https://spherevista360.com/digital-banking-2025/)  
- [AI Cybersecurity 2025: Automation for Defense](https://spherevista360.com/ai-cybersecurity-automation/)
"""),

"Finance/02-green-bonds-and-energy-transition-2025.md": md("""\
---
title: "Green Bonds and the Energy Transition: Where Yields Make Sense"
excerpt: "How to evaluate sustainability-linked debt without overpaying for the label."
category: "Finance"
tags: ["Green bonds", "Sustainable finance", "Energy"]
seo_title: "Green Bonds 2025: Returns, Risks, and Real Impact"
seo_description: "Understand how to evaluate green bonds in 2025—what to read in frameworks, pricing, and actual climate impact."
publish: true
image: "https://images.unsplash.com/photo-1509395176047-4a66953fd231?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Wind turbines at sunset – Finance"
---

Green debt markets have matured, but pricing varies widely. Look beyond labels to frameworks, capex plans, and third-party assurance.
Blended portfolios can capture yield without concentration risk.

## What to Check
- Use-of-proceeds clarity  
- Credible KPIs and baseline  
- Duration vs. rate path

**Related reading:**  
- [Rising Inflation and Its Impact on Emerging Markets](https://spherevista360.com/global-inflation-2025/)  
- [US–India Trade Relations: A New Era of Cooperation](https://spherevista360.com/us-india-trade-2025/)
"""),

# =========================
# Technology (3)
# =========================
"Technology/01-on-device-ai-vs-cloud-2025.md": md("""\
---
title: "On-Device AI vs Cloud AI: Where Each Wins in 2025"
excerpt: "Latency, privacy, and cost decide the architecture. Here’s how teams split workloads today."
category: "Technology"
tags: ["AI", "Edge", "Cloud", "Latency"]
seo_title: "On-Device vs Cloud AI (2025): A Practical Architecture Guide"
seo_description: "Choose the right balance between on-device and cloud AI in 2025—latency, privacy, and total cost considerations."
publish: true
image: "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Smartphone chip and cloud icon – Technology"
---

Inference is shifting. Lightweight models run locally for speed and privacy; heavier tasks still live in the cloud.
A hybrid pattern—edge pre-processing + cloud refinement—often wins.

## Decision Checklist
- **Latency budget**  
- **Privacy constraints**  
- **Battery/thermal limits**  
- **Unit economics**

**Related reading:**  
- [The Cloud Wars of 2025: AWS vs Azure vs Google Cloud](https://spherevista360.com/cloud-wars-2025/)  
- [Top Generative AI Tools 2025](https://spherevista360.com/generative-ai-tools-2025/)
"""),

"Technology/02-open-source-models-enterprise-2025.md": md("""\
---
title: "Open-Source AI Models in the Enterprise: Build, Buy, or Blend?"
excerpt: "Security and flexibility make OSS attractive—if you plan MLOps and governance early."
category: "Technology"
tags: ["Open source", "AI", "MLOps", "Security"]
seo_title: "Open-Source AI in 2025: Security, Cost, and Control"
seo_description: "How enterprises evaluate open-source AI models in 2025—licensing, compliance, MLOps, and hybrid strategies."
publish: true
image: "https://images.unsplash.com/photo-1556075798-4825dfaaf498?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Developer terminal and model weights diagram – Technology"
---

Open models reduce vendor risk and can lower inference costs. The trade-off is owning updates, evals, and safety tuning.
Many teams blend OSS for core tasks with a managed API for spiky workloads.

## What to Plan
- License scope and data policy  
- Eval harness and red-teaming  
- Observability and rollback

**Related reading:**  
- [AI Cybersecurity 2025: Automation for Defense](https://spherevista360.com/ai-cybersecurity-automation/)  
- [Startup Funding 2025: What Investors Want](https://spherevista360.com/startup-funding-2025/)
"""),

"Technology/03-product-analytics-2025-roadmap.md": md("""\
---
title: "Product Analytics in 2025: From Dashboards to Decisions"
excerpt: "Beyond vanity metrics—teams wire analytics to experiments and roadmaps."
category: "Technology"
tags: ["Analytics", "A/B testing", "Growth"]
seo_title: "Product Analytics 2025: Experiments, Models, Action"
seo_description: "A pragmatic guide to product analytics in 2025—data quality, experimentation, and making decisions faster."
publish: true
image: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Dashboard showing product KPIs – Technology"
---

Dashboards don’t move needles—decisions do. Modern stacks connect events to experiments and roadmaps.
Quality > quantity: track fewer, better metrics and wire them to action.

## Essentials
- Clear event taxonomy  
- Guardrail metrics  
- Experiment review cadence

**Related reading:**  
- [Open-Source AI Models in the Enterprise](https://spherevista360.com/open-source-models-2025/)  
- [Startup Funding 2025: What Investors Want](https://spherevista360.com/startup-funding-2025/)
"""),

# =========================
# World (2)
# =========================
"World/01-supply-chain-reshoring-2025.md": md("""\
---
title: "Reshoring 2.0: How Supply Chains Are Really Changing in 2025"
excerpt: "Friend-shoring, dual sourcing, and regional hubs—what actually stuck after the shocks."
category: "World"
tags: ["Supply chain", "Manufacturing", "Trade"]
seo_title: "Supply Chains 2025: Reshoring, Hubs, and Risk"
seo_description: "A clear look at how global supply chains evolved in 2025—regional hubs, dual sourcing, and real risk reduction."
publish: true
image: "https://images.unsplash.com/photo-1517959105821-eaf2591984dd?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Container port and logistics cranes – World"
---

Companies are keeping buffers and building regional hubs. Critical inputs get dual sources; software replaces spreadsheets.
The winners invest in visibility and scenario planning.

## What’s Working
- Near-shoring for time-sensitive goods  
- Inventory tiers for resilience  
- Shared data across partners

**Related reading:**  
- [US–India Trade Relations](https://spherevista360.com/us-india-trade-2025/)  
- [Global Elections 2025](https://spherevista360.com/global-elections-2025/)
"""),

"World/02-digital-identity-cross-border-2025.md": md("""\
---
title: "Digital Identity Goes Global: Cross-Border Logins and Payments"
excerpt: "eID, passkeys, and KYC sharing promise fewer forms and faster onboarding."
category: "World"
tags: ["Digital identity", "Payments", "Policy"]
seo_title: "Digital Identity 2025: eID, Passkeys, and Fintech Onboarding"
seo_description: "How digital identity and passkeys change travel, banking, and cross-border apps in 2025."
publish: true
image: "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Passport with smartphone authentication – World"
---

Cross-border identity is getting simpler. Passkeys reduce phishing; verified credentials speed remote onboarding.
Privacy rules differ—apps must design for regional compliance.

## Watchpoints
- Data minimization  
- Revocation and recovery  
- Interop with banks and telcos

**Related reading:**  
- [Visa-Free Destinations for 2025 Travelers](https://spherevista360.com/visa-free-destinations-2025/)  
- [Digital Banking Revolution](https://spherevista360.com/digital-banking-2025/)
"""),

# =========================
# Travel (1)
# =========================
"Travel/01-smart-itineraries-ai-2025.md": md("""\
---
title: "Smart Itineraries with AI: Plan Trips in Hours, Not Weeks"
excerpt: "Use AI to plan routes, book smarter, and avoid tourist traps in 2025."
category: "Travel"
tags: ["Travel planning", "AI", "Itinerary"]
seo_title: "AI Travel Planning 2025: Faster, Cheaper, Smarter"
seo_description: "Plan smarter trips with AI in 2025—routes, budgets, and local finds without the overwhelm."
publish: true
image: "https://images.unsplash.com/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Traveler planning route on a map with phone – Travel"
---

Trip planning can be fun again. AI helps you sequence cities, optimize budgets, and avoid crowds—then export to maps.
Keep room for spontaneity: lock anchors (flights, hotels) and leave gaps.

## Quick Wins
- Pre-tag must-sees  
- Group by neighborhoods  
- Book transport early, food late

**Related reading:**  
- [Digital Nomad Visas 2025](https://spherevista360.com/digital-nomad-visas-2025/)  
- [Visa-Free Destinations 2025](https://spherevista360.com/visa-free-destinations-2025/)
"""),

# =========================
# Politics (1)
# =========================
"Politics/01-ai-regulation-speech-safety-2025.md": md("""\
---
title: "AI, Speech, and Safety: What Regulation Is Aiming for in 2025"
excerpt: "Lawmakers target transparency, attribution, and accountability—without stifling innovation."
category: "Politics"
tags: ["AI policy", "Regulation", "Governance"]
seo_title: "AI Regulation 2025: Transparency, Safety, and Innovation"
seo_description: "A level-headed guide to AI regulation in 2025—what governments want and what developers should prepare for."
publish: true
image: "https://images.unsplash.com/photo-1555371363-3bc9f2d9ea9f?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Government building with digital overlay – Politics"
---

Policies are converging on a few ideas: model transparency, provenance for media, and stronger accountability for harms.
Expect obligations to scale with risk and deployment reach.

## For Builders
- Document data use and limits  
- Plan red-team & evals  
- Support content authenticity standards

**Related reading:**  
- [How AI Is Influencing Modern Politics](https://spherevista360.com/ai-in-politics/)  
- [AI Cybersecurity 2025](https://spherevista360.com/ai-cybersecurity-automation/)
"""),

# =========================
# Entertainment (2)
# =========================
"Entertainment/01-ai-in-hollywood-vfx-2025.md": md("""\
---
title: "Hollywood’s AI Moment: How VFX Pipelines Are Changing"
excerpt: "From rotoscoping to crowd scenes, AI is speeding up the slowest parts of production."
category: "Entertainment"
tags: ["VFX", "AI", "Film tech"]
seo_title: "AI in Hollywood 2025: Faster VFX and New Workflows"
seo_description: "A practical look at how AI is reshaping visual effects and post-production in Hollywood."
publish: true
image: "https://images.unsplash.com/photo-1478720568477-152d9b164e26?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Film set with green screen and lights – Entertainment"
---

Studios are using AI to accelerate tedious VFX steps. Artists focus more on look-dev and story while tools handle masks and fills.
The bottleneck shifts to review and integration—not hand work.

## Implications
- Faster iterations  
- Smaller teams, deeper specialization  
- New roles for tool orchestration

**Related reading:**  
- [On-Device AI vs Cloud AI](https://spherevista360.com/on-device-vs-cloud-ai-2025/)  
- [Open-Source AI in the Enterprise](https://spherevista360.com/open-source-models-2025/)
"""),

"Entertainment/02-streaming-personalization-ai-2025.md": md("""\
---
title: "Streaming Gets Personal: How AI Recommenders Shape What You Watch"
excerpt: "From cold starts to mood mixes—why your home page finally feels relevant."
category: "Entertainment"
tags: ["Streaming", "Recommenders", "Music", "OTT"]
seo_title: "AI Recommenders 2025: Smarter Streaming for Movies and Music"
seo_description: "Understand modern recommenders in streaming—signals, evaluation, and how discovery is changing in 2025."
publish: true
image: "https://images.unsplash.com/photo-1519474187921-36ba4c76a2f7?auto=format&fit=crop&w=800&h=500&q=80"
alt: "TV streaming interface with recommendations – Entertainment"
---

Recommenders are getting context-aware and multi-objective. Cold starts shrink with graph signals; mood mixes keep sessions going.
Artists and studios win when discovery is fair and transparent.

## What’s New
- Session-based models  
- Diversity/novelty tuning  
- Better evals beyond clicks

**Related reading:**  
- [Product Analytics in 2025](https://spherevista360.com/product-analytics-2025/)  
- [On-Device AI vs Cloud AI](https://spherevista360.com/on-device-vs-cloud-ai-2025/)
"""),

# =========================
# Business (1)
# =========================
"Business/01-ops-automation-copilots-2025.md": md("""\
---
title: "Ops Copilots: Automating the Unsexy Work That Scales Businesses"
excerpt: "From finance closes to vendor intake—copilots are eating back-office toil."
category: "Business"
tags: ["Automation", "Operations", "Copilots"]
seo_title: "Ops Automation 2025: Copilots for Finance, HR, and IT"
seo_description: "Where automation copilots deliver ROI in 2025—finance closes, employee onboarding, and vendor workflows."
publish: true
image: "https://images.unsplash.com/photo-1504384764586-bb4cdc1707b0?auto=format&fit=crop&w=800&h=500&q=80"
alt: "Business team using laptops with AI assistant – Business"
---

The ROI is hiding in ops. Copilots speed closings, vendor checks, and onboarding by turning checklists into workflows.
Start with one lane, measure cycle time, and expand.

## Playbook
- Map steps and owners  
- Automate approvals  
- Track time-to-done monthly

**Related reading:**  
- [Open-Source AI in the Enterprise](https://spherevista360.com/open-source-models-2025/)  
- [Product Analytics in 2025](https://spherevista360.com/product-analytics-2025/)
"""),
}

# Write files
for rel_path, content in POSTS.items():
    (BASE_DIR / rel_path).write_text(content, encoding="utf-8")

# Zip the folder tree
zip_path = Path("spherevista360_week2_final.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in BASE_DIR.rglob("*"):
        zf.write(p, p.relative_to(BASE_DIR))

print(f"✅ Created {zip_path.resolve()}")
