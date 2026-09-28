from query_engine import get_connection


def save_chat(user_id, question, answer, generated_sql):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO chat_history (
                user_id,
                question,
                answer,
                generated_sql
            )
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, question, answer, generated_sql)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def get_chat_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                question,
                answer,
                generated_sql,
                created_at
            FROM chat_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
