import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #080d18;
    --panel: rgba(17, 26, 44, 0.78);
    --panel-strong: rgba(21, 32, 53, 0.94);
    --line: rgba(157, 177, 211, 0.15);
    --text: #edf3ff;
    --muted: #91a0bb;
    --accent: #8b7cff;
    --accent-2: #41d9c4;
    --success: #53d6a2;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
.stApp {
    background:
      radial-gradient(ellipse 65% 45% at 8% -8%, rgba(111, 92, 255, .22), transparent 68%),
      radial-gradient(ellipse 55% 40% at 100% 12%, rgba(44, 213, 192, .11), transparent 68%),
      linear-gradient(145deg, #080d18 0%, #0b1220 55%, #080d18 100%);
    background-attachment: fixed;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.8rem 3rem 3rem;
    max-width: 1320px;
}
[data-testid="stAppViewContainer"] { background: transparent; }
[data-testid="stVerticalBlock"] { gap: 0.85rem; }

/* Hero */
.hero {
    text-align: center;
    padding: 2.7rem 0 1.9rem;
    position: relative;
}
.hero-eyebrow {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .72rem;
    font-weight: 500;
    letter-spacing: .16em;
    text-transform: uppercase;
    color: #bcb4ff;
    background: rgba(139, 124, 255, .11);
    border: 1px solid rgba(139, 124, 255, .25);
    border-radius: 999px;
    padding: .45rem .85rem;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.04;
    letter-spacing: -.055em;
    color: #f4f7ff;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(100deg, #a69bff 10%, #58e3d0 95%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero-sub {
    font-size: 1.02rem;
    font-weight: 400;
    color: #9eacc5;
    max-width: 610px;
    margin: 0 auto;
    line-height: 1.75;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,124,255,.5), rgba(65,217,196,.28), transparent);
    margin: 1.4rem 0 2rem;
}

/* Main cards */
.input-card {
    background: linear-gradient(145deg, rgba(22, 32, 53, .88), rgba(13, 21, 37, .84));
    border: 1px solid rgba(157, 177, 211, .18);
    border-radius: 22px;
    padding: 1.8rem 1.8rem 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 18px 60px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.035);
}
.stTextInput > label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .72rem !important;
    letter-spacing: .13em !important;
    text-transform: uppercase !important;
    color: #bcb4ff !important;
    font-weight: 500 !important;
    margin-bottom: .65rem !important;
}
.stTextInput > div > div > input {
    background: rgba(5, 11, 22, .72) !important;
    border: 1px solid rgba(157,177,211,.23) !important;
    border-radius: 12px !important;
    color: #f1f5ff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: .9rem 1rem !important;
    min-height: 3.15rem;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #9588ff !important;
    box-shadow: 0 0 0 3px rgba(139,124,255,.16) !important;
}
.stTextInput input::placeholder { color: #65738d !important; }

.stButton > button, .stDownloadButton > button {
    border: 1px solid rgba(174, 164, 255, .34) !important;
    border-radius: 12px !important;
    background: linear-gradient(110deg, #9183ff 0%, #6e72f6 55%, #54cfc7 130%) !important;
    color: #080d18 !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 800 !important;
    font-size: .92rem !important;
    letter-spacing: .01em !important;
    padding: .75rem 1.1rem !important;
    min-height: 3rem;
    box-shadow: 0 8px 25px rgba(111, 102, 240, .2) !important;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(111, 102, 240, .3) !important;
    filter: brightness(1.06);
}
.stButton > button:active, .stDownloadButton > button:active {
    transform: translateY(0) !important;
}
.stDownloadButton > button {
    background: rgba(139,124,255,.12) !important;
    color: #dcd8ff !important;
    border-color: rgba(139,124,255,.3) !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover { background: rgba(139,124,255,.2) !important; }

/* Pipeline cards */
.section-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: #f0f4ff;
    margin: .4rem 0 1.1rem;
    letter-spacing: -.025em;
}
.step-card {
    background: linear-gradient(120deg, rgba(18, 28, 47, .88), rgba(13, 21, 37, .78));
    border: 1px solid rgba(157,177,211,.14);
    border-radius: 15px;
    padding: 1.1rem 1.15rem;
    margin-bottom: .75rem;
    position: relative;
    overflow: hidden;
    transition: border-color .25s, transform .25s, background .25s;
}
.step-card:hover { transform: translateY(-1px); border-color: rgba(157,177,211,.28); }
.step-card.active {
    border-color: rgba(139,124,255,.62);
    background: linear-gradient(120deg, rgba(100,84,220,.17), rgba(17,27,47,.9));
    box-shadow: 0 0 0 1px rgba(139,124,255,.07), 0 8px 28px rgba(0,0,0,.12);
}
.step-card.done {
    border-color: rgba(83,214,162,.34);
    background: linear-gradient(120deg, rgba(44,166,128,.1), rgba(17,27,47,.85));
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: rgba(157,177,211,.12);
}
.step-card.active::before { background: #a69bff; }
.step-card.done::before { background: #53d6a2; }
.step-header { display: flex; align-items: center; gap: .7rem; margin-bottom: .25rem; }
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .68rem;
    color: #a69bff;
    background: rgba(139,124,255,.11);
    border: 1px solid rgba(139,124,255,.16);
    padding: .28rem .42rem;
    border-radius: 6px;
}
.step-title {
    font-family: 'Manrope', sans-serif;
    font-size: .91rem;
    font-weight: 800;
    color: #eaf0ff;
}
.step-status {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .62rem;
    letter-spacing: .07em;
    white-space: nowrap;
}
.status-waiting { color: #71809b; }
.status-running { color: #bcb4ff; }
.status-done { color: #65e2b2; }
.step-card div[style*="font-size:0.82rem"] { color: #8291ac !important; line-height: 1.5; }

/* Results */
.result-panel, .report-panel, .feedback-panel {
    background: linear-gradient(145deg, rgba(18,28,47,.82), rgba(12,19,33,.78));
    border: 1px solid rgba(157,177,211,.15);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    margin: .7rem 0 1.3rem;
    box-shadow: 0 12px 38px rgba(0,0,0,.12);
}
.report-panel { border-color: rgba(139,124,255,.3); }
.feedback-panel { border-color: rgba(83,214,162,.25); }
.result-panel-title, .panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .69rem;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: .75rem;
}
.result-panel-title, .panel-label.orange {
    color: #bcb4ff;
    border-bottom: 1px solid rgba(139,124,255,.2);
}
.panel-label.green {
    color: #65e2b2;
    border-bottom: 1px solid rgba(83,214,162,.2);
}
.result-content {
    font-size: .92rem;
    line-height: 1.85;
    color: #c2cde0;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stExpander"] {
    background: rgba(17,26,44,.6);
    border: 1px solid rgba(157,177,211,.14);
    border-radius: 13px;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif !important;
    font-size: .9rem !important;
    color: #c6d1e6 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Manrope', sans-serif;
    color: #f0f4ff;
    letter-spacing: -.025em;
}
.stMarkdown p, .stMarkdown li { color: #c4cee0; line-height: 1.8; }
.stMarkdown a { color: #a69bff; }
.stMarkdown code {
    color: #bcb4ff;
    background: rgba(139,124,255,.1);
    border-radius: 5px;
}
.stSpinner > div { color: #bcb4ff !important; }
[data-testid="stAlert"] { border-radius: 12px; }
.notice {
    font-family: 'IBM Plex Mono', monospace;
    font-size: .68rem;
    color: #65738d;
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(157,177,211,.1);
    letter-spacing: .04em;
}
@media (max-width: 900px) {
    .block-container { padding: 1rem 1rem 2rem; }
    .hero { padding: 1.8rem 0 1.2rem; }
    .input-card, .result-panel, .report-panel, .feedback-panel { padding: 1.2rem; }
    .step-card { padding: .95rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div style="display:flex;justify-content:center;gap:.65rem;flex-wrap:wrap;margin:0 auto 1.3rem;">
    <span style="font:500 .68rem 'IBM Plex Mono',monospace;color:#aab8d1;border:1px solid rgba(157,177,211,.16);background:rgba(17,26,44,.58);padding:.45rem .75rem;border-radius:999px;">✦ WEB SEARCH</span>
    <span style="font:500 .68rem 'IBM Plex Mono',monospace;color:#aab8d1;border:1px solid rgba(157,177,211,.16);background:rgba(17,26,44,.58);padding:.45rem .75rem;border-radius:999px;">✦ DEEP READING</span>
    <span style="font:500 .68rem 'IBM Plex Mono',monospace;color:#aab8d1;border:1px solid rgba(157,177,211,.16);background:rgba(17,26,44,.58);padding:.45rem .75rem;border-radius:999px;">✦ REPORT GENERATION</span>
    <span style="font:500 .68rem 'IBM Plex Mono',monospace;color:#aab8d1;border:1px solid rgba(157,177,211,.16);background:rgba(17,26,44,.58);padding:.45rem .75rem;border-radius:999px;">✦ AI REVIEW</span>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(139,124,255,0.08);
            border:1px solid rgba(139,124,255,0.18);
            border-radius:6px;
            padding:0.25rem 0.7rem;
            font-size:0.75rem;
            color:#a09890;
            font-family:'DM Sans',sans-serif;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)