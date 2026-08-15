def generate_answer(question, columns, results):
    """
    Convert database results into a concise,
    human-readable answer.

    The database result is the source of truth.
    No additional LLM call is required.
    """

    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not results:
        return (
            "I couldn't find any matching records "
            "in the smart-grid database."
        )

    # --------------------------------------------------------
    # Convert database rows into dictionaries
    # --------------------------------------------------------

    records = []

    for row in results:

        record = {}

        for column, value in zip(columns, row):
            record[column] = value

        records.append(record)

    # --------------------------------------------------------
    # Single result
    # --------------------------------------------------------

    if len(records) == 1:

        record = records[0]

        # ----------------------------------------------------
        # Feeder result
        # ----------------------------------------------------

        if "feeder_id" in record:

            feeder = record["feeder_id"]

            if "power" in record:
                return (
                    f"Feeder {feeder} has a power "
                    f"reading of {record['power']}."
                )

            if "voltage" in record:
                return (
                    f"Feeder {feeder} has a voltage "
                    f"reading of {record['voltage']}."
                )

            if "current" in record:
                return (
                    f"Feeder {feeder} has a current "
                    f"reading of {record['current']}."
                )

            if "energy_consumption" in record:
                return (
                    f"Feeder {feeder} has an energy "
                    f"consumption of "
                    f"{record['energy_consumption']}."
                )

        # ----------------------------------------------------
        # Transformer result
        # ----------------------------------------------------

        if "transformer_id" in record:

            transformer = record["transformer_id"]

            if "power" in record:
                return (
                    f"Transformer {transformer} has a power "
                    f"reading of {record['power']}."
                )

            if "voltage" in record:
                return (
                    f"Transformer {transformer} has a voltage "
                    f"reading of {record['voltage']}."
                )

            if "current" in record:
                return (
                    f"Transformer {transformer} has a current "
                    f"reading of {record['current']}."
                )

            if "energy_consumption" in record:
                return (
                    f"Transformer {transformer} has an energy "
                    f"consumption of "
                    f"{record['energy_consumption']}."
                )

        # ----------------------------------------------------
        # Single aggregate value
        # ----------------------------------------------------

        if len(record) == 1:

            column = columns[0]
            value = record[column]

            readable_name = column.replace(
                "_",
                " "
            )

            return (
                f"The {readable_name} is {value}."
            )

        # ----------------------------------------------------
        # Generic single result
        # ----------------------------------------------------

        values = []

        for column in columns:

            readable_column = column.replace(
                "_",
                " "
            )

            values.append(
                f"{readable_column}: {record[column]}"
            )

        return "The result is " + ", ".join(values) + "."

    # --------------------------------------------------------
    # Multiple results
    # --------------------------------------------------------

    lines = []

    for record in records:

        values = []

        for column in columns:

            readable_column = column.replace(
                "_",
                " "
            )

            values.append(
                f"{readable_column}: {record[column]}"
            )

        lines.append(
            " | ".join(values)
        )

    return (
        "Here are the matching smart-grid measurements:\n\n"
        + "\n".join(lines)
    )
