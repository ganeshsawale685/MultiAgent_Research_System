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

# ── Custom CSS · "Orbit" theme (light) ────────────────────────────────────────
# Palette
#   paper   #f5f1ff   page background (pale lilac)
#   ink     #1e1536   text / primary button (deep violet-black)
#   violet  #6c3df0   Search agent, links, focus
#   tang    #ff7a2f   Reader agent, running state
#   pink    #ff4d8d   Writer agent
#   teal    #14b8a6   Critic agent, done state
# Each agent has its own colour, and the hero shows four of them orbiting a core.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;800&family=Figtree:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
    --paper: #f5f1ff;
    --ink: #1e1536;
    --ink-soft: #4b4268;
    --line: #d8cff5;
    --violet: #6c3df0;
    --tang: #ff7a2f;
    --pink: #ff4d8d;
    --teal: #14b8a6;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Figtree', system-ui, sans-serif;
    color: var(--ink);
}
.stApp {
    background-color: var(--paper);
    background-image:
        radial-gradient(ellipse 55% 45% at 8% 0%, rgba(108,61,240,0.14) 0%, transparent 65%),
        radial-gradient(ellipse 45% 40% at 100% 18%, rgba(255,122,47,0.14) 0%, transparent 65%),
        radial-gradient(ellipse 50% 40% at 70% 105%, rgba(255,77,141,0.10) 0%, transparent 65%);
}
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: var(--ink-soft);
    line-height: 1.75;
}
.stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2,
.stApp [data-testid="stMarkdownContainer"] h3,
.stApp [data-testid="stMarkdownContainer"] h4 {
    font-family: 'Unbounded', sans-serif;
    font-weight: 600;
    color: var(--ink);
    letter-spacing: -0.01em;
}
.stApp [data-testid="stMarkdownContainer"] strong { color: var(--ink); }
.stApp [data-testid="stMarkdownContainer"] a { color: var(--violet); }
.stApp [data-testid="stMarkdownContainer"] code {
    background: rgba(108,61,240,0.10);
    color: var(--violet);
    border-radius: 5px;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero with orbiting agents (the one big animated moment) ── */
.hero {
    position: relative;
    padding: 3rem 0 2.5rem;
    min-height: 320px;
}
.hero h1 {
    position: relative;
    z-index: 2;
    font-family: 'Unbounded', sans-serif;
    font-size: clamp(2.1rem, 5.2vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.04em;
    color: var(--ink);
    margin: 0 0 1.2rem;
    animation: drop 0.9s cubic-bezier(.2,.9,.25,1.1) both;
}
.hero-sub {
    position: relative;
    z-index: 2;
    font-size: 1.08rem;
    color: var(--ink-soft);
    max-width: 470px;
    line-height: 1.65;
    margin: 0;
    animation: drop 0.9s 0.15s cubic-bezier(.2,.9,.25,1.1) both;
}
@keyframes drop {
    from { opacity: 0; transform: translateY(-16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.orbit {
    position: absolute;
    z-index: 1;
    right: 4%;
    top: 50%;
    width: 290px;
    height: 290px;
    margin-top: -145px;
}
.orbit .core {
    position: absolute;
    left: 50%; top: 50%;
    width: 74px; height: 74px;
    margin: -37px 0 0 -37px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, var(--violet), var(--pink), var(--tang), var(--violet));
    box-shadow: 0 0 40px rgba(108,61,240,0.35);
    animation: core-spin 6s linear infinite, core-pulse 2.6s ease-in-out infinite;
}
.orbit .core::after {
    content: '';
    position: absolute;
    inset: 9px;
    border-radius: 50%;
    background: var(--paper);
}
@keyframes core-spin  { to { transform: rotate(360deg); } }
@keyframes core-pulse {
    0%,100% { box-shadow: 0 0 30px rgba(108,61,240,0.30); }
    50%     { box-shadow: 0 0 60px rgba(255,77,141,0.45); }
}
.orbit .ring {
    position: absolute;
    border-radius: 50%;
    border: 1.5px dashed rgba(30,21,54,0.22);
}
.orbit .r1 { inset: 0; }
.orbit .r2 { inset: 52px; }
.orbit .arm {
    position: absolute;
    border-radius: 50%;
    animation: orbit linear infinite;
}
.orbit .arm i {
    position: absolute;
    top: -9px; left: 50%;
    width: 18px; height: 18px;
    margin-left: -9px;
    border-radius: 50%;
    background: var(--c);
    box-shadow: 0 0 0 4px rgba(255,255,255,0.7), 0 4px 14px var(--c);
}
.orbit .a1 { inset: 0;    --c: var(--violet); animation-duration: 9s; }
.orbit .a2 { inset: 0;    --c: var(--tang);   animation-duration: 9s; animation-delay: -4.5s; }
.orbit .a3 { inset: 52px; --c: var(--pink);   animation-duration: 5.5s; animation-direction: reverse; }
.orbit .a4 { inset: 52px; --c: var(--teal);   animation-duration: 5.5s; animation-direction: reverse; animation-delay: -2.75s; }
@keyframes orbit { to { transform: rotate(360deg); } }

@media (max-width: 760px) {
    .block-container { padding: 1.5rem 1.2rem 3rem; }
    .orbit { width: 160px; height: 160px; margin-top: -80px; right: -30px; opacity: 0.45; }
    .orbit .r2 { inset: 28px; }
    .orbit .a3, .orbit .a4 { inset: 28px; }
}

/* ── Divider ── */
.divider {
    height: 2px;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--violet), var(--pink), var(--tang), transparent);
    opacity: 0.55;
    margin: 2rem 0;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 2px solid var(--line) !important;
    border-radius: 14px !important;
    color: var(--ink) !important;
    font-family: 'Figtree', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.05rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input::placeholder { color: #9a90b8 !important; }
.stTextInput > div > div > input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 5px rgba(108,61,240,0.15) !important;
}
.stTextInput > label, .stTextInput label p {
    font-family: 'Unbounded', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button {
    background: var(--ink) !important;
    background-image: linear-gradient(110deg, var(--ink) 0%, var(--ink) 45%, var(--violet) 55%, var(--pink) 100%) !important;
    background-size: 250% 100% !important;
    background-position: 0% 0 !important;
    color: #ffffff !important;
    font-family: 'Unbounded', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 2rem !important;
    box-shadow: 0 6px 0 rgba(30,21,54,0.18) !important;
    transition: background-position 0.5s ease, transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-position: 100% 0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 9px 0 rgba(30,21,54,0.18) !important;
    color: #ffffff !important;
}
.stButton > button:active, .stDownloadButton > button:active {
    transform: translateY(4px) !important;
    box-shadow: 0 2px 0 rgba(30,21,54,0.18) !important;
}
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible {
    outline: 3px solid var(--tang) !important;
    outline-offset: 3px !important;
}

/* ── Example topics ── */
.try-row { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; margin: 1.1rem 0 1.5rem; }
.try-label { font-size: 0.85rem; color: #8a80a8; margin-right: 0.2rem; }
.chip {
    background: #ffffff;
    border: 1.5px solid var(--line);
    border-radius: 999px;
    padding: 0.28rem 0.85rem;
    font-size: 0.82rem;
    color: var(--ink-soft);
}

/* ── Pipeline ── */
.section-heading {
    font-family: 'Unbounded', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--ink);
    margin: 0.4rem 0 1rem;
}
.step-card {
    --c: var(--violet);
    display: flex;
    align-items: center;
    gap: 1rem;
    position: relative;
    overflow: hidden;
    background: #ffffff;
    border: 1.5px solid var(--line);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.4s, box-shadow 0.4s;
}
.step-card.active {
    border-color: var(--c);
    box-shadow: 0 8px 26px -10px var(--c);
}
.step-card.done { border-color: var(--teal); }

.step-node {
    flex: 0 0 auto;
    width: 2.5rem; height: 2.5rem;
    display: grid; place-items: center;
    border-radius: 50%;
    background: color-mix(in srgb, var(--c) 14%, white);
    color: var(--c);
    font-family: 'Unbounded', sans-serif;
    font-weight: 600;
    font-size: 0.72rem;
    position: relative;
}
.step-card.active .step-node::after {          /* pulsing ring on the running step */
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid var(--c);
    animation: node-ping 1.5s ease-out infinite;
}
@keyframes node-ping {
    0%   { transform: scale(1);   opacity: 0.9; }
    100% { transform: scale(1.8); opacity: 0; }
}
.step-card.done .step-node {
    background: var(--teal);
    color: #ffffff;
    animation: pop 0.5s cubic-bezier(.3,1.7,.5,1);
}
@keyframes pop { from { transform: scale(0.5) rotate(-30deg); } to { transform: scale(1) rotate(0); } }

.step-body { flex: 1 1 auto; min-width: 0; }
.step-title {
    font-family: 'Unbounded', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--ink);
}
.step-desc { font-size: 0.85rem; color: #7a7098; margin-top: 0.2rem; }
.step-status { flex: 0 0 auto; font-size: 0.82rem; font-weight: 600; }
.status-waiting { color: #a69dc2; }
.status-running { color: var(--tang); animation: breathe 1.3s ease-in-out infinite; }
.status-done    { color: var(--teal); }
@keyframes breathe { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }

.step-card.active::after {                    /* sliding bar along the bottom of the running step */
    content: '';
    position: absolute;
    left: 0; bottom: 0;
    height: 3px; width: 35%;
    background: linear-gradient(90deg, transparent, var(--c), transparent);
    animation: slide 1.5s ease-in-out infinite;
}
@keyframes slide { from { transform: translateX(-100%); } to { transform: translateX(300%); } }

/* ── Live scan bar (shown while the pipeline runs) ── */
.scan {
    margin: 0 0 1.1rem;
    font-size: 0.88rem;
    font-weight: 500;
    color: var(--violet);
}
.scan-track {
    position: relative;
    height: 6px;
    margin-top: 0.5rem;
    border-radius: 6px;
    background: rgba(108,61,240,0.12);
    overflow: hidden;
}
.scan-track::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    width: 35%;
    border-radius: 6px;
    background: linear-gradient(90deg, var(--violet), var(--pink), var(--tang));
    animation: scan 1.4s ease-in-out infinite;
}
@keyframes scan { from { left: -35%; } to { left: 100%; } }

/* ── Result panels ── */
.result-panel {
    background: #ffffff;
    border: 1.5px solid var(--line);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.5rem 0 1rem;
}
.result-panel-title {
    font-family: 'Unbounded', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--violet);
    margin-bottom: 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1.5px dashed var(--line);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: var(--ink-soft);
    white-space: pre-wrap;
}

/* ── Report & feedback headers (fade in when results land) ── */
.panel-label {
    font-family: 'Unbounded', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    margin: 2rem 0 0.8rem;
    padding: 0.25rem 0 0.25rem 0.9rem;
    border-left: 4px solid;
    animation: drop 0.7s cubic-bezier(.2,.9,.25,1.1) both;
}
.panel-label.orange { color: var(--ink); border-color: var(--pink); }
.panel-label.green  { color: var(--ink); border-color: var(--teal); }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff;
    border: 1.5px solid var(--line) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary,
details summary {
    font-family: 'Figtree', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    color: var(--ink-soft) !important;
}
[data-testid="stExpander"] summary:hover { color: var(--violet) !important; }

/* ── Spinner / alerts ── */
.stSpinner > div { color: var(--violet) !important; }
.stSpinner svg { stroke: var(--violet) !important; }
[data-testid="stAlert"] { border-radius: 14px; }

/* ── Footer ── */
.notice {
    font-size: 0.82rem;
    color: #9a90b8;
    text-align: center;
    margin-top: 3rem;
}

/* ── Respect reduced-motion settings ── */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("Waiting",  "status-waiting"),
        "running": ("Running",  "status-running"),
        "done":    ("Done",     "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    agent_color = {
        "01": "var(--violet)",
        "02": "var(--tang)",
        "03": "var(--pink)",
        "04": "var(--teal)",
    }.get(num, "var(--violet)")
    node = "✓" if state == "done" else num
    desc_html = f"<div class='step-desc'>{desc}</div>" if desc else ""
    st.markdown(f"""
    <div class="step-card {card_cls}" style="--c:{agent_color};">
        <div class="step-node">{node}</div>
        <div class="step-body">
            <div class="step-title">{title}</div>
            {desc_html}
        </div>
        <span class="step-status {cls}">{label}</span>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="orbit">
        <span class="ring r1"></span><span class="ring r2"></span>
        <span class="core"></span>
        <span class="arm a1"><i></i></span>
        <span class="arm a2"><i></i></span>
        <span class="arm a3"><i></i></span>
        <span class="arm a4"><i></i></span>
    </div>
    <h1>ResearchMind</h1>
    <p class="hero-sub">
        Four AI agents search the web, read the best sources, write a report
        and critique it. Enter a topic to start.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    # Example chips
    examples = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress"]
    chips = "".join(f'<span class="chip">{ex}</span>' for ex in examples)
    st.markdown(
        f'<div class="try-row"><span class="try-label">Try:</span>{chips}</div>',
        unsafe_allow_html=True,
    )

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    # Animated progress bar while the agents are working (display only)
    if st.session_state.running and not st.session_state.done:
        st.markdown(
            '<div class="scan">Agents are working on your topic…'
            '<div class="scan-track"></div></div>',
            unsafe_allow_html=True,
        )

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
        st.markdown('<div class="panel-label orange">📝 Final Research Report</div>',
                    unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown('<div class="panel-label green">🧐 Critic Feedback</div>',
                    unsafe_allow_html=True)
        st.markdown(r["critic"])


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)