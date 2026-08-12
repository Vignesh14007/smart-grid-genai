import streamlit as st

from llm_sql import generate_sql
from query_engine import execute_query
from src.sql_validator import clean_sql, validate_sql
from src.answer_generator import generate_answer


# -----------------------------------------
# Page configuration
# -----------------------------------------

st.set_page_config(
    page_title="Smart Grid AI",
    page_icon="⚡",
    layout="centered"
)


# -----------------------------------------
# Session state
# -----------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------------------
# Header
# -----------------------------------------

st.title("⚡ Smart Grid AI Assistant")

st.write(
    "Ask questions about smart-grid power measurements "
    "using natural language."
)

st.divider()


# -----------------------------------------
# Display conversation
# -----------------------------------------

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# -----------------------------------------
# Chat input
# -----------------------------------------

question = st.chat_input(
    "Ask about the smart grid..."
)


# -----------------------------------------
# Process question
# -----------------------------------------

if question:

    # -----------------------------------------
    # Display user question
    # -----------------------------------------

    with st.chat_message("user"):
        st.write(question)

    # -----------------------------------------
    # Save user question
    # -----------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    try:

        # -----------------------------------------
        # Build detailed conversation context
        # -----------------------------------------

        conversation_context = ""

        for message in st.session_state.chat_history:

            conversation_context += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

            # Include SQL information when available
            if "sql" in message:

                conversation_context += (
                    f"GENERATED SQL: "
                    f"{message['sql']}\n"
                )

            # Include database result when available
            if "result" in message:

                conversation_context += (
                    f"DATABASE RESULT: "
                    f"{message['result']}\n"
                )


        # -----------------------------------------
        # Generate SQL
        # -----------------------------------------

        with st.spinner("Generating SQL..."):

            sql = generate_sql(
                question,
                conversation_context
            )

            sql = clean_sql(sql)


        # -----------------------------------------
        # Validate SQL
        # -----------------------------------------

        validate_sql(sql)


        # -----------------------------------------
        # Execute SQL
        # -----------------------------------------

        with st.spinner(
            "Querying smart-grid database..."
        ):

            columns, results = execute_query(sql)


        # -----------------------------------------
        # Generate AI answer
        # -----------------------------------------

        with st.spinner(
            "Generating answer..."
        ):

            answer = generate_answer(
                question,
                columns,
                results
            )


        # -----------------------------------------
        # Save complete interaction
        # -----------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sql": sql,
                "result": results
            }
        )


        # -----------------------------------------
        # Display AI answer
        # -----------------------------------------

        with st.chat_message("assistant"):

            st.write(answer)


        # -----------------------------------------
        # Display generated SQL
        # -----------------------------------------

        with st.expander(
            "View Generated SQL"
        ):

            st.code(
                sql,
                language="sql"
            )


        # -----------------------------------------
        # Display database result
        # -----------------------------------------

        with st.expander(
            "View Database Result"
        ):

            if results:

                st.dataframe(
                    results,
                    use_container_width=True
                )

            else:

                st.info(
                    "No records found."
                )


    except Exception as error:

        with st.chat_message("assistant"):

            st.error(
                f"Something went wrong: {error}"
            )
