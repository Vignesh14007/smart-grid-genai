import pytest

from src.sql_validator import clean_sql, validate_sql


# ============================================================
# CLEAN SQL TESTS
# ============================================================

def test_clean_sql_removes_sql_prefix():

    sql = "SQL: SELECT feeder_id FROM power_measurements"

    cleaned = clean_sql(sql)

    assert cleaned == (
        "SELECT feeder_id FROM power_measurements"
    )


def test_clean_sql_removes_trailing_semicolon():

    sql = (
        "SELECT feeder_id "
        "FROM power_measurements;"
    )

    cleaned = clean_sql(sql)

    assert not cleaned.endswith(";")


def test_clean_sql_removes_text_before_select():

    sql = (
        "Here is the SQL query: "
        "SELECT feeder_id "
        "FROM power_measurements;"
    )

    cleaned = clean_sql(sql)

    assert cleaned.startswith("SELECT")


def test_clean_sql_rejects_empty_sql():

    with pytest.raises(ValueError):

        clean_sql("")


# ============================================================
# VALID SQL TESTS
# ============================================================

def test_valid_select_query():

    sql = (
        "SELECT feeder_id, power "
        "FROM power_measurements"
    )

    assert validate_sql(sql) is True


def test_valid_average_query():

    sql = (
        "SELECT AVG(voltage) AS average_voltage "
        "FROM power_measurements"
    )

    assert validate_sql(sql) is True


def test_valid_grouped_query():

    sql = (
        "SELECT feeder_id, AVG(power) AS average_power "
        "FROM power_measurements "
        "GROUP BY feeder_id"
    )

    assert validate_sql(sql) is True


# ============================================================
# INVALID SQL TESTS
# ============================================================

def test_rejects_non_select_query():

    sql = (
        "DELETE FROM power_measurements"
    )

    with pytest.raises(ValueError):

        validate_sql(sql)


def test_rejects_insert_query():

    sql = (
        "INSERT INTO power_measurements "
        "(feeder_id) VALUES ('F_01')"
    )

    with pytest.raises(ValueError):

        validate_sql(sql)


def test_rejects_unknown_table():

    sql = (
        "SELECT * FROM customers"
    )

    with pytest.raises(ValueError):

        validate_sql(sql)


def test_rejects_multiple_statements():

    sql = (
        "SELECT feeder_id "
        "FROM power_measurements; "
        "DROP TABLE power_measurements"
    )

    with pytest.raises(ValueError):

        validate_sql(sql)


def test_rejects_query_without_from():

    sql = (
        "SELECT feeder_id"
    )

    with pytest.raises(ValueError):

        validate_sql(sql)
