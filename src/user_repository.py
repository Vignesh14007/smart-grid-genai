from query_engine import get_connection


def get_or_create_user(google_sub, email, name=None):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check whether this Google account already exists
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE google_sub = %s
            """,
            (google_sub,)
        )

        row = cursor.fetchone()

        if row:
            user_id = row[0]

            # Keep profile information up to date
            cursor.execute(
                """
                UPDATE users
                SET email = %s,
                    name = %s
                WHERE id = %s
                """,
                (email, name, user_id)
            )

        else:
            # Create a new user
            cursor.execute(
                """
                INSERT INTO users (google_sub, email, name)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (google_sub, email, name)
            )

            user_id = cursor.fetchone()[0]

        connection.commit()

        return user_id

    finally:
        cursor.close()
        connection.close()
