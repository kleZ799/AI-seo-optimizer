"""
SERP Analyzer Module
--------------------
Analyses competitive SERP landscape for a keyword using Claude's knowledge.
Gives insight into content type, SERP features, and ranking strategies.
"""

import json
import re
import streamlit as st
from .llm_client import ask_claude


SYSTEM = (
    "You are an expert SERP analyst with deep knowledge of Google search behaviour. "
    "Return ONLY valid JSON – no markdown fences, no extra text."
)


def _parse_json(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw)


def render(api_key: str):
    st.markdown("## 📊 SERP Analyzer")
    st.markdown("Analyse the competitive landscape for any keyword and understand what it takes to rank on page one.")

    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("Keyword to analyse", placeholder="e.g. best project management software")
    with col2:
        intent_filter = st.selectbox("Search intent", ["Any", "Informational", "Commercial", "Transactional"])

    if st.button("📡 Analyse SERP", use_container_width=True):
        if not keyword.strip():
            st.warning("Enter a keyword first.")
            return
        with st.spinner("Mapping the SERP landscape…"):
            prompt = f"""
Perform a detailed SERP analysis for the keyword: "{keyword}"
Intent context: {intent_filter}

Return JSON with this exact structure:
{{
  "keyword": "{keyword}",
  "estimated_difficulty": 1-100,
  "search_intent": "informational|commercial|transactional|navigational",
  "serp_features": ["Featured Snippet", "People Also Ask", "Video Carousel", ...],
  "dominant_content_types": ["long-form guide", "listicle", "product page", ...],
  "top_ranking_factors": ["...", "..."],
  "content_recommendations": {{
    "ideal_word_count": 1000,
    "must_cover_topics": ["...", "..."],
    "content_angle": "...",
    "cta_suggestion": "..."
  }},
  "competitor_weaknesses": ["...", "..."],
  "ranking_strategy": "3-4 sentence actionable strategy to rank for this keyword"
}}
"""
            try:
                raw = ask_claude(api_key, prompt, system=SYSTEM, max_tokens=1800)
                data = _parse_json(raw)
            except Exception as e:
                st.error(f"API error: {e}")
                return

        diff = data.get("estimated_difficulty", 50)
        diff_color = "#10b981" if diff < 35 else "#f59e0b" if diff < 65 else "#ef4444"
        diff_label = "Easy" if diff < 35 else "Medium" if diff < 65 else "Hard"

        # Header metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{diff_color}">{diff}</div><div class="metric-label">Difficulty</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.2rem">{diff_label}</div><div class="metric-label">Competition</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1rem">{data.get("search_intent","").title()}</div><div class="metric-label">Intent</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card"><div class="metric-value">{data.get("content_recommendations",{}).get("ideal_word_count","N/A")}</div><div class="metric-label">Ideal Words</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Strategy
        st.markdown("### 🎯 Ranking Strategy")
        st.markdown(f'<div class="section-card"><p style="color:#cbd5e1;line-height:1.8">{data.get("ranking_strategy","")}</p></div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["SERP Landscape", "Content Blueprint", "Competitor Gaps"])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**SERP Features present**")
                items = "".join(f'<div class="suggestion-item">📌 {f}</div>' for f in data.get("serp_features", []))
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown("**Dominant content types**")
                items = "".join(f'<div class="suggestion-item">📄 {t}</div>' for t in data.get("dominant_content_types", []))
                st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

            st.markdown("**Key ranking factors**")
            items = "".join(f'<div class="suggestion-item success">✅ {f}</div>' for f in data.get("top_ranking_factors", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab2:
            cr = data.get("content_recommendations", {})
            st.markdown(f"""
<div class="section-card">
  <div class="section-title">📐 Content Blueprint</div>
  <p><strong style="color:#818cf8">Angle:</strong> <span style="color:#cbd5e1">{cr.get("content_angle","")}</span></p>
  <p><strong style="color:#818cf8">CTA:</strong> <span style="color:#cbd5e1">{cr.get("cta_suggestion","")}</span></p>
  <p><strong style="color:#818cf8">Word count:</strong> <span style="color:#cbd5e1">{cr.get("ideal_word_count","")} words</span></p>
</div>""", unsafe_allow_html=True)
            st.markdown("**Topics you must cover**")
            items = "".join(f'<div class="suggestion-item">📝 {t}</div>' for t in cr.get("must_cover_topics", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab3:
            items = "".join(f'<div class="suggestion-item warning">⚡ {g}</div>' for g in data.get("competitor_weaknesses", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)