from ollama import chat


# ============================================================
# GREETING CHECK
# ============================================================

def is_greeting(question):

    text = question.strip().lower()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hai",
        "hi there",
        "hello there",
        "hey there",
        "good morning",
        "good afternoon",
        "good evening"
    }

    return text in greetings


# ============================================================
# RELEVANCE CHECK
# ============================================================

def check_relevance(question):

    prompt = f"""
You are a relevance classifier for a Smart Grid Monitoring
question-answering system.

The system can answer questions about:

- smart grid
- power
- voltage
- current
- energy consumption
- feeders
- transformers
- power measurements
- electricity measurements
- timestamps
- database measurements

Determine whether the user's question is related to these topics.

User question:
{question}

Return ONLY one of these two exact words:

RELEVANT

IRRELEVANT

Do not provide any explanation.
Do not return any other text.
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

    result = response["message"]["content"].strip().upper()

    # --------------------------------------------------------
    # Exact classification
    # --------------------------------------------------------

    if result == "RELEVANT":
        return True

    return False
