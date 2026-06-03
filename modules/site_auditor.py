"""
Site Auditor Module
-------------------
Performs a technical SEO audit by fetching a URL's HTML and running
structural checks + AI analysis.
"""

import re
import json
import requests
from bs4 import BeautifulSoup
import streamlit as st
from .llm_client import ask_claude


SYSTEM = (
    "You are a technical SEO auditor. "
    "Return ONLY valid JSON – no markdown fences, no extra text."
)


def _fetch_page(url: str) -> tuple[str, dict]:
    """Fetch a page and extract basic SEO signals."""
    headers = {"User-Agent": "Mozilla/5.0 (SEO-Audit-Bot/1.0)"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.find("title")
    desc  = soup.find("meta", attrs={"name": "description"})
    h1s   = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s   = [h.get_text(strip=True) for h in soup.find_all("h2")]
    imgs  = soup.find_all("img")
    links = soup.find_all("a", href=True)
    word_count = len(soup.get_text().split())
    canonical = soup.find("link", rel="canonical")
    robots = soup.find("meta", attrs={"name": "robots"})

    signals = {
        "title": title.get_text(strip=True) if title else None,
        "title_length": len(title.get_text(strip=True)) if title else 0,
        "meta_description": desc["content"] if desc else None,
        "meta_description_length": len(desc["content"]) if desc else 0,
        "h1_count": len(h1s),
        "h1_texts": h1s[:3],
        "h2_count": len(h2s),
        "h2_samples": h2s[:5],
        "word_count": word_count,
        "total_images": len(imgs),
        "images_missing_alt": sum(1 for img in imgs if not img.get("alt")),
        "internal_links": sum(1 for a in links if url.split("/")[2] in a["href"] or a["href"].startswith("/")),
        "external_links": sum(1 for a in links if a["href"].startswith("http") and url.split("/")[2] not in a["href"]),
        "canonical_url": canonical["href"] if canonical else None,
        "robots_directive": robots["content"] if robots else None,
        "status_code": resp.status_code,
        "page_size_kb": round(len(resp.content) / 1024, 1),
    }
    return resp.text[:2000], signals


def _parse_json(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw)


def render(api_key: str):
    st.markdown("## 🏗️ Site Auditor")
    st.markdown("Enter any live URL and get a full technical SEO audit in seconds.")

    url = st.text_input("URL to audit", placeholder="https://example.com/blog/my-article")

    if st.button("🔬 Run Site Audit", use_container_width=True):
        if not url.strip():
            st.warning("Please enter a URL.")
            return
        if not url.startswith("http"):
            url = "https://" + url

        with st.spinner("Fetching page and running technical checks…"):
            try:
                snippet, signals = _fetch_page(url)
            except Exception as e:
                st.error(f"Could not fetch page: {e}")
                return

        with st.spinner("Running AI analysis on audit data…"):
            prompt = f"""
Perform a technical SEO audit based on these extracted page signals:
{json.dumps(signals, indent=2)}

And this content snippet:
{snippet[:1500]}

Return JSON with this exact shape:
{{
  "overall_score": 0-100,
  "issues": {{
    "critical": ["...", "..."],
    "warnings":  ["...", "..."],
    "passed":    ["...", "..."]
  }},
  "quick_fixes": ["...", "..."],
  "technical_recommendations": ["...", "..."],
  "content_observations": ["...", "..."],
  "audit_summary": "3-sentence executive summary"
}}
"""
            try:
                raw = ask_claude(api_key, prompt, system=SYSTEM, max_tokens=2000)
                data = _parse_json(raw)
            except Exception as e:
                st.error(f"AI analysis error: {e}")
                return

        # ── Render ────────────────────────────────────────────────────────
        overall = data.get("overall_score", 0)
        score_color = "#10b981" if overall >= 70 else "#f59e0b" if overall >= 45 else "#ef4444"

        col_metrics = st.columns(5)
        metric_data = [
            ("SEO Score", f"{overall}/100", score_color),
            ("Word Count", signals["word_count"], "#818cf8"),
            ("Images w/o Alt", signals["images_missing_alt"], "#ef4444" if signals["images_missing_alt"] > 0 else "#10b981"),
            ("H1 Tags", signals["h1_count"], "#818cf8"),
            ("Page Size", f"{signals['page_size_kb']} KB", "#818cf8"),
        ]
        for col, (label, val, color) in zip(col_metrics, metric_data):
            col.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{color};font-size:1.5rem">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Executive Summary")
        st.markdown(f'<div class="section-card"><p style="color:#cbd5e1;line-height:1.8">{data.get("audit_summary","")}</p></div>', unsafe_allow_html=True)

        # Raw signals expander
        with st.expander("🔎 Raw extracted signals"):
            st.json(signals)

        tab1, tab2, tab3 = st.tabs(["Issues & Passes", "Recommendations", "Content Notes"])

        with tab1:
            issues = data.get("issues", {})
            c1, c2 = st.columns(2)
            with c1:
                crit = issues.get("critical", [])
                st.markdown(f"**🔴 Critical issues ({len(crit)})**")
                items = "".join(f'<div class="suggestion-item error">🔴 {x}</div>' for x in crit) or '<div class="suggestion-item success">None! Great work.</div>'
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

                warn = issues.get("warnings", [])
                st.markdown(f"**🟡 Warnings ({len(warn)})**")
                items = "".join(f'<div class="suggestion-item warning">🟡 {x}</div>' for x in warn)
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)
            with c2:
                passed = issues.get("passed", [])
                st.markdown(f"**🟢 Passed checks ({len(passed)})**")
                items = "".join(f'<div class="suggestion-item success">✅ {x}</div>' for x in passed)
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**⚡ Quick Fixes**")
                items = "".join(f'<div class="suggestion-item">⚡ {x}</div>' for x in data.get("quick_fixes", []))
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown("**🛠 Technical Recommendations**")
                items = "".join(f'<div class="suggestion-item">🛠 {x}</div>' for x in data.get("technical_recommendations", []))
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab3:
            items = "".join(f'<div class="suggestion-item">📌 {x}</div>' for x in data.get("content_observations", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)
