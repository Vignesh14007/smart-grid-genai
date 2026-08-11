from query_engine import execute_query


def question_to_sql(question):
    question = question.lower().strip()

    if "average power" in question and "transformer" not in question:
        return """
        SELECT AVG(power) AS average_power
        FROM power_measurements;
        """

    elif "total energy" in question:
        return """
        SELECT SUM(energy_consumption) AS total_energy
        FROM power_measurements;
        """

    elif "highest power" in question:
        return """
        SELECT *
        FROM power_measurements
        ORDER BY power DESC
        LIMIT 1;
        """

    elif "transformer" in question and "average" in question:
        return """
        SELECT transformer_id,
               AVG(power) AS average_power
        FROM power_measurements
        GROUP BY transformer_id
        ORDER BY average_power DESC
        LIMIT 1;
        """

    else:
        return None


question = input("Ask your question: ")

sql_query = question_to_sql(question)

if sql_query is None:
    print("Sorry, I don't understand this question yet.")
else:
    print("\nGenerated SQL:")
    print(sql_query)

    columns, results = execute_query(sql_query)

    print("Result:")
    print(columns)

    for row in results:
        print(row)
