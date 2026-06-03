"""
Meta Tag Generator Module
--------------------------
Generates optimised title tags, meta descriptions, Open Graph tags,
Twitter Card tags, and structured data snippets.
"""

import json
import re
import streamlit as st
from .llm_client import ask_claude


SYSTEM = (
    "You are an expert SEO copywriter specialising in meta tags and structured data. "
    "Return ONLY valid JSON – no markdown fences, no extra text."
)


def _parse_json(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw)


def render(api_key: str):
    st.markdown("## 🏷️ Meta Tag Generator")
    st.markdown("Describe your page and Claude will write perfectly optimised meta tags, Open Graph, and Schema markup.")

    col1, col2 = st.columns(2)
    with col1:
        page_topic = st.text_input("Page topic / title", placeholder="e.g. Complete Guide to Plant-Based Protein Sources")
        target_kw  = st.text_input("Primary keyword", placeholder="e.g. plant-based protein")
    with col2:
        page_type  = st.selectbox("Page type", ["Blog Post / Article", "Product Page", "Category Page", "Homepage", "Landing Page", "FAQ Page"])
        brand_name = st.text_input("Brand / site name", placeholder="e.g. NutriWorld")

    description = st.text_area("Brief description of the page (2-3 sentences)", height=100,
                               placeholder="What is this page about? Who is it for? What value does it deliver?")

    if st.button("🏷️ Generate Meta Tags", use_container_width=True):
        if not page_topic.strip():
            st.warning("Please enter a page topic.")
            return
        with st.spinner("Crafting perfect meta tags…"):
            prompt = f"""
Generate SEO-optimised meta tags for:
- Page topic: {page_topic}
- Primary keyword: {target_kw}
- Page type: {page_type}
- Brand: {brand_name}
- Description: {description}

Return JSON with this exact shape:
{{
  "title_tags": [
    {{"version": "Primary", "text": "...", "length": 55, "note": "..."}},
    {{"version": "Alternative A", "text": "...", "length": 58, "note": "..."}},
    {{"version": "Alternative B", "text": "...", "length": 52, "note": "..."}}
  ],
  "meta_descriptions": [
    {{"version": "Primary", "text": "...", "length": 155, "note": "..."}},
    {{"version": "Alternative", "text": "...", "length": 150, "note": "..."}}
  ],
  "open_graph": {{
    "og:title": "...",
    "og:description": "...",
    "og:type": "article|product|website",
    "og:image_suggestion": "describe ideal image"
  }},
  "twitter_card": {{
    "twitter:card": "summary_large_image",
    "twitter:title": "...",
    "twitter:description": "..."
  }},
  "schema_markup": {{
    "@context": "https://schema.org",
    "@type": "...",
    "headline": "...",
    "description": "...",
    "author": {{"@type": "Organization", "name": "{brand_name}"}}
  }},
  "tips": ["...", "..."]
}}
"""
            try:
                raw = ask_claude(api_key, prompt, system=SYSTEM, max_tokens=2000)
                data = _parse_json(raw)
            except Exception as e:
                st.error(f"API error: {e}")
                return

        tab1, tab2, tab3, tab4 = st.tabs(["Title & Meta", "Open Graph", "Twitter Card", "Schema Markup"])

        with tab1:
            st.markdown("**🔤 Title Tag Options**")
            for t in data.get("title_tags", []):
                length = t.get("length", len(t.get("text", "")))
                lcolor = "#10b981" if 50 <= length <= 60 else "#f59e0b"
                st.markdown(f"""
<div class="section-card" style="margin-bottom:0.8rem">
  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem">
    <strong style="color:#818cf8">{t.get("version","")}</strong>
    <span style="color:{lcolor};font-size:0.8rem">{length} chars</span>
  </div>
  <code style="font-size:0.95rem;color:#e2e8f0;background:#0f172a;padding:0.6rem 1rem;border-radius:8px;display:block">{t.get("text","")}</code>
  <p style="color:#64748b;font-size:0.8rem;margin-top:0.5rem">{t.get("note","")}</p>
</div>""", unsafe_allow_html=True)

            st.markdown("**📝 Meta Description Options**")
            for m in data.get("meta_descriptions", []):
                length = m.get("length", len(m.get("text", "")))
                lcolor = "#10b981" if 140 <= length <= 160 else "#f59e0b"
                st.markdown(f"""
<div class="section-card" style="margin-bottom:0.8rem">
  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem">
    <strong style="color:#818cf8">{m.get("version","")}</strong>
    <span style="color:{lcolor};font-size:0.8rem">{length} chars</span>
  </div>
  <code style="font-size:0.9rem;color:#e2e8f0;background:#0f172a;padding:0.6rem 1rem;border-radius:8px;display:block">{m.get("text","")}</code>
  <p style="color:#64748b;font-size:0.8rem;margin-top:0.5rem">{m.get("note","")}</p>
</div>""", unsafe_allow_html=True)

        with tab2:
            og = data.get("open_graph", {})
            html_block = "\n".join(f'<meta property="{k}" content="{v}" />' for k, v in og.items() if k != "og:image_suggestion")
            st.markdown(f'<div class="section-card"><code style="color:#a5b4fc;font-size:0.85rem;white-space:pre-wrap;display:block">{html_block}</code></div>', unsafe_allow_html=True)
            if og.get("og:image_suggestion"):
                st.info(f"💡 Ideal OG image: {og['og:image_suggestion']}")

        with tab3:
            tw = data.get("twitter_card", {})
            html_block = "\n".join(f'<meta name="{k}" content="{v}" />' for k, v in tw.items())
            st.markdown(f'<div class="section-card"><code style="color:#a5b4fc;font-size:0.85rem;white-space:pre-wrap;display:block">{html_block}</code></div>', unsafe_allow_html=True)

        with tab4:
            schema = data.get("schema_markup", {})
            schema_str = json.dumps(schema, indent=2)
            st.markdown(f'<div class="section-card"><code style="color:#a5b4fc;font-size:0.82rem;white-space:pre-wrap;display:block">{schema_str}</code></div>', unsafe_allow_html=True)
            st.caption("Copy this into a <script type=\"application/ld+json\"> tag in your page's <head>.")

        if data.get("tips"):
            st.markdown("### 💡 Pro Tips")
            items = "".join(f'<div class="suggestion-item success">💡 {t}</div>' for t in data["tips"])
            st.markdown(f'<div class="section-card">{items}</div>', unsafe_allow_html=True)
