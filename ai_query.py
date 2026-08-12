from llm_sql import generate_sql
from query_engine import execute_query
from src.sql_validator import clean_sql, validate_sql
from src.answer_generator import generate_answer


def main():

    question = input("Ask your question: ")

    try:

        # --------------------------------
        # 1. Natural language → SQL
        # --------------------------------

        sql = generate_sql(question)

        sql = clean_sql(sql)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------
        # 2. Validate SQL
        # --------------------------------

        validate_sql(sql)

        print("\nSQL validation: PASSED")

        # --------------------------------
        # 3. Execute SQL
        # --------------------------------

        columns, results = execute_query(sql)

        print("\nDatabase Result:")
        print(columns)

        for row in results:
            print(row)

        # --------------------------------
        # 4. Generate AI answer
        # --------------------------------

        answer = generate_answer(
            question,
            columns,
            results
        )

        print("\nAI Answer:")
        print(answer)

    except Exception as error:

        print("\nError:")
        print(error)


if __name__ == "__main__":
    main()
