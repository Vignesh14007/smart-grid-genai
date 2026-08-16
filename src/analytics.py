from query_engine import get_connection


def get_dashboard_data():
    """
    Fetch summary statistics and chart data
    from the smart-grid database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Overall statistics
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_records,
            AVG(power) AS average_power,
            AVG(voltage) AS average_voltage,
            AVG(current) AS average_current,
            SUM(energy_consumption) AS total_energy
        FROM power_measurements;
        """
    )

    summary = cursor.fetchone()

    # --------------------------------------------------------
    # Feeder power
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            feeder_id,
            AVG(power) AS average_power
        FROM power_measurements
        GROUP BY feeder_id
        ORDER BY average_power DESC;
        """
    )

    feeder_power = cursor.fetchall()

    # --------------------------------------------------------
    # Transformer power
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            transformer_id,
            AVG(power) AS average_power
        FROM power_measurements
        GROUP BY transformer_id
        ORDER BY average_power DESC;
        """
    )

    transformer_power = cursor.fetchall()

    # --------------------------------------------------------
    # Highest power feeder
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            feeder_id,
            MAX(power) AS highest_power
        FROM power_measurements
        GROUP BY feeder_id
        ORDER BY highest_power DESC
        LIMIT 1;
        """
    )

    highest_feeder = cursor.fetchone()

    # --------------------------------------------------------
    # Lowest power feeder
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            feeder_id,
            MIN(power) AS lowest_power
        FROM power_measurements
        GROUP BY feeder_id
        ORDER BY lowest_power ASC
        LIMIT 1;
        """
    )

    lowest_feeder = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "summary": summary,
        "feeder_power": feeder_power,
        "transformer_power": transformer_power,
        "highest_feeder": highest_feeder,
        "lowest_feeder": lowest_feeder,
    }
