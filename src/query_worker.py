from llm_sql import generate_sql
from query_engine import execute_query
from src.sql_validator import clean_sql, validate_sql
from src.answer_generator import generate_answer


def process_question(question, conversation_context=""):
    """
    Complete AI query pipeline.

    Question
        ↓
    Generate SQL
        ↓
    Clean SQL
        ↓
    Validate SQL
        ↓
    Execute PostgreSQL query
        ↓
    Generate human-readable answer

    This function does NOT contain Streamlit UI code.
    It can safely run in the background.
    """

    # --------------------------------------------------------
    # Generate SQL
    # --------------------------------------------------------

    sql = generate_sql(
        question,
        conversation_context
    )

    # --------------------------------------------------------
    # Clean generated SQL
    # --------------------------------------------------------

    sql = clean_sql(sql)

    # --------------------------------------------------------
    # Validate SQL
    # --------------------------------------------------------

    validate_sql(sql)

    # --------------------------------------------------------
    # Execute SQL
    # --------------------------------------------------------

    columns, results = execute_query(sql)

    # --------------------------------------------------------
    # Generate final answer
    # --------------------------------------------------------

    answer = generate_answer(
        question,
        columns,
        results
    )

    # --------------------------------------------------------
    # Return complete result
    # --------------------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "sql": sql,
        "columns": columns,
        "results": results
    }
