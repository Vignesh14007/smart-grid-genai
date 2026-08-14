import re


# ============================================================
# ALLOWED TABLE
# ============================================================

ALLOWED_TABLE = "power_measurements"


# ============================================================
# CLEAN SQL
# ============================================================

def clean_sql(sql):
    """
    Clean common formatting produced by an LLM.
    """

    if not sql:
        raise ValueError("The AI did not generate any SQL.")

    sql = sql.strip()

    # Remove markdown code fences
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    sql = sql.strip()

    # Remove common LLM prefixes
    prefixes = [
        "SQL:",
        "QUERY:",
        "GENERATED SQL:",
        "ANSWER:"
    ]

    for prefix in prefixes:

        if sql.upper().startswith(prefix):
            sql = sql[len(prefix):].strip()

    # Remove trailing semicolon
    sql = sql.rstrip(";").strip()

    return sql


# ============================================================
# VALIDATE SQL
# ============================================================

def validate_sql(sql):
    """
    Validate generated SQL before sending it to PostgreSQL.
    """

    if not sql:
        raise ValueError(
            "SQL validation failed: empty query."
        )


    # --------------------------------------------------------
    # Only SELECT queries are allowed
    # --------------------------------------------------------

    if not re.match(
        r"^\s*SELECT\b",
        sql,
        re.IGNORECASE
    ):

        raise ValueError(
            "Only SELECT queries are allowed."
        )


    # --------------------------------------------------------
    # Block multiple SQL statements
    # --------------------------------------------------------

    if ";" in sql:

        raise ValueError(
            "Multiple SQL statements are not allowed."
        )


    # --------------------------------------------------------
    # Block data modification commands
    # --------------------------------------------------------

    forbidden_commands = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE"
    ]

    sql_upper = sql.upper()

    for command in forbidden_commands:

        if re.search(
            rf"\b{command}\b",
            sql_upper
        ):

            raise ValueError(
                f"SQL command '{command}' is not allowed."
            )


    # --------------------------------------------------------
    # Require project table
    # --------------------------------------------------------

    if not re.search(
        rf"\b{ALLOWED_TABLE}\b",
        sql,
        re.IGNORECASE
    ):

        raise ValueError(
            f"Query must use the '{ALLOWED_TABLE}' table."
        )


    # --------------------------------------------------------
    # Basic SQL structure check
    # --------------------------------------------------------

    if not re.search(
        r"\bFROM\b",
        sql,
        re.IGNORECASE
    ):

        raise ValueError(
            "SQL validation failed: FROM clause is missing."
        )


    return True
