from ollama import chat


def generate_answer(question, columns, results):

    data = []

    for row in results:
        data.append(
            dict(zip(columns, row))
        )

    prompt = f"""
You are an assistant for a smart-grid monitoring system.

Answer the user's question using ONLY the database result.

User question:
{question}

Database result:
{data}

Rules:
- Use only information present in the database result.
- Never invent numbers.
- Never invent measurements.
- Never invent dates or identifiers.
- If the information is unavailable, say so.
- Give a short and clear answer.
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
