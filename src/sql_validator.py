def clean_sql(sql):
    sql = sql.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


def validate_sql(sql):

    sql_lower = sql.lower().strip()

    # Only SELECT queries are allowed
    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    # Query must use our table
    if "power_measurements" not in sql_lower:
        raise ValueError(
            "Query must use the power_measurements table."
        )

    # Block dangerous SQL commands
    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
        "execute"
    ]

    for keyword in blocked_keywords:

        if keyword in sql_lower:
            raise ValueError(
                f"Blocked SQL operation: {keyword}"
            )

    # Prevent multiple SQL statements
    if ";" in sql_lower[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    return True
