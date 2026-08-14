from ollama import chat


def generate_answer(question, columns, results):
    """
    Convert database results into a concise,
    human-readable answer using the local LLM.
    """

    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not results:
        return (
            "I couldn't find any matching records "
            "in the smart-grid database."
        )

    # --------------------------------------------------------
    # Convert database result into readable text
    # --------------------------------------------------------

    result_text = ""

    for row in results:
        row_data = []

        for column, value in zip(columns, row):
            row_data.append(
                f"{column}: {value}"
            )

        result_text += (
            ", ".join(row_data) + "\n"
        )

    # --------------------------------------------------------
    # LLM prompt
    # --------------------------------------------------------

    prompt = f"""
You are Smart Grid AI, an assistant for analyzing
smart-grid power measurements.

User question:
{question}

Database columns:
{columns}

Database results:
{result_text}

Generate a short, clear and professional answer.

Rules:
1. Answer only from the database results.
2. Do not invent values.
3. Do not mention SQL unless the user asks about SQL.
4. Do not mention the LLM, model, prompt, or internal processing.
5. Use the actual names and values from the database.
6. Keep the answer concise.
7. If there are multiple important results, summarize them clearly.
8. Use appropriate units when they are available from the data.
9. If the result is empty, clearly say that no matching records were found.
"""

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    response = chat(
        model="llama3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"].strip()

    return answer
