# 🔍 AI-Powered SEO Optimization Tool

> AI-driven SEO research, content optimization, and site auditing — powered by Claude (Anthropic LLM) and built with Streamlit.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Anthropic](https://img.shields.io/badge/LLM-Claude%20(Anthropic)-blueviolet)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
(_Make sure you cross checck the repo before copying_)

---

## 📌 Project Overview

This tool automates the most time-consuming parts of SEO work by combining **Large Language Models (LLMs)** with structured HTML parsing and NLP analysis. It was built to demonstrate the practical application of AI APIs in a real-world productivity tool.

### What It Does

| Module | Description |
|--------|-------------|
| **Keyword Research** | AI-generated keyword clusters, search intent classification, difficulty estimates, long-tail phrases, and content gap analysis |
| **Content Optimizer** | Scores existing content on 5 SEO dimensions and returns prioritised fix lists with AI-rewritten sections |
| **SERP Analyzer** | Maps the competitive landscape for any keyword — content types, SERP features, word count targets, and ranking strategies |
**Site Auditor** | Fetches a live URL, extracts 15+ technical SEO signals, and generates a scored audit report with critical/warning/passed checks |
**Meta Tag Generator** | Produces title tags, meta descriptions, Open Graph, Twitter Card, and JSON-LD Schema markup — all optimised for the target keyword |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend / UI** | [Streamlit](https://streamlit.io) | Interactive web dashboard with real-time inputs and tabbed results |
| **LLM / AI** | [Anthropic Claude API](https://anthropic.com) | Natural language SEO analysis, structured JSON generation |
| **HTTP Requests** | `requests` | Fetching live web pages for the site auditor |
| **HTML Parsing** | `BeautifulSoup4` | Extracting title tags, headings, image alt attributes, links, etc. |
| **Data Handling** | Python `json`, `re` | Parsing Claude's structured JSON responses |
| **Language** | Python 3.10+ | Core application language |

---

## Architecture

```
seo-tool/
│
├── app.py                     # Main Streamlit entry point — routing, sidebar, CSS
│
└── modules/
    ├── __init__.py            # Package marker
    ├── llm_client.py          # Shared Claude API wrapper (ask_claude)
    ├── keyword_research.py    # Keyword Research module
    ├── content_optimizer.py   # Content Optimizer module
    ├── serp_analyzer.py       # SERP Analyzer module
    ├── site_auditor.py        # Site Auditor module (fetches live URLs)
    └── meta_generator.py      # Meta Tag Generator module
```

### How It Works (Flow)

```
User Input (Streamlit UI)
        │
        ▼
Module-specific prompt builder
        │
        ▼
ask_claude() → Anthropic /v1/messages API
        │
        ▼
Structured JSON response (Claude)
        │
        ▼
Parse + validate JSON
        │
        ▼
Render results in Streamlit tabs / cards
```

For the **Site Auditor**, there's a pre-step:
```
URL Input → requests.get() → BeautifulSoup parsing
         → 15 technical signals extracted
         → Signals sent to Claude for AI analysis
         → Scored report rendered
```

---

## ⚙️ How Each Module Works

### Keyword Research
Takes a seed topic and target market. Sends a structured prompt to Claude asking it to act as an SEO strategist. Claude returns a JSON object with primary keywords (each annotated with intent, difficulty 1-100, and volume tier), long-tail phrases, LSI/semantic keywords, "People Also Ask"-style questions, and content gap opportunities.

### Content Optimizer
Accepts raw article content and a target keyword. Claude analyses the text against five dimensions — overall SEO strength, keyword usage, readability, content structure, and uniqueness — scoring each 0-100. It then generates three tiers of recommendations (critical fixes, improvements, quick wins) plus a rewritten intro and suggested heading structure.

### SERP Analyzer
Takes a keyword and optional intent filter. Claude simulates the knowledge of an experienced SERP analyst, identifying what content types dominate the results, which SERP features are likely present (Featured Snippet, PAA, Video Carousel, etc.), top ranking factors, and a concrete ranking strategy. It also calculates an estimated difficulty score.

### Site Auditor
Fetches any live URL using `requests` with a browser-like user agent. `BeautifulSoup4` parses the HTML to extract: title tag, meta description, H1/H2 tags, image alt attributes, internal/external link counts, word count, canonical URL, robots meta directive, page size, and status code. These 15 signals are serialised to JSON and sent to Claude, which returns a scored audit (0-100) with issues classified as critical, warnings, or passed.

### Meta Tag Generator
Takes a page topic, keyword, page type, and brand name. Claude generates three title tag variants (all 50-60 chars), two meta description variants (all 140-160 chars), complete Open Graph tags, Twitter Card tags, and a JSON-LD Schema.org markup block appropriate for the page type.

---

## Quick Start (Run Locally)

### Prerequisites
- Python 3.10 or higher
- An [Anthropic API key](https://console.anthropic.com) (free tier available)
- Git installed

### Step-by-Step Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-seo-optimizer.git
cd ai-seo-optimizer
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

**5. Open in browser**  
Streamlit will automatically open `http://localhost:8501` in your browser.  
Paste your Anthropic API key in the sidebar and start using the tool.

---

## Getting an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Navigate to **API Keys** → **Create Key**
4. Copy the key (starts with `sk-ant-`)
5. Paste it into the sidebar of the running app

> **Note:** The key is never stored — it only lives in your browser session.

---

## Features at a Glance

- **Real-time AI analysis** — every result is generated live by Claude
- **Structured JSON responses** — Claude returns machine-parseable data, not free text
- **5 specialist modules** — each purpose-built for a different SEO workflow
- **Dark, professional UI** — custom CSS with Space Grotesk typography, gradient accents, and card layouts
- **Live site auditing** — fetches real pages, no mock data
- **Copy-ready outputs** — meta tags, schema markup, and headings are formatted to paste directly into your CMS

---

## Dependencies

```
streamlit>=1.35.0       # Web UI framework
anthropic>=0.28.0       # Official Anthropic Python SDK
requests>=2.31.0        # HTTP client for site auditor
beautifulsoup4>=4.12.0  # HTML parser for site auditor
```

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

## 👤 Author

Built by **Parth Bahadana** · [GitHub](https://github.com/kleZ799) · [LinkedIn](https://www.linkedin.com/in/parth-bhadana-530014202/)

> *Part of my AI/ML engineering portfolio demonstrating practical LLM integration, NLP pipelines, and full-stack Python development.*
