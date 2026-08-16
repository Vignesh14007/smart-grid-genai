from query_engine import get_connection


def get_dashboard_data():
    """
    Fetch overall smart-grid analytics.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ====================================================
        # OVERALL SUMMARY
        # ====================================================

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

        # ====================================================
        # FEEDER POWER
        # ====================================================

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

        # ====================================================
        # TRANSFORMER POWER
        # ====================================================

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

        # ====================================================
        # HIGHEST POWER FEEDER
        # ====================================================

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

        # ====================================================
        # LOWEST POWER FEEDER
        # ====================================================

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

        # ====================================================
        # VOLTAGE BY FEEDER
        # ====================================================

        cursor.execute(
            """
            SELECT
                feeder_id,
                AVG(voltage) AS average_voltage
            FROM power_measurements
            GROUP BY feeder_id
            ORDER BY average_voltage DESC;
            """
        )

        feeder_voltage = cursor.fetchall()

        # ====================================================
        # CURRENT BY FEEDER
        # ====================================================

        cursor.execute(
            """
            SELECT
                feeder_id,
                AVG(current) AS average_current
            FROM power_measurements
            GROUP BY feeder_id
            ORDER BY average_current DESC;
            """
        )

        feeder_current = cursor.fetchall()

        # ====================================================
        # ENERGY BY FEEDER
        # ====================================================

        cursor.execute(
            """
            SELECT
                feeder_id,
                SUM(energy_consumption) AS total_energy
            FROM power_measurements
            GROUP BY feeder_id
            ORDER BY total_energy DESC;
            """
        )

        feeder_energy = cursor.fetchall()

        # ====================================================
        # RETURN ALL DATA
        # ====================================================

        return {
            "summary": summary,
            "feeder_power": feeder_power,
            "transformer_power": transformer_power,
            "highest_feeder": highest_feeder,
            "lowest_feeder": lowest_feeder,
            "feeder_voltage": feeder_voltage,
            "feeder_current": feeder_current,
            "feeder_energy": feeder_energy
        }

    finally:

        cursor.close()
        connection.close()
