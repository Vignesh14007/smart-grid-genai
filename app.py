import logging
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from src.chat_history import get_chat_history, save_chat
from src.query_worker import process_question
from src.user_repository import get_or_create_user
from query_engine import get_connection

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Grid AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# AUTHENTICATION
# ============================================================

if not st.user.is_logged_in:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            .stApp { background-color: #080B10; color: #F4F7FA; font-family: 'Inter', sans-serif; }
            .auth-container { text-align: center; margin-top: 120px; }
            .auth-logo { font-size: 48px; color: #22D3EE; margin-bottom: 16px; }
            .auth-title { font-size: 32px; font-weight: 700; color: #F4F7FA; margin-bottom: 8px; letter-spacing: -0.5px; }
            .auth-subtitle { color: #9AA7B5; font-size: 16px; margin-bottom: 48px; font-weight: 400; }
            .auth-card { background-color: #0E131A; border: 1px solid #26313D; border-radius: 12px; padding: 32px; max-width: 400px; margin: 0 auto; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
        </style>
        <div class="auth-container">
            <div class="auth-logo">⚡</div>
            <div class="auth-title">SMART GRID AI</div>
            <div class="auth-subtitle">Power Grid Intelligence</div>
            <div class="auth-card">
                <p style="color: #9AA7B5; margin-bottom: 24px; font-size: 14px;">Sign in to access the operations console</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("Sign in with Google", on_click=st.login, use_container_width=True)
    st.stop()

# ============================================================
# CURRENT USER
# ============================================================

google_sub = st.user.sub
user_email = st.user.email
user_name = st.user.name

user_id = get_or_create_user(google_sub, user_email, user_name)

# ============================================================
# CUSTOM CSS (Premium Dark Industrial Theme)
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base Variables */
    :root {
        --bg: #080B10;
        --surface-main: #0E131A;
        --surface-secondary: #121922;
        --surface-elevated: #171F29;
        --border: #26313D;
        --text-primary: #F4F7FA;
        --text-secondary: #9AA7B5;
        --text-muted: #667482;
        --accent: #22D3EE;
        --success: #22C55E;
        --warning: #F59E0B;
        --error: #EF4444;
    }

    /* Global */
    .stApp {
        background-color: var(--bg);
        color: var(--text-primary);
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    
    /* Layout */
    .block-container {
        padding-top: 32px;
        padding-bottom: 96px; 
        max-width: 1100px;
        margin: 0 auto;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--surface-main);
        border-right: 1px solid var(--border);
        min-width: 260px !important;
        max-width: 270px !important;
    }
    
    /* Remove default header styling */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Sidebar Elements */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 48px;
        margin-top: 16px;
    }
    .sidebar-logo {
        color: var(--accent);
        font-size: 24px;
        font-weight: 700;
    }
    .sidebar-title-container {
        display: flex;
        flex-direction: column;
    }
    .sidebar-app-name {
        font-size: 15px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: 0.5px;
    }
    .sidebar-app-sub {
        font-size: 11px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sidebar-section-title {
        font-size: 11px;
        font-weight: 600;
        color: var(--text-muted);
        margin-bottom: 16px;
        margin-top: 48px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Status indicators */
    .status-row {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 13px;
        color: var(--text-secondary);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 12px;
    }
    .status-dot.success { background-color: var(--success); }
    .status-dot.warning { background-color: var(--warning); }
    .status-dot.error { background-color: var(--error); }
    .status-dot.accent { background-color: var(--accent); }
    
    .status-value {
        color: var(--text-primary);
        font-weight: 500;
        margin-left: auto;
    }
    
    /* Custom Navigation Buttons (Styled Radio) */
    div.stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    div.stRadio > div > label {
        background-color: transparent;
        padding: 10px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 2px solid transparent;
        margin-bottom: 4px;
    }
    div.stRadio > div > label:hover {
        background-color: var(--surface-secondary);
    }
    div.stRadio > div > label[data-checked="true"] {
        background-color: var(--surface-secondary);
        border-left: 2px solid var(--accent);
    }
    div.stRadio > div > label > div:first-child {
        display: none; /* hide standard radio circle */
    }
    div.stRadio > div > label[data-checked="true"] p {
        color: var(--accent) !important;
        font-weight: 500;
    }
    div.stRadio > div > label p {
        color: var(--text-secondary);
        font-size: 14px;
        margin: 0;
    }

    /* Sidebar User Profile */
    .user-profile {
        margin-top: 48px;
        padding-top: 24px;
        border-top: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    .user-avatar {
        width: 32px;
        height: 32px;
        background-color: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: var(--text-primary);
        font-size: 14px;
    }
    .user-info {
        display: flex;
        flex-direction: column;
    }
    .user-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-primary);
    }
    .user-email {
        font-size: 11px;
        color: var(--text-muted);
    }
    
    /* Main Content Typography */
    .page-eyebrow {
        font-size: 12px;
        font-weight: 600;
        color: var(--text-muted);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .page-title {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .page-subtitle {
        font-size: 15px;
        color: var(--text-secondary);
        margin-bottom: 24px;
    }
    
    /* Top Status Strip */
    .top-status-strip {
        display: flex;
        gap: 12px;
        margin-bottom: 48px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        background-color: transparent;
        border: 1px solid var(--border);
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
        color: var(--text-secondary);
    }
    .status-pill .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-pill.ready .dot { background-color: var(--accent); }
    .status-pill.connected .dot { background-color: var(--success); }
    .status-pill.disconnected .dot { background-color: var(--error); }
    .status-pill.info .dot { background-color: var(--text-muted); }

    /* Buttons */
    .stButton button {
        background-color: var(--surface-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
        padding: 8px 16px;
    }
    .stButton button:hover {
        border-color: var(--accent);
        background-color: var(--surface-elevated);
        color: var(--accent);
    }

    /* Suggestions Area */
    .suggestions-title {
        font-size: 12px;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
        margin-top: 16px;
    }
    
    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 0;
        margin-bottom: 32px;
    }
    
    /* User Message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        display: flex;
        flex-direction: row-reverse;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
        background-color: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px 20px;
        max-width: 70%;
        color: var(--text-primary);
    }
    /* Hide avatars for a cleaner look */
    [data-testid="stChatMessage"] [data-testid="stChatAvatar"] {
        display: none;
    }
    
    /* AI Message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
        background-color: var(--surface-main);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* AI Header styling within markdown */
    .ai-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 24px;
    }
    .ai-header-icon {
        color: var(--accent);
    }
    
    .ai-content {
        font-size: 15px;
        color: var(--text-primary);
        line-height: 1.6;
        margin-bottom: 24px;
    }
    
    .ai-footer {
        font-size: 12px;
        color: var(--success);
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        border: 1px solid var(--border);
        background-color: var(--surface-secondary);
    }
    
    /* Expander / SQL */
    [data-testid="stExpander"] {
        background-color: var(--surface-main);
        border: 1px solid var(--border);
        border-radius: 8px;
        box-shadow: none;
    }
    [data-testid="stExpander"] summary {
        color: var(--text-secondary) !important;
        font-size: 13px;
        font-weight: 500;
        padding: 12px 16px;
    }
    [data-testid="stExpander"] summary:hover {
        color: var(--text-primary) !important;
    }
    [data-testid="stExpander"] summary p {
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stCode"] {
        border-radius: 8px;
        background-color: var(--surface-secondary) !important;
        border: 1px solid var(--border);
        margin-top: 8px;
    }
    [data-testid="stCode"] code {
        font-family: monospace;
    }

    /* Chat Input */
    [data-testid="stChatInput"] {
        background-color: var(--surface-main);
        border: 1px solid var(--border);
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        padding: 4px;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--accent);
    }
    [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-muted) !important;
    }
    [data-testid="stChatInput"] button {
        background-color: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
        transition: all 0.2s;
    }
    [data-testid="stChatInput"] button:hover {
        color: var(--accent) !important;
        background-color: var(--surface-secondary) !important;
    }
    
    /* Chat History Cards */
    .history-card {
        background-color: var(--surface-main);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .history-card-q {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 12px;
    }
    .history-card-a {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 24px;
        line-height: 1.6;
    }
    .history-card-meta {
        font-size: 12px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        margin-top: 80px;
        padding: 48px;
    }
    .empty-icon {
        font-size: 40px;
        color: var(--text-muted);
        margin-bottom: 24px;
    }
    .empty-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 12px;
    }
    .empty-desc {
        font-size: 14px;
        color: var(--text-secondary);
        max-width: 400px;
        margin: 0 auto 32px auto;
        line-height: 1.6;
    }
    
    /* Status block for processing */
    [data-testid="stStatusWidget"] {
        background-color: var(--surface-main);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DB METRICS CACHING
# ============================================================
@st.cache_data(ttl=60)
def get_grid_metrics():
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM power_measurements")
        measurements = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        return {"measurements": measurements, "status": "Connected"}
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return {"measurements": "-", "status": "Error"}

metrics = get_grid_metrics()

# ============================================================
# SESSION STATE
# ============================================================
if "chat_history" not in st.session_state:
    rows = get_chat_history(user_id)
    st.session_state.chat_history = []
    for row in reversed(rows):
        chat_id, question, answer, generated_sql, created_at = row
        st.session_state.chat_history.append({
            "role": "user",
            "content": question,
            "chat_id": chat_id,
            "created_at": created_at
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sql": generated_sql,
            "chat_id": chat_id,
            "created_at": created_at
        })

if "query_executor" not in st.session_state:
    st.session_state.query_executor = ThreadPoolExecutor(max_workers=1)

if "query_future" not in st.session_state:
    st.session_state.query_future = None

if "query_question" not in st.session_state:
    st.session_state.query_question = None

if "navigate_to" not in st.session_state:
    st.session_state.navigate_to = None

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">⚡</div>
            <div class="sidebar-title-container">
                <div class="sidebar-app-name">SMART GRID AI</div>
                <div class="sidebar-app-sub">Power Grid Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sidebar-section-title">NAVIGATION</div>', unsafe_allow_html=True)
    
    # Handle navigation
    if st.session_state.navigate_to:
        st.session_state.current_page_radio = st.session_state.navigate_to
        st.session_state.navigate_to = None
        
    selected_page = st.radio(
        "Navigation",
        ["◉ AI Assistant", "◷ Chat History"],
        label_visibility="collapsed",
        key="current_page_radio"
    )
    
    st.markdown('<div class="sidebar-section-title">SYSTEM STATUS</div>', unsafe_allow_html=True)
    
    if metrics["status"] == "Connected":
        st.markdown(
            '<div class="status-row"><div class="status-dot success"></div>PostgreSQL<div class="status-value">Connected</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-row"><div class="status-dot error"></div>PostgreSQL<div class="status-value">Error</div></div>',
            unsafe_allow_html=True
        )
        
    st.markdown(
        '<div class="status-row"><div class="status-dot accent"></div>AI Engine<div class="status-value">Ready</div></div>',
        unsafe_allow_html=True
    )
    
    measurements_count = metrics["measurements"] if metrics["measurements"] != "-" else "0"
    st.markdown(
        f'<div class="status-row"><div class="status-dot muted"></div>Measurements<div class="status-value">{measurements_count}</div></div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="user-profile">
            <div class="user-avatar">{user_name[0].upper() if user_name else 'U'}</div>
            <div class="user-info">
                <div class="user-name">{user_name}</div>
                <div class="user-email">{user_email}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.button("Logout", on_click=st.logout, use_container_width=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def is_greeting(question):
    text = question.lower().strip()
    greetings = {"hi", "hii", "hello", "hey", "hi there", "hello there", "good morning", "good afternoon", "good evening", "thanks", "thank you", "what can you do", "who are you"}
    return text in greetings

def greeting_response(question):
    text = question.lower().strip()
    if text in {"thanks", "thank you"}:
        return "You're welcome! ⚡ Feel free to ask another smart-grid question."
    if text in {"what can you do", "what can you do?"}:
        return "I can convert natural-language questions into database queries and help you analyze smart-grid measurements such as power, voltage, current, feeders, transformers, and energy consumption."
    if text in {"who are you", "who are you?"}:
        return "I'm Smart Grid AI — a natural-language interface for querying and analyzing smart-grid power data."
    return "Hello! 👋 I'm Smart Grid AI. I can help you analyze smart-grid power measurements. Ask me about feeders, transformers, power, voltage, current, or energy consumption."

def is_smart_grid_question(question):
    text = question.lower().strip()
    keywords = ["smart grid", "power grid", "electric grid", "electricity", "electrical", "feeder", "transformer", "power", "voltage", "current", "energy", "consumption", "measurement", "reading", "database", "data", "f_01", "f_02", "tr_01", "tr_02"]
    return any(keyword in text for keyword in keywords)

def irrelevant_response():
    return (
        "This question is outside the current grid dataset.\n\n"
        "Try asking about:\n"
        "• transformers\n"
        "• feeders\n"
        "• power\n"
        "• voltage\n"
        "• current\n"
        "• energy consumption\n"
        "• measurements"
    )

def build_conversation_context():
    ctx = ""
    for msg in st.session_state.chat_history:
        ctx += f"{msg['role'].upper()}: {msg['content']}\n"
        if "sql" in msg:
            ctx += f"GENERATED SQL: {msg['sql']}\n"
        if "result" in msg:
            ctx += f"DATABASE RESULT: {msg['result']}\n"
    return ctx

def check_background_query():
    future = st.session_state.query_future
    if future is None or not future.done():
        return False
        
    try:
        result = future.result()
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["answer"],
            "sql": result["sql"],
            "result": result["results"]
        })
        save_chat(user_id=user_id, question=result["question"], answer=result["answer"], generated_sql=result["sql"])
        
        st.session_state.query_future = None
        st.session_state.query_question = None
        return True
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "I couldn't process that request. Please ask a question about the smart-grid measurements."
        })
        st.session_state.query_future = None
        st.session_state.query_question = None
        return True
    except Exception as e:
        logger.exception("Background query failed")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "⚠️ **Something went wrong**\n\nWe couldn't process that query right now."
        })
        st.session_state.query_future = None
        st.session_state.query_question = None
        return True

def submit_question(q):
    q = q.strip()
    if not q: return
    
    st.session_state.chat_history.append({"role": "user", "content": q})
    
    if is_greeting(q):
        st.session_state.chat_history.append({"role": "assistant", "content": greeting_response(q)})
        return
        
    if not is_smart_grid_question(q):
        st.session_state.chat_history.append({"role": "assistant", "content": irrelevant_response()})
        return
        
    ctx = build_conversation_context()
    future = st.session_state.query_executor.submit(process_question, q, ctx)
    st.session_state.query_future = future
    st.session_state.query_question = q

# ============================================================
# PAGE: AI ASSISTANT
# ============================================================
if selected_page == "◉ AI Assistant":
    
    st.markdown('<div class="page-eyebrow">SMART GRID INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Grid Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ask questions about your power grid using natural language.</div>', unsafe_allow_html=True)
    
    status_class = "connected" if metrics["status"] == "Connected" else "disconnected"
    
    st.markdown(
        f'''
        <div class="top-status-strip">
            <div class="status-pill ready"><div class="dot"></div>AI Engine Ready</div>
            <div class="status-pill {status_class}"><div class="dot"></div>PostgreSQL {metrics["status"]}</div>
            <div class="status-pill info"><div class="dot"></div>{measurements_count} Measurements</div>
        </div>
        ''', unsafe_allow_html=True
    )
    
    # Check for background queries
    if check_background_query():
        st.rerun()

    # Empty State & Suggestions
    if not st.session_state.chat_history:
        st.markdown('<div class="suggestions-title">TRY ASKING</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("How many feeders are there?", use_container_width=True):
                submit_question("How many feeders are there?")
                st.rerun()
            if st.button("What is the average power of TR_01?", use_container_width=True):
                submit_question("What is the average power of TR_01?")
                st.rerun()
        with c2:
            if st.button("How many transformers are there?", use_container_width=True):
                submit_question("How many transformers are there?")
                st.rerun()
            if st.button("Show the latest readings", use_container_width=True):
                submit_question("Show the latest readings")
                st.rerun()
        with c3:
            if st.button("Which feeder has the highest power?", use_container_width=True):
                submit_question("Which feeder has the highest power?")
                st.rerun()
            if st.button("Which transformer uses the most energy?", use_container_width=True):
                submit_question("Which transformer uses the most energy?")
                st.rerun()
    
    # Render Chat History
    for message in st.session_state.chat_history:
        role = message["role"]
        with st.chat_message(role, avatar="👤" if role == "user" else "⚡"):
            if role == "assistant":
                if "⚠️" in message["content"] or is_greeting(message.get("content", "")) or "outside the current" in message.get("content", ""):
                    st.markdown(message["content"])
                else:
                    st.markdown(
                        f"""
                        <div class="ai-header">
                            <span class="ai-header-icon">⚡</span> SMART GRID AI
                        </div>
                        <div class="ai-content">
                            {message["content"]}
                        </div>
                        <div class="ai-footer">✓ Query completed</div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                if message.get("result"):
                    st.dataframe(message["result"], use_container_width=True, hide_index=True)
                    
                if message.get("sql"):
                    with st.expander("▸ View generated SQL"):
                        st.code(message["sql"], language="sql")
            else:
                st.markdown(message["content"])
                
    # Processing state
    if st.session_state.query_future is not None:
        with st.status("⚡ Processing your grid query", expanded=True):
            st.write("Generating SQL")
            st.write("Executing query")
            st.write("Preparing response")
        
    # Chat Input
    question_input = st.chat_input(
        "Ask about your smart grid...",
        disabled=(st.session_state.query_future is not None)
    )
    if question_input:
        submit_question(question_input)
        st.rerun()

# ============================================================
# PAGE: CHAT HISTORY
# ============================================================
elif selected_page == "◷ Chat History":
    
    st.markdown('<div class="page-eyebrow">CHAT HISTORY</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Previous Conversations</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Review your previous smart-grid questions and generated answers.</div>', unsafe_allow_html=True)
    
    history = get_chat_history(user_id)
    
    if not history:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">◷</div>
                <div class="empty-title">No conversations yet</div>
                <div class="empty-desc">Your saved grid questions will appear here after you start using the assistant.</div>
            </div>
            """, unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Open AI Assistant", use_container_width=True):
                st.session_state.navigate_to = "◉ AI Assistant"
                st.rerun()
    else:
        for chat_id, question, answer, generated_sql, created_at in history:
            timestamp = created_at.strftime("%d %b %Y · %I:%M %p")
            with st.container():
                st.markdown(
                    f"""
                    <div class="history-card">
                        <div class="history-card-q">{question}</div>
                        <div class="history-card-a">{answer}</div>
                        <div class="history-card-meta">
                            <span>{timestamp}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
                if generated_sql:
                    with st.expander("▸ View conversation"):
                        st.markdown(f"**Question:** {question}")
                        st.markdown(f"**Answer:** {answer}")
                        st.markdown("**Generated SQL:**")
                        st.code(generated_sql, language="sql")
                st.markdown("<br>", unsafe_allow_html=True)

