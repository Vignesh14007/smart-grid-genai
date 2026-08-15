import ollama


def generate_sql(question, conversation_context=""):
    """
    Convert a natural-language smart-grid question
    into a safe PostgreSQL SELECT query.
    """

    prompt = f"""
Convert the user's question into ONE PostgreSQL SELECT query.

DATABASE TABLE:
power_measurements

COLUMNS:
id
timestamp
transformer_id
feeder_id
voltage
current
power
energy_consumption

RULES:
1. Return ONLY a PostgreSQL SELECT query.
2. Use ONLY the power_measurements table.
3. Never use INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, TRUNCATE, GRANT, REVOKE, or other
   modification statements.
4. Use GROUP BY correctly when aggregation is required.
5. Highest means ORDER BY ... DESC.
6. Lowest means ORDER BY ... ASC.
7. For a single measurement, return the latest
   available record using timestamp DESC LIMIT 1,
   unless the user explicitly asks for another
   calculation or time range.
8. For average, maximum, minimum, total, or time-range
   questions, perform the requested calculation.
9. If the question refers to something from the
   previous conversation, use the context.
10. Do not use tables or columns that do not exist.
11. Do not return explanations.
12. Do not use markdown code blocks.

PREVIOUS CONTEXT:
{conversation_context}

CURRENT QUESTION:
{question}

Return ONLY SQL.
"""

    response = ollama.chat(
        model="qwen2.5-coder:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0,
            "num_predict": 100
        },
        keep_alive="10m"
    )

    return response["message"]["content"].strip()
