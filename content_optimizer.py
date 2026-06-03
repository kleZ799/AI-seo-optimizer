"""
Content Optimizer Module
------------------------
Scores existing content against SEO best-practices and returns actionable
recommendations powered by Claude.
"""

import json
import re
import streamlit as st
from .llm_client import ask_claude


SYSTEM = (
    "You are a senior on-page SEO consultant. "
    "Return ONLY valid JSON – no markdown, no extra commentary."
)


def _parse_json(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw)


def _score_bar(label: str, score: int):
    pct = min(max(score, 0), 100)
    st.markdown(f"""
<div class="score-bar-wrap">
  <div class="score-label">{label} <strong style="color:#818cf8">{score}/100</strong></div>
  <div class="score-bar-bg"><div class="score-bar-fill" style="width:{pct}%"></div></div>
</div>""", unsafe_allow_html=True)


def render(api_key: str):
    st.markdown("## ✍️ Content Optimizer")
    st.markdown("Paste your content and target keyword — Claude will score it and give you a prioritised fix list.")

    target_kw = st.text_input("Target keyword", placeholder="e.g. best noise-cancelling headphones 2025")
    content = st.text_area("Your content (paste the full article or section)", height=280,
                           placeholder="Paste your draft article here…")

    if st.button("🚀 Optimize Content", use_container_width=True):
        if not content.strip():
            st.warning("Please paste some content first.")
            return
        with st.spinner("Running deep SEO analysis…"):
            prompt = f"""
Analyse this content for SEO optimisation against the target keyword "{target_kw}".

CONTENT:
\"\"\"
{content[:4000]}
\"\"\"

Return JSON with this exact shape:
{{
  "scores": {{
    "overall": 0-100,
    "keyword_usage": 0-100,
    "readability": 0-100,
    "structure": 0-100,
    "uniqueness": 0-100
  }},
  "critical_fixes": ["...", "..."],
  "recommended_improvements": ["...", "..."],
  "quick_wins": ["...", "..."],
  "optimised_intro": "Rewritten first paragraph optimised for the keyword",
  "suggested_headings": ["H2: ...", "H2: ...", "H3: ..."],
  "semantic_keywords_to_add": ["...", "..."]
}}
"""
            try:
                raw = ask_claude(api_key, prompt, system=SYSTEM, max_tokens=2000)
                data = _parse_json(raw)
            except Exception as e:
                st.error(f"API error: {e}")
                return

        scores = data.get("scores", {})

        st.markdown("### 📊 SEO Scores")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        for col, (label, key) in zip([c1, c2, c3, c4, c5], [
            ("Overall", "overall"), ("Keyword", "keyword_usage"),
            ("Readability", "readability"), ("Structure", "structure"), ("Uniqueness", "uniqueness")
        ]):
            v = scores.get(key, 0)
            col.markdown(f'<div class="metric-card"><div class="metric-value">{v}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["🔴 Critical Fixes", "🟡 Improvements", "🟢 Quick Wins", "✨ Rewrites"])

        with tab1:
            items = "".join(f'<div class="suggestion-item error">🔴 {x}</div>' for x in data.get("critical_fixes", []))
            st.markdown(f'<div class="section-card">{items or "<p style=\'color:#64748b\'>No critical issues found!</p>"}</div>', unsafe_allow_html=True)

        with tab2:
            items = "".join(f'<div class="suggestion-item warning">🟡 {x}</div>' for x in data.get("recommended_improvements", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab3:
            items = "".join(f'<div class="suggestion-item success">🟢 {x}</div>' for x in data.get("quick_wins", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown("**Optimised intro paragraph**")
            st.markdown(f'<div class="section-card"><p style="color:#cbd5e1;line-height:1.8">{data.get("optimised_intro","")}</p></div>', unsafe_allow_html=True)
            st.markdown("**Suggested heading structure**")
            headings = "".join(f'<div class="suggestion-item">{h}</div>' for h in data.get("suggested_headings", []))
            st.markdown(f'<div class="section-card">{headings}</div>', unsafe_allow_html=True)
            st.markdown("**Semantic keywords to sprinkle in**")
            pills = "".join(f'<span class="keyword-pill">{k}</span>' for k in data.get("semantic_keywords_to_add", []))
            st.markdown(f'<div class="section-card">{pills}</div>', unsafe_allow_html=True)
