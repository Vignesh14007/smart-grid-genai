import ollama


def generate_sql(question, conversation_context=""):

    prompt = f"""
You are an expert SQL generator for a smart-grid monitoring system.

Your job is to convert the user's natural-language question
into a PostgreSQL SELECT query.

Database table:

power_measurements

Columns:

id
timestamp
transformer_id
feeder_id
voltage
current
power
energy_consumption

Important rules:

1. Generate ONLY a PostgreSQL SELECT query.
2. Use only the power_measurements table.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   TRUNCATE, GRANT, REVOKE, or other modification queries.
4. Do not use tables that do not exist.
5. If aggregation is required, use GROUP BY correctly.
6. If the question asks for the highest value, use ORDER BY ... DESC.
7. If the question asks for the lowest value, use ORDER BY ... ASC.
8. Return ONLY SQL.
9. Do not use markdown code blocks.
10. Use previous conversation context when the current question
    refers to something such as "it", "its", "that feeder",
    "that transformer", "same feeder", or "previous result".
11. When the user asks for a single measurement such as voltage,
    current, power, or energy_consumption for a feeder or transformer,
    return the latest available measurement.
12. For the latest measurement, use:
    ORDER BY timestamp DESC
    LIMIT 1
13. If the user explicitly asks for average, maximum, minimum,
    total, or a time range, perform the requested calculation
    instead of using the latest measurement.
Previous conversation:

{conversation_context}

Current question:

{question}

Generate the PostgreSQL SELECT query now.
"""

    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()
