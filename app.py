import streamlit as st

from llm_sql import generate_sql
from query_engine import execute_query
from src.sql_validator import clean_sql, validate_sql
from src.answer_generator import generate_answer


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
# CUSTOM STYLE
# White + Sky Blue Glassmorphism
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

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


    /* -------------------------------------------------------
       MAIN CONTENT WIDTH
    ------------------------------------------------------- */

    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 7rem;
    }


    /* -------------------------------------------------------
       REMOVE DEFAULT STREAMLIT TOP SPACE
    ------------------------------------------------------- */

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* -------------------------------------------------------
       MAIN TITLE
    ------------------------------------------------------- */

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


    /* -------------------------------------------------------
       SUBTITLE
    ------------------------------------------------------- */

    .app-subtitle {
        font-size: 1rem;
        color: #667085;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }


    /* -------------------------------------------------------
       HEADER LINE
    ------------------------------------------------------- */

    .header-line {
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #b9dff2,
            transparent
        );
        margin: 1.5rem 0 2rem 0;
    }


    /* -------------------------------------------------------
       CHAT MESSAGE AREA
    ------------------------------------------------------- */

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        margin-bottom: 0.9rem;
        padding: 0.35rem 0.4rem;
    }


    /* -------------------------------------------------------
       USER MESSAGE
    ------------------------------------------------------- */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: rgba(224, 242, 254, 0.72);
        border: 1px solid rgba(125, 211, 252, 0.45);
        box-shadow:
            0 8px 24px rgba(14, 116, 144, 0.06);
    }


    /* -------------------------------------------------------
       ASSISTANT MESSAGE
    ------------------------------------------------------- */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(186, 230, 253, 0.75);
        box-shadow:
            0 8px 28px rgba(15, 118, 170, 0.07);
    }


    /* -------------------------------------------------------
       MESSAGE TEXT
    ------------------------------------------------------- */

    [data-testid="stChatMessage"] p {
        color: #243044 !important;
        font-size: 0.98rem;
        line-height: 1.7;
    }


    [data-testid="stChatMessage"] li {
        color: #243044 !important;
    }


    /* -------------------------------------------------------
       CHAT INPUT
    ------------------------------------------------------- */

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


    /* -------------------------------------------------------
       BUTTON
    ------------------------------------------------------- */

    [data-testid="stChatInput"] button {
        background: #1597d4 !important;
        border-radius: 12px !important;
        border: none !important;
    }


    [data-testid="stChatInput"] button:hover {
        background: #087fb8 !important;
    }


    /* -------------------------------------------------------
       EXPANDERS
    ------------------------------------------------------- */

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


    /* -------------------------------------------------------
       CODE BLOCK
    ------------------------------------------------------- */

    [data-testid="stCode"] {
        border-radius: 12px;
    }


    /* -------------------------------------------------------
       DATAFRAME
    ------------------------------------------------------- */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }


    /* -------------------------------------------------------
       ALERTS
    ------------------------------------------------------- */

    [data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* -------------------------------------------------------
       SCROLLBAR
    ------------------------------------------------------- */

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
# HELPER FUNCTIONS
# ============================================================

def is_greeting(question):
    """
    Detect simple greetings so they do not go through
    SQL generation.
    """

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
        "how are you",
        "who are you",
        "what are you"
    }

    cleaned = question.lower().strip()

    return cleaned in greetings


def is_smart_grid_question(question):
    """
    Basic domain check.

    Questions containing these concepts are considered
    relevant to the smart-grid project.
    """

    keywords = [
        "smart grid",
        "smart-grid",
        "power",
        "voltage",
        "current",
        "energy",
        "energy consumption",
        "consumption",
        "feeder",
        "feeders",
        "transformer",
        "transformers",
        "measurement",
        "measurements",
        "electricity",
        "electrical",
        "grid",
        "load",
        "highest power",
        "lowest power",
        "average power",
        "latest voltage",
        "latest current"
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in keywords
    )


def greeting_response(question):
    """
    Natural response for greetings.
    """

    cleaned = question.lower().strip()

    if cleaned in {"hi", "hello", "hey", "hii", "hiii"}:
        return (
            "Hello! 👋 I'm Smart Grid AI. "
            "I can help you analyze smart-grid power measurements. "
            "You can ask me about feeders, transformers, "
            "power, voltage, current, or energy consumption."
        )

    if "good morning" in cleaned:
        return (
            "Good morning! 👋 "
            "I'm ready to help you analyze the smart-grid data."
        )

    if "good afternoon" in cleaned:
        return (
            "Good afternoon! 👋 "
            "What would you like to know about the smart-grid data?"
        )

    if "good evening" in cleaned:
        return (
            "Good evening! 👋 "
            "Ask me anything about the smart-grid measurements."
        )

    if "good night" in cleaned:
        return (
            "Good night! 👋 "
            "You can come back anytime to analyze the smart-grid data."
        )

    if "how are you" in cleaned:
        return (
            "I'm doing well! ⚡ "
            "I'm ready to help with your smart-grid analysis."
        )

    if "who are you" in cleaned or "what are you" in cleaned:
        return (
            "I'm Smart Grid AI, a natural-language interface "
            "for querying smart-grid power measurements."
        )

    return (
        "Hello! 👋 "
        "I can help you analyze the smart-grid measurements."
    )


def irrelevant_response():
    """
    Response when the user asks something outside
    the project's domain.
    """

    return (
        "I can help only with questions related to "
        "smart-grid monitoring and power measurements. "
        "You can ask about feeders, transformers, power, "
        "voltage, current, or energy consumption."
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.chat_history:

    role = message["role"]

    with st.chat_message(
        role,
        avatar="👤" if role == "user" else "⚡"
    ):

        st.markdown(message["content"])

        # ---------------------------------------------
        # Show SQL if available
        # ---------------------------------------------

        if role == "assistant" and message.get("sql"):

            with st.expander("View generated SQL"):

                st.code(
                    message["sql"],
                    language="sql"
                )

        # ---------------------------------------------
        # Show database result if available
        # ---------------------------------------------

        if role == "assistant" and message.get("result"):

            with st.expander("View database result"):

                st.dataframe(
                    message["result"],
                    use_container_width=True,
                    hide_index=True
                )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask about your smart-grid data..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    question = question.strip()

    if not question:
        st.stop()


    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(question)


    # ========================================================
    # GREETING CHECK
    # ========================================================

    if is_greeting(question):

        answer = greeting_response(question)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            st.markdown(answer)

        st.stop()


    # ========================================================
    # PROJECT DOMAIN CHECK
    # ========================================================

    if not is_smart_grid_question(question):

        answer = irrelevant_response()

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            st.markdown(answer)

        st.stop()


    # ========================================================
    # MAIN AI + SQL PIPELINE
    # ========================================================

    try:

        # ----------------------------------------------------
        # BUILD CONVERSATION CONTEXT
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # GENERATE SQL
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            with st.spinner("Analyzing smart-grid data..."):

                sql = generate_sql(
                    question,
                    conversation_context
                )

                sql = clean_sql(sql)


            # ------------------------------------------------
            # VALIDATE SQL
            # ------------------------------------------------

            validate_sql(sql)


            # ------------------------------------------------
            # EXECUTE SQL
            # ------------------------------------------------

            with st.spinner("Querying PostgreSQL..."):

                columns, results = execute_query(sql)


            # ------------------------------------------------
            # GENERATE NATURAL LANGUAGE ANSWER
            # ------------------------------------------------

            with st.spinner("Preparing the answer..."):

                answer = generate_answer(
                    question,
                    columns,
                    results
                )


            # ------------------------------------------------
            # DISPLAY ANSWER
            # ------------------------------------------------

            st.markdown(answer)


            # ------------------------------------------------
            # DISPLAY SQL
            # ------------------------------------------------

            with st.expander("View generated SQL"):

                st.code(
                    sql,
                    language="sql"
                )


            # ------------------------------------------------
            # DISPLAY DATABASE RESULT
            # ------------------------------------------------

            with st.expander("View database result"):

                if results:

                    st.dataframe(
                        results,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No records found."
                    )


        # ====================================================
        # SAVE ASSISTANT RESPONSE
        # ====================================================

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sql": sql,
                "result": results
            }
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        error_message = str(error)

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            st.error(
                f"Unable to process the request: {error_message}"
            )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": (
                    f"Unable to process the request: "
                    f"{error_message}"
                )
            }
        )
