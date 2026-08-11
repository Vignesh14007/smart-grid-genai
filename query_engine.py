import psycopg2


def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="smart_grid",
        user="smartgrid_user",
        password="smartgrid123"
    )


def execute_query(query):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    cursor.close()
    connection.close()

    return columns, results
