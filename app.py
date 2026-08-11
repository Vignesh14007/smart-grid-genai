import streamlit as st

from llm_sql import generate_sql
from query_engine import execute_query


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Smart Grid AI Assistant",
    page_icon="⚡",
    layout="centered"
)


# -----------------------------
# SQL utilities
# -----------------------------

def clean_sql(sql):
    sql = sql.strip()
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    return sql.strip()


def validate_sql(sql):

    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke"
    ]

    for keyword in blocked_keywords:

        if keyword in sql_lower:
            raise ValueError(
                f"Blocked SQL operation: {keyword}"
            )


# -----------------------------
# AI answer
# -----------------------------

def generate_answer(question, sql, columns, results):

    data = []

    for row in results:
        data.append(
            dict(zip(columns, row))
        )

    from ollama import chat

    prompt = f"""
You are an assistant for a smart-grid monitoring system.

Answer the user's question using ONLY the database result.

User question:
{question}

Database result:
{data}

Rules:
- Answer only using information explicitly present in the database result.
- Never invent numbers, units, dates, identifiers, or measurements.
- If information is not available, say that it is not available.
- Give a clear and concise answer.
- Do not mention SQL, Python, PostgreSQL, or Llama.
"""

    response = chat(
        model="llama3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content.strip()


# -----------------------------
# UI
# -----------------------------

st.title("⚡ Smart Grid AI Assistant")

st.write(
    "Ask questions about power measurements "
    "using natural language."
)

question = st.text_input(
    "Ask your question",
    placeholder="Example: Which feeder has the highest power?"
)


if st.button("Ask AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Analyzing your question..."):

                # Natural language → SQL
                sql = generate_sql(question)

                # Clean generated SQL
                sql = clean_sql(sql)

                # Validate SQL
                validate_sql(sql)

                # Execute SQL
                columns, results = execute_query(sql)

                # Generate final answer
                answer = generate_answer(
                    question,
                    sql,
                    columns,
                    results
                )

            st.subheader("AI Answer")

            st.success(answer)

            with st.expander("View generated SQL"):

                st.code(
                    sql,
                    language="sql"
                )

            with st.expander("View database result"):

                st.dataframe(
                    results
                )

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )
