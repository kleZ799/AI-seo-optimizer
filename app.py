import streamlit as st
import time
from modules import keyword_research, content_optimizer, serp_analyzer, site_auditor, meta_generator

st.set_page_config(
    page_title="AI SEO Optimizer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp { background: #0a0e1a; color: #e2e8f0; }

.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 40%, rgba(99,102,241,0.12) 0%, transparent 50%),
                radial-gradient(circle at 70% 60%, rgba(139,92,246,0.08) 0%, transparent 50%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
}
.hero-sub { color: #94a3b8; font-size: 1.05rem; margin: 0; }

.metric-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #6366f1; }
.metric-value { font-size: 2rem; font-weight: 700; color: #818cf8; }
.metric-label { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.2rem; }

.section-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #c7d2fe;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.keyword-pill {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    margin: 0.25rem;
    font-family: 'JetBrains Mono', monospace;
}

.score-bar-wrap { margin: 0.5rem 0; }
.score-label { font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.3rem; }
.score-bar-bg { background: #1e2535; border-radius: 999px; height: 8px; }
.score-bar-fill { height: 8px; border-radius: 999px; background: linear-gradient(90deg, #6366f1, #8b5cf6); }

.suggestion-item {
    background: #0f172a;
    border-left: 3px solid #6366f1;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: #cbd5e1;
}
.suggestion-item.warning { border-left-color: #f59e0b; }
.suggestion-item.success { border-left-color: #10b981; }
.suggestion-item.error   { border-left-color: #ef4444; }

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.6rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

div[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1f2937;
}

.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

hr { border-color: #1f2937 !important; }

.stSpinner > div { border-top-color: #6366f1 !important; }

[data-testid="stTab"] button { color: #94a3b8 !important; }
[data-testid="stTab"] button[aria-selected="true"] { color: #818cf8 !important; border-bottom-color: #6366f1 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1 class="hero-title">🔍 AI SEO Optimizer</h1>
  <p class="hero-sub">Keyword research · Content optimization · SERP analysis · Site audits — all powered by LLMs</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    tool = st.radio("Select Tool", [
        "🔑 Keyword Research",
        "✍️ Content Optimizer",
        "📊 SERP Analyzer",
        "🏗️ Site Auditor",
        "🏷️ Meta Tag Generator",
    ])
    st.markdown("---")
    st.markdown("<small style='color:#475569'>AI SEO Tool · Built with Streamlit + Claude</small>", unsafe_allow_html=True)

if not api_key:
    st.info("👈 Enter your Anthropic API key in the sidebar to get started.")
    st.stop()

# ── Tool Router ───────────────────────────────────────────────────────────────
if tool == "🔑 Keyword Research":
    keyword_research.render(api_key)
elif tool == "✍️ Content Optimizer":
    content_optimizer.render(api_key)
elif tool == "📊 SERP Analyzer":
    serp_analyzer.render(api_key)
elif tool == "🏗️ Site Auditor":
    site_auditor.render(api_key)
elif tool == "🏷️ Meta Tag Generator":
    meta_generator.render(api_key)
