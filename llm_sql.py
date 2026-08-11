from ollama import chat


DATABASE_SCHEMA = """
Database: smart_grid

Table: power_measurements

Columns:
- id
- timestamp
- transformer_id
- feeder_id
- voltage
- current
- power
- energy_consumption
"""


def generate_sql(question):

    prompt = f"""
You are an expert PostgreSQL SQL generator.

Your task is to convert the user's natural-language question
into a PostgreSQL SQL query.

DATABASE SCHEMA:
{DATABASE_SCHEMA}

STRICT RULES:

1. Use ONLY the table public.power_measurements.
2. Never use smart_grid.power_measurements.
3. Use ONLY the columns listed in the schema.
4. Return ONLY one SELECT query.
5. Do not return markdown.
6. Do not explain the query.
7. Do not use unnecessary JOINs.
8. Do not invent tables or columns.

9. For "which feeder has the highest power":
   SELECT feeder_id, power
   FROM public.power_measurements
   ORDER BY power DESC
   LIMIT 1;

10. For "which feeder has the lowest power":
    SELECT feeder_id, power
    FROM public.power_measurements
    ORDER BY power ASC
    LIMIT 1;

11. For "which transformer has the highest average power":
    SELECT transformer_id, AVG(power) AS average_power
    FROM public.power_measurements
    GROUP BY transformer_id
    ORDER BY average_power DESC
    LIMIT 1;

12. For "which transformer has the lowest average power":
    SELECT transformer_id, AVG(power) AS average_power
    FROM public.power_measurements
    GROUP BY transformer_id
    ORDER BY average_power ASC
    LIMIT 1;

13. If the user asks "which [entity] has the highest/lowest [measurement]",
    return the entity identifier AND the corresponding measurement value.

14. Do not select a normal column together with MAX() or MIN()
    unless the query uses GROUP BY or a correct subquery.

15. Use PostgreSQL-compatible SQL.

USER QUESTION:
{question}
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


if __name__ == "__main__":

    question = input("Ask your question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)
