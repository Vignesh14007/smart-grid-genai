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
# CUSTOM CSS
# White + Sky Blue Glassmorphism
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
        padding-top: 3rem;
        padding-bottom: 7rem;
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

        margin: 1.5rem 0 2rem 0;
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
# GREETING DETECTION
# ============================================================

def is_greeting(question):
    """
    Detect common conversational messages so they
    do not enter the SQL pipeline.
    """

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
    """
    Return a natural response for simple conversational input.
    """

    text = question.lower().strip()

    # ---------------------------------------------
    # Basic greetings
    # ---------------------------------------------

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

    # ---------------------------------------------
    # Morning
    # ---------------------------------------------

    if text == "good morning":

        return (
            "Good morning! 👋 "
            "I'm ready to help you analyze the smart-grid data."
        )

    # ---------------------------------------------
    # Afternoon
    # ---------------------------------------------

    if text == "good afternoon":

        return (
            "Good afternoon! 👋 "
            "What would you like to know about the smart-grid data?"
        )

    # ---------------------------------------------
    # Evening
    # ---------------------------------------------

    if text == "good evening":

        return (
            "Good evening! 👋 "
            "Ask me anything about the smart-grid measurements."
        )

    # ---------------------------------------------
    # Night
    # ---------------------------------------------

    if text == "good night":

        return (
            "Good night! 👋 "
            "See you next time."
        )

    # ---------------------------------------------
    # Thanks
    # ---------------------------------------------

    if text in {
        "thanks",
        "thank you",
        "thankyou"
    }:

        return (
            "You're welcome! ⚡ "
            "Feel free to ask another smart-grid question."
        )

    # ---------------------------------------------
    # Capabilities
    # ---------------------------------------------

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

    # ---------------------------------------------
    # Identity
    # ---------------------------------------------

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
    """
    Check whether a question belongs to the smart-grid
    monitoring domain.
    """

    text = question.lower().strip()

    keywords = [

        # -----------------------------------------
        # Grid
        # -----------------------------------------

        "smart grid",
        "smart-grid",
        "power grid",
        "electric grid",
        "electricity",
        "electrical",

        # -----------------------------------------
        # Equipment
        # -----------------------------------------

        "feeder",
        "feeders",
        "transformer",
        "transformers",

        # -----------------------------------------
        # Measurements
        # -----------------------------------------

        "power",
        "voltage",
        "current",
        "energy",
        "energy consumption",
        "consumption",
        "measurement",
        "measurements",

        # -----------------------------------------
        # Analysis
        # -----------------------------------------

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

        # -----------------------------------------
        # Data
        # -----------------------------------------

        "reading",
        "readings",
        "database",
        "data",
        "record",
        "records",

        # -----------------------------------------
        # Dataset identifiers
        # -----------------------------------------

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
# IRRELEVANT QUESTION RESPONSE
# ============================================================

def irrelevant_response():

    return (
        "I can help only with questions related to "
        "smart-grid monitoring and power measurements.\n\n"
        "You can ask about feeders, transformers, power, "
        "voltage, current, or energy consumption."
    )


# ============================================================
# BUILD CONVERSATION CONTEXT
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
# DISPLAY PREVIOUS CHAT
# ============================================================

for message in st.session_state.chat_history:

    role = message["role"]

    with st.chat_message(
        role,
        avatar="👤" if role == "user" else "⚡"
    ):

        st.markdown(message["content"])

        # ---------------------------------------------
        # Generated SQL
        # ---------------------------------------------

        if (
            role == "assistant"
            and message.get("sql")
        ):

            with st.expander("View generated SQL"):

                st.code(
                    message["sql"],
                    language="sql"
                )

        # ---------------------------------------------
        # Database result
        # ---------------------------------------------

        if (
            role == "assistant"
            and message.get("result")
        ):

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
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(question)


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
    # STEP 1 — GREETING CHECK
    # ========================================================

    if is_greeting(question):

        answer = greeting_response(question)

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            st.markdown(answer)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.stop()


    # ========================================================
    # STEP 2 — SMART GRID DOMAIN CHECK
    # ========================================================

    if not is_smart_grid_question(question):

        answer = irrelevant_response()

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            st.markdown(answer)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.stop()


    # ========================================================
    # STEP 3 — BUILD CONTEXT
    # ========================================================

    try:

        conversation_context = (
            build_conversation_context()
        )


        # ====================================================
        # STEP 4 — GENERATE SQL
        # ====================================================

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            with st.spinner(
                "Analyzing smart-grid data..."
            ):

                sql = generate_sql(
                    question,
                    conversation_context
                )

                sql = clean_sql(sql)


            # =================================================
            # STEP 5 — VALIDATE SQL
            # =================================================

            validate_sql(sql)


            # =================================================
            # STEP 6 — EXECUTE SQL
            # =================================================

            with st.spinner(
                "Querying PostgreSQL..."
            ):

                columns, results = execute_query(sql)


            # =================================================
            # STEP 7 — GENERATE AI ANSWER
            # =================================================

            with st.spinner(
                "Preparing the answer..."
            ):

                answer = generate_answer(
                    question,
                    columns,
                    results
                )


            # =================================================
            # DISPLAY ANSWER
            # =================================================

            st.markdown(answer)


            # =================================================
            # DISPLAY SQL
            # =================================================

            with st.expander(
                "View generated SQL"
            ):

                st.code(
                    sql,
                    language="sql"
                )


            # =================================================
            # DISPLAY DATABASE RESULT
            # =================================================

            with st.expander(
                "View database result"
            ):

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

        error_message = (
            f"Unable to process the request: {error}"
        )

        with st.chat_message(
            "assistant",
            avatar="⚡"
        ):

            st.error(error_message)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )
