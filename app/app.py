import streamlit as st
import requests
import time
import os

st.set_page_config(
    page_title="Poornima University Chatbot",
    page_icon="🎓",
    layout="wide"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(59,130,246,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(37,99,235,0.10) 0%, transparent 55%),
        #f0f6ff !important;
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container { max-width: 860px !important; padding: 0 1.5rem 4rem !important; margin: 0 auto !important; }

/* ── Hero Banner ── */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 2rem 2.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    color: #1d4ed8;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    border: 1px solid #bfdbfe;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    line-height: 1.18;
    color: #0f172a;
    margin-bottom: 0.8rem;
}
.hero-title .title-plain {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: none !important;
}
.hero-title .title-accent {
    background: linear-gradient(135deg, #2563eb 20%, #1d4ed8 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: #475569;
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 480px;
    margin: 0 auto 0.5rem;
    line-height: 1.65;
}

/* ── Divider ── */
.pu-divider {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 0.5rem 0 2rem;
}
.pu-divider::before, .pu-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #bfdbfe, transparent);
}
.pu-divider-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #3b82f6;
    box-shadow: 0 0 8px rgba(59,130,246,0.5);
}

/* ── Card ── */
.chat-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(191,219,254,0.7);
    border-radius: 20px;
    padding: 2.2rem 2.4rem 2rem;
    box-shadow:
        0 4px 6px rgba(37,99,235,0.04),
        0 20px 40px rgba(37,99,235,0.07),
        inset 0 1px 0 rgba(255,255,255,0.9);
    margin-bottom: 1.5rem;
}

/* ── Label ── */
.input-label {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #1d4ed8;
    margin-bottom: 0.6rem;
}

/* ── Text Input override ── */
[data-testid="stTextInput"] > div > div {
    border: 1.5px solid #bfdbfe !important;
    border-radius: 12px !important;
    background: #f8fbff !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.06) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15), 0 2px 8px rgba(37,99,235,0.08) !important;
}
[data-testid="stTextInput"] input {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    color: #0f172a !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stTextInput"] input::placeholder { color: #94a3b8 !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.72rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    width: 100% !important;
    margin-top: 1rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.30) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.38) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Answer Box ── */
.answer-box {
    background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
    border: 1px solid #bfdbfe;
    border-left: 4px solid #2563eb;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.5rem;
    animation: fadeSlide 0.4s ease;
}
.answer-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #1d4ed8;
    margin-bottom: 0.75rem;
}
.answer-header .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px rgba(34,197,94,0.6);
}
.answer-text {
    color: #1e293b;
    font-size: 1rem;
    line-height: 1.72;
    font-weight: 400;
}

/* ── Warning ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid #fde68a !important;
    background: #fffbeb !important;
}

/* ── Spinner text ── */
[data-testid="stSpinner"] p {
    font-family: 'DM Sans', sans-serif !important;
    color: #2563eb !important;
    font-weight: 500 !important;
}

/* ── Quick Chips ── */
.chips-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    justify-content: center;
}
.chip {
    background: white;
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 0.38rem 0.85rem;
    border-radius: 100px;
    cursor: default;
    box-shadow: 0 1px 3px rgba(37,99,235,0.08);
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    padding: 1.5rem 1rem;
    margin-top: 1rem;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1d4ed8;
    line-height: 1;
}
.stat-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 0.25rem;
}

/* ── Footer ── */
.pu-footer {
    text-align: center;
    padding: 2rem 0 0.5rem;
    color: #94a3b8;
    font-size: 0.8rem;
}
.pu-footer a { color: #3b82f6; text-decoration: none; }

/* ── Fade animation ── */
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ── Helper ──────────────────────────────────────────────────────────────────
def get_bot_response(question):
    base_url = os.getenv(
        "PU_CHATBOT_API_URL",
        "https://pu-chatbot-api-delightful-gerenuk-am.cfapps.us10-001.hana.ondemand.com"
    )
    url = f"{base_url.rstrip('/')}/ask"
    headers = {"Content-Type": "application/json"}
    data = {"input": {"question": question}}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json().get("answer", "Sorry, I couldn't find an answer.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection error: {e}"


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🎓 AI-Powered Campus Assistant</div>
    <h1 class="hero-title"><span class="title-plain">Poornima</span> <span class="title-accent">University</span><br><span class="title-plain">Chatbot</span></h1>
</div>
<div class="pu-divider"><div class="pu-divider-dot"></div></div>
""", unsafe_allow_html=True)

# ── Chat Card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">✦ Ask your question</div>', unsafe_allow_html=True)

user_input = st.text_input(
    label="question",
    placeholder="e.g. What are the BTech admission requirements?",
    label_visibility="collapsed"
)

ask_clicked = st.button("Ask Poornima University Chatbot →")

if ask_clicked:
    if user_input.strip():
        with st.spinner("Searching university knowledge base…"):
            time.sleep(0.8)
            answer = get_bot_response(user_input)
        st.markdown(f"""
        <div class="answer-box">
            <div class="answer-header">
                <div class="dot"></div>
                Poornima University Assistant
            </div>
            <div class="answer-text">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️  Please type a question before submitting.")

st.markdown('</div>', unsafe_allow_html=True)   # close chat-card

# ── Stats Bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item"><div class="stat-num">50+</div><div class="stat-label">Programs</div></div>
    <div class="stat-item"><div class="stat-num">15K+</div><div class="stat-label">Students</div></div>
    <div class="stat-item"><div class="stat-num">500+</div><div class="stat-label">Faculty</div></div>
    <div class="stat-item"><div class="stat-num">98%</div><div class="stat-label">Placement</div></div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pu-footer">
    Powered by Poornima University AI &nbsp;·&nbsp;
    <a href="https://poornima.edu.in" target="_blank">poornima.edu.in</a>
</div>
""", unsafe_allow_html=True)