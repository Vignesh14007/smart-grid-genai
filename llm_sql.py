import ollama


def generate_sql(question, conversation_context=""):

    prompt = f"""
You are an expert PostgreSQL SQL generator for a
smart-grid monitoring system.

Your task is to convert the user's natural-language
question into ONE correct PostgreSQL SELECT query.

============================================================
DATABASE
============================================================

Table:
power_measurements

Columns:
- id
- timestamp
- transformer_id
- feeder_id
- voltage
- current
- power
- energy_consumption

============================================================
STRICT RULES
============================================================

1. Return ONLY the SQL query.

2. Use ONLY the power_measurements table.

3. Generate ONLY SELECT queries.

4. Never generate:
   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   CREATE
   TRUNCATE
   GRANT
   REVOKE

5. Never use tables or columns that do not exist.

6. Use PostgreSQL syntax.

7. Use GROUP BY correctly whenever aggregation
   is performed per feeder or transformer.

8. For "highest", "maximum", "largest", or "top":
   use ORDER BY <value> DESC.

9. For "lowest", "minimum", "smallest":
   use ORDER BY <value> ASC.

10. When using ORDER BY to find the highest or lowest
    record, SELECT both the identifying column and
    the value being compared.

    Example:

    SELECT feeder_id, power
    FROM power_measurements
    ORDER BY power DESC
    LIMIT 1;

11. When the user asks for the highest or lowest
    measurement, return enough information to identify
    the source and the measurement value.

12. When the user asks for a single measurement for
    a feeder or transformer, return the latest available
    measurement using:

    ORDER BY timestamp DESC
    LIMIT 1

13. For "average", use AVG().

14. For "maximum", use MAX() when the user asks for
    the maximum value itself or an aggregated maximum.

15. For "minimum", use MIN().

16. For "total", use SUM().

17. If the user asks for an average, maximum, minimum,
    total, or time-based calculation, perform the
    requested calculation instead of automatically
    returning the latest measurement.

18. If the user asks for multiple feeders or transformers,
    return the relevant identifying column together with
    the requested measurement.

19. Use aliases for calculated values when helpful.

20. Do not add explanations.

21. Do not add Markdown.

22. Do not wrap the SQL in ```.

============================================================
CONVERSATION CONTEXT
============================================================

Previous conversation:

{conversation_context}

============================================================
CURRENT QUESTION
============================================================

{question}

============================================================
EXAMPLES
============================================================

Question:
Which feeder has the highest power?

Correct SQL:

SELECT feeder_id, power
FROM power_measurements
ORDER BY power DESC
LIMIT 1;


Question:
Which transformer has the lowest voltage?

Correct SQL:

SELECT transformer_id, voltage
FROM power_measurements
ORDER BY voltage ASC
LIMIT 1;


Question:
What is the average voltage?

Correct SQL:

SELECT AVG(voltage) AS average_voltage
FROM power_measurements;


Question:
What is the average power for each feeder?

Correct SQL:

SELECT feeder_id, AVG(power) AS average_power
FROM power_measurements
GROUP BY feeder_id
ORDER BY average_power DESC;


Question:
What is the total energy consumption?

Correct SQL:

SELECT SUM(energy_consumption) AS total_energy_consumption
FROM power_measurements;


Question:
What is the latest power measurement for feeder F_01?

Correct SQL:

SELECT feeder_id, power, timestamp
FROM power_measurements
WHERE feeder_id = 'F_01'
ORDER BY timestamp DESC
LIMIT 1;


Question:
Which transformer has the highest average power?

Correct SQL:

SELECT transformer_id, AVG(power) AS average_power
FROM power_measurements
GROUP BY transformer_id
ORDER BY average_power DESC
LIMIT 1;

============================================================
FINAL INSTRUCTION
============================================================

Generate the PostgreSQL SELECT query for the
current question now.

Return ONLY SQL.
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
