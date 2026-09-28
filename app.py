import logging
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from src.query_worker import process_question
from src.dashboard import show_dashboard


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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# AUTHENTICATION
# ============================================================

if not st.user.is_logged_in:

    st.title("⚡ Smart Grid AI")

    st.write(
        "Please sign in with your Google account to continue."
    )

    st.button(
        "Sign in with Google",
        on_click=st.login
    )

    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

google_sub = st.user.sub
user_email = st.user.email
user_name = st.user.name

user_id = get_or_create_user(
    google_sub,
    user_email,
    user_name
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(186, 230, 253, 0.35),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(224, 242, 254, 0.45),
                transparent 30%
            ),
            #f8fbff;

        color: #172033;

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2.5rem;
        padding-bottom: 6rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .app-title {
        font-size: 2.3rem;
        font-weight: 700;
        letter-spacing: -1px;
        color: #172033;
        margin-bottom: 0.4rem;
    }

    .app-title span {
        color: #1597d4;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #667085;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .header-line {
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #b9dff2,
            transparent
        );

        margin: 1.5rem 0 1.5rem 0;
    }

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        margin-bottom: 0.9rem;
        padding: 0.35rem 0.4rem;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: rgba(224, 242, 254, 0.72);
        border: 1px solid rgba(125, 211, 252, 0.45);

        box-shadow:
            0 8px 24px rgba(14, 116, 144, 0.06);
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(186, 230, 253, 0.75);

        box-shadow:
            0 8px 28px rgba(15, 118, 170, 0.07);
    }

    [data-testid="stChatMessage"] p {
        color: #243044 !important;
        font-size: 0.98rem;
        line-height: 1.7;
    }

    [data-testid="stChatMessage"] li {
        color: #243044 !important;
    }

    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(125, 211, 252, 0.65);
        border-radius: 18px;

        box-shadow:
            0 12px 35px rgba(14, 116, 144, 0.10);

        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    [data-testid="stChatInput"] textarea {
        color: #172033 !important;
        background: transparent !important;
        font-size: 0.96rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8a97a8 !important;
    }

    [data-testid="stChatInput"] button {
        background: #1597d4 !important;
        border-radius: 12px !important;
        border: none !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: #087fb8 !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid rgba(125, 211, 252, 0.45);
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.72);
        overflow: hidden;
        margin-top: 0.6rem;
    }

    [data-testid="stExpander"] summary {
        color: #24627d !important;
        font-weight: 600;
    }

    [data-testid="stCode"] {
        border-radius: 12px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(186, 230, 253, 0.75);
        border-radius: 14px;
        padding: 1rem;

        box-shadow:
            0 8px 24px rgba(15, 118, 170, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: #667085 !important;
    }

    [data-testid="stMetricValue"] {
        color: #172033 !important;
    }

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #f8fbff;
    }

    ::-webkit-scrollbar-thumb {
        background: #b7dced;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #83c5df;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if "query_executor" not in st.session_state:
    st.session_state.query_executor = ThreadPoolExecutor(
        max_workers=1
    )


if "query_future" not in st.session_state:
    st.session_state.query_future = None


if "query_question" not in st.session_state:
    st.session_state.query_question = None


if "last_analytics" not in st.session_state:
    st.session_state.last_analytics = None


if "current_page" not in st.session_state:
    st.session_state.current_page = "💬 AI Assistant"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="app-title">
        ⚡ Smart Grid <span>AI</span>
    </div>

    <div class="app-subtitle">
        Ask questions about feeders, transformers, power,
        voltage, current, or energy consumption using natural language.
    </div>

    <div class="header-line"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GREETING DETECTION
# ============================================================

def is_greeting(question):

    text = question.lower().strip()

    greetings = {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "hai",
        "hi there",
        "hello there",
        "hey there",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
        "thanks",
        "thank you",
        "thankyou",
        "what can you do",
        "what can you do?",
        "who are you",
        "who are you?",
        "what are you",
        "what are you?"
    }

    return text in greetings


# ============================================================
# GREETING RESPONSE
# ============================================================

def greeting_response(question):

    text = question.lower().strip()

    if text in {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "hai",
        "hi there",
        "hello there",
        "hey there"
    }:

        return (
            "Hello! 👋 I'm Smart Grid AI. "
            "I can help you analyze smart-grid power measurements. "
            "Ask me about feeders, transformers, power, voltage, "
            "current, or energy consumption."
        )

    if text == "good morning":

        return (
            "Good morning! 👋 "
            "I'm ready to help you analyze the smart-grid data."
        )

    if text == "good afternoon":

        return (
            "Good afternoon! 👋 "
            "What would you like to know about the smart-grid data?"
        )

    if text == "good evening":

        return (
            "Good evening! 👋 "
            "Ask me anything about the smart-grid measurements."
        )

    if text == "good night":

        return (
            "Good night! 👋 "
            "See you next time."
        )

    if text in {
        "thanks",
        "thank you",
        "thankyou"
    }:

        return (
            "You're welcome! ⚡ "
            "Feel free to ask another smart-grid question."
        )

    if text in {
        "what can you do",
        "what can you do?"
    }:

        return (
            "I can convert natural-language questions into "
            "database queries and help you analyze smart-grid "
            "measurements such as power, voltage, current, "
            "feeders, transformers, and energy consumption."
        )

    if text in {
        "who are you",
        "who are you?",
        "what are you",
        "what are you?"
    }:

        return (
            "I'm Smart Grid AI — a natural-language interface "
            "for querying and analyzing smart-grid power data."
        )

    return (
        "Hello! 👋 "
        "I can help you analyze the smart-grid measurements."
    )


# ============================================================
# SMART GRID DOMAIN CHECK
# ============================================================

def is_smart_grid_question(question):

    text = question.lower().strip()

    keywords = [

        "smart grid",
        "smart-grid",
        "power grid",
        "electric grid",
        "electricity",
        "electrical",

        "feeder",
        "feeders",
        "transformer",
        "transformers",

        "power",
        "voltage",
        "current",
        "energy",
        "energy consumption",
        "consumption",
        "measurement",
        "measurements",

        "highest power",
        "lowest power",
        "maximum power",
        "minimum power",
        "average power",
        "peak power",

        "highest voltage",
        "lowest voltage",
        "average voltage",

        "highest current",
        "lowest current",
        "average current",

        "highest energy",
        "lowest energy",
        "average energy",

        "reading",
        "readings",
        "database",
        "data",
        "record",
        "records",

        "f_01",
        "f_02",
        "f_03",

        "tr_01",
        "tr_02",
        "tr_03"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


# ============================================================
# IRRELEVANT RESPONSE
# ============================================================

def irrelevant_response():

    return (
        "I can help only with questions related to "
        "smart-grid monitoring and power measurements.\n\n"
        "You can ask about feeders, transformers, power, "
        "voltage, current, or energy consumption."
    )


# ============================================================
# CONVERSATION CONTEXT
# ============================================================

def build_conversation_context():

    conversation_context = ""

    for message in st.session_state.chat_history:

        conversation_context += (
            f"{message['role'].upper()}: "
            f"{message['content']}\n"
        )

        if "sql" in message:

            conversation_context += (
                f"GENERATED SQL: "
                f"{message['sql']}\n"
            )

        if "result" in message:

            conversation_context += (
                f"DATABASE RESULT: "
                f"{message['result']}\n"
            )

    return conversation_context


# ============================================================
# PROCESS COMPLETED BACKGROUND QUERY
# ============================================================

def check_background_query():

    future = st.session_state.query_future

    if future is None:
        return False

    if not future.done():
        return False

    try:

        result = future.result()

        # ----------------------------------------------------
        # Save chat response
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": result["answer"],
                "sql": result["sql"],
                "result": result["results"]
            }
        )

        # ----------------------------------------------------
        # Save analytics context
        # ----------------------------------------------------

        st.session_state.last_analytics = {
            "question": result["question"],
            "answer": result["answer"],
            "sql": result["sql"],
            "columns": result["columns"],
            "results": result["results"]
        }

        # ----------------------------------------------------
        # Clear background task
        # ----------------------------------------------------

        st.session_state.query_future = None
        st.session_state.query_question = None

        return True

    except ValueError as error:

        logger.warning(
            "Validation error: %s",
            error
        )

        error_message = (
            "I couldn't process that request. "
            "Please ask a question about the "
            "smart-grid measurements."
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )

        st.session_state.query_future = None
        st.session_state.query_question = None

        return True

    except Exception:

        logger.exception(
            "Background query failed"
        )

        error_message = (
            "Something went wrong while processing "
            "your request. Please try again."
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )

        st.session_state.query_future = None
        st.session_state.query_question = None

        return True


# ============================================================
# DISPLAY CHAT
# ============================================================

def show_chat():

    # --------------------------------------------------------
    # Check whether background query finished
    # --------------------------------------------------------

    if check_background_query():

        st.rerun()


    # --------------------------------------------------------
    # Display chat history
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        role = message["role"]

        with st.chat_message(
            role,
            avatar="👤" if role == "user" else "⚡"
        ):

            st.markdown(
                message["content"]
            )

            if (
                role == "assistant"
                and message.get("sql")
            ):

                with st.expander(
                    "View generated SQL"
                ):

                    st.code(
                        message["sql"],
                        language="sql"
                    )

            if (
                role == "assistant"
                and message.get("result")
            ):

                with st.expander(
                    "View database result"
                ):

                    st.dataframe(
                        message["result"],
                        use_container_width=True,
                        hide_index=True
                    )


    # --------------------------------------------------------
    # Processing status
    # --------------------------------------------------------

    if st.session_state.query_future is not None:

        st.info(
            "⚡ Your question is being processed..."
        )

        st.caption(
            "You can switch to Analytics. "
            "The AI query will continue processing."
        )


    # --------------------------------------------------------
    # Chat input
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask about your smart-grid data...",
        disabled=(
            st.session_state.query_future is not None
        )
    )


    # --------------------------------------------------------
    # New question
    # --------------------------------------------------------

    if question:

        question = question.strip()

        if not question:
            st.stop()


        # ----------------------------------------------------
        # Save user message
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )


        # ----------------------------------------------------
        # Greeting
        # ----------------------------------------------------

        if is_greeting(question):

            answer = greeting_response(
                question
            )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()


        # ----------------------------------------------------
        # Domain validation
        # ----------------------------------------------------

        if not is_smart_grid_question(
            question
        ):

            answer = irrelevant_response()

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()


        # ----------------------------------------------------
        # Build context
        # ----------------------------------------------------

        conversation_context = (
            build_conversation_context()
        )


        # ----------------------------------------------------
        # Start background processing
        # ----------------------------------------------------

        future = (
            st.session_state
            .query_executor
            .submit(
                process_question,
                question,
                conversation_context
            )
        )

        st.session_state.query_future = future

        st.session_state.query_question = (
            question
        )

        st.rerun()


# ============================================================
# NAVIGATION
# ============================================================

selected_page = st.radio(
    "View",
    [
        "💬 AI Assistant",
        "📊 Analytics"
    ],
    horizontal=True,
    key="current_page"
)


# ============================================================
# AI ASSISTANT
# ============================================================

if selected_page == "💬 AI Assistant":

    show_chat()


# ============================================================
# ANALYTICS
# ============================================================

elif selected_page == "📊 Analytics":

    # --------------------------------------------------------
    # Check background query
    # --------------------------------------------------------

    query_finished = (
        check_background_query()
    )

    if query_finished:

        st.success(
            "✅ Your latest AI analysis is ready."
        )


    # --------------------------------------------------------
    # Processing indicator
    # --------------------------------------------------------

    if st.session_state.query_future is not None:

        st.info(
            "⚡ Your AI question is still processing "
            "in the background."
        )

        st.caption(
            "You can continue viewing the overall "
            "grid analytics."
        )


    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    try:

        show_dashboard(
            st.session_state.last_analytics
        )

    except Exception:

        logger.exception(
            "Analytics dashboard error"
        )

        st.error(
            "Unable to load the analytics dashboard. "
            "Please check the database connection."
        )
