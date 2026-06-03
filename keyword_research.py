"""
Keyword Research Module
-----------------------
Uses Claude to generate keyword clusters, intent labels, difficulty estimates,
and related long-tail phrases for any seed topic.
"""

import json
import re
import streamlit as st
from .llm_client import ask_claude


SYSTEM = (
    "You are an expert SEO strategist specialising in keyword research. "
    "Return ONLY valid JSON – no markdown fences, no extra text."
)


def _parse_json(raw: str) -> dict | list:
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw)


def render(api_key: str):
    st.markdown("## 🔑 Keyword Research")
    st.markdown("Enter a seed topic and Claude will surface keyword clusters, intent, estimated difficulty, and long-tail ideas.")

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Seed topic / niche", placeholder="e.g. sustainable fashion for beginners")
    with col2:
        country = st.selectbox("Target market", ["Global", "US", "UK", "IN", "CA", "AU"])

    if st.button("🔍 Research Keywords", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic first.")
            return
        with st.spinner("Analysing keyword landscape with AI…"):
            prompt = f"""
You are performing keyword research for the topic: "{topic}" in the market: "{country}".

Return a JSON object with this exact shape:
{{
  "primary_keywords": [
    {{"keyword": "...", "intent": "informational|commercial|transactional|navigational", "difficulty": 1-100, "monthly_searches": "low|medium|high"}}
  ],
  "long_tail_keywords": ["...", "..."],
  "lsi_keywords": ["...", "..."],
  "questions_to_answer": ["...", "..."],
  "content_gaps": ["...", "..."],
  "seo_summary": "2-3 sentence strategic overview"
}}

Generate 8 primary keywords, 10 long-tail phrases, 8 LSI terms, 6 questions, 4 content gaps.
"""
            try:
                raw = ask_claude(api_key, prompt, system=SYSTEM, max_tokens=2000)
                data = _parse_json(raw)
            except Exception as e:
                st.error(f"API error: {e}")
                return

        # ── Display results ──────────────────────────────────────────────
        st.markdown("### 📈 Strategic Overview")
        st.markdown(f"""<div class="section-card"><p style="color:#cbd5e1;line-height:1.7">{data.get("seo_summary", "")}</p></div>""", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["Primary Keywords", "Long-Tail & LSI", "Questions", "Content Gaps"])

        with tab1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            for kw in data.get("primary_keywords", []):
                diff = kw.get("difficulty", 50)
                color = "#10b981" if diff < 35 else "#f59e0b" if diff < 65 else "#ef4444"
                vol_badge = {"low": "🔵", "medium": "🟡", "high": "🟢"}.get(kw.get("monthly_searches", ""), "⚪")
                st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
     background:#0f172a;border-radius:10px;padding:0.8rem 1.2rem;margin:0.4rem 0;
     border:1px solid #1e293b">
  <span style="font-family:'JetBrains Mono',monospace;color:#a5b4fc;font-size:0.9rem">{kw.get("keyword","")}</span>
  <span style="font-size:0.78rem;color:#64748b">{kw.get("intent","").upper()} &nbsp;·&nbsp; {vol_badge} Volume &nbsp;·&nbsp;
    <span style="color:{color}">Difficulty {diff}</span></span>
</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Long-tail phrases**")
                pills = "".join(f'<span class="keyword-pill">{k}</span>' for k in data.get("long_tail_keywords", []))
                st.markdown(f'<div class="section-card">{pills}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown("**LSI / Semantic keywords**")
                pills = "".join(f'<span class="keyword-pill">{k}</span>' for k in data.get("lsi_keywords", []))
                st.markdown(f'<div class="section-card">{pills}</div>', unsafe_allow_html=True)

        with tab3:
            items = "".join(f'<div class="suggestion-item">❓ {q}</div>' for q in data.get("questions_to_answer", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)

        with tab4:
            items = "".join(f'<div class="suggestion-item warning">⚠️ {g}</div>' for g in data.get("content_gaps", []))
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)
