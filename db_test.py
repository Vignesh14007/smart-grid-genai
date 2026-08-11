import psycopg2

connection = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    database="smart_grid",
    user="smartgrid_user",
    password="smartgrid123"
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM power_measurements;")

result = cursor.fetchone()

print("Total records:", result[0])

cursor.close()
connection.close()
