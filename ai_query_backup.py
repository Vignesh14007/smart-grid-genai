from ollama import chat

from llm_sql import generate_sql
from query_engine import execute_query


def clean_sql(sql):
    sql = sql.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


def validate_sql(sql):

    sql_lower = sql.lower().strip()

    # Must be SELECT
    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    # Only allow the project's table
    if "power_measurements" not in sql_lower:
        raise ValueError(
            "Query must use the power_measurements table."
        )

    # Block dangerous SQL operations
    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
        "execute"
    ]

    for keyword in blocked_keywords:

        if keyword in sql_lower:
            raise ValueError(
                f"Blocked SQL operation: {keyword}"
            )

    # Prevent multiple SQL statements
    if ";" in sql_lower[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    return True


def generate_answer(question, sql, columns, results):

    data = []

    for row in results:
        data.append(dict(zip(columns, row)))

    prompt = f"""
You are an assistant for a smart-grid monitoring system.

Answer the user's question using ONLY the database result provided.

User question:
{question}

SQL query:
{sql}

Database result:
{data}

Rules:
- Answer ONLY using information explicitly present in the database result.
- Never calculate or guess values that are not present in the result.
- Never invent numbers, units, measurements, dates, or identifiers.
- If the result contains only an identifier, report only that identifier.
- If a value is not available, say that it is not available.
- Give a clear and concise answer.
- Use simple language.
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


question = input("Ask your question: ")

try:

    # 1. Natural language → SQL
    sql = generate_sql(question)

    # 2. Clean SQL
    sql = clean_sql(sql)

    print("\nGenerated SQL:")
    print(sql)

    # 3. Validate SQL
    validate_sql(sql)

    # 4. Execute SQL
    columns, results = execute_query(sql)

    print("\nDatabase Result:")
    print(columns)

    for row in results:
        print(row)

    # 5. Generate human-readable answer
    answer = generate_answer(
        question,
        sql,
        columns,
        results
    )

    print("\nAI Answer:")
    print(answer)

except Exception as error:

    print("\nError:")
    print(error)
