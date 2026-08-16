import pandas as pd
import streamlit as st

from src.analytics import get_dashboard_data


def show_dashboard(question_data=None):
    """
    Display the Smart Grid analytics dashboard.

    If question_data is available, display
    question-specific analytics first.
    """

    st.markdown("## ⚡ Grid Analytics")

    st.caption(
        "Overview of power, voltage, current, "
        "energy consumption, feeders, and transformers."
    )

    # ========================================================
    # LOAD DATABASE ANALYTICS
    # ========================================================

    data = get_dashboard_data()

    summary = data["summary"]

    total_records = summary[0]
    average_power = summary[1]
    average_voltage = summary[2]
    average_current = summary[3]
    total_energy = summary[4]

    highest_feeder = data["highest_feeder"]
    lowest_feeder = data["lowest_feeder"]

    # ========================================================
    # QUESTION-SPECIFIC ANALYTICS
    # ========================================================

    if question_data:

        show_question_analytics(
            question_data,
            data
        )

        st.divider()

        st.markdown("## 📊 Overall Grid Overview")

    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Records",
            f"{total_records:,}"
        )

    with col2:

        st.metric(
            "Average Power",
            f"{average_power:.2f}"
        )

    with col3:

        st.metric(
            "Average Voltage",
            f"{average_voltage:.2f}"
        )

    with col4:

        st.metric(
            "Average Current",
            f"{average_current:.2f}"
        )

    st.divider()

    # ========================================================
    # ENERGY + FEEDER HIGHLIGHTS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Energy",
            f"{total_energy:,.2f}"
        )

    with col2:

        st.metric(
            "Highest Power Feeder",
            highest_feeder[0],
            f"{highest_feeder[1]:.2f}"
        )

    with col3:

        st.metric(
            "Lowest Power Feeder",
            lowest_feeder[0],
            f"{lowest_feeder[1]:.2f}"
        )

    st.divider()

    # ========================================================
    # FEEDER POWER
    # ========================================================

    st.markdown("### ⚡ Feeder Power")

    feeder_data = pd.DataFrame(
        data["feeder_power"],
        columns=[
            "Feeder",
            "Average Power"
        ]
    )

    st.bar_chart(
        feeder_data.set_index("Feeder")
    )

    # ========================================================
    # TRANSFORMER POWER
    # ========================================================

    st.markdown("### 🔌 Transformer Power")

    transformer_data = pd.DataFrame(
        data["transformer_power"],
        columns=[
            "Transformer",
            "Average Power"
        ]
    )

    st.bar_chart(
        transformer_data.set_index("Transformer")
    )

    # ========================================================
    # FEEDER VOLTAGE
    # ========================================================

    st.markdown("### 🔋 Feeder Voltage")

    voltage_data = pd.DataFrame(
        data["feeder_voltage"],
        columns=[
            "Feeder",
            "Average Voltage"
        ]
    )

    st.bar_chart(
        voltage_data.set_index("Feeder")
    )

    # ========================================================
    # FEEDER CURRENT
    # ========================================================

    st.markdown("### 🔌 Feeder Current")

    current_data = pd.DataFrame(
        data["feeder_current"],
        columns=[
            "Feeder",
            "Average Current"
        ]
    )

    st.bar_chart(
        current_data.set_index("Feeder")
    )

    # ========================================================
    # FEEDER ENERGY
    # ========================================================

    st.markdown("### ⚡ Feeder Energy Consumption")

    energy_data = pd.DataFrame(
        data["feeder_energy"],
        columns=[
            "Feeder",
            "Total Energy"
        ]
    )

    st.bar_chart(
        energy_data.set_index("Feeder")
    )

    # ========================================================
    # FEEDER TABLE
    # ========================================================

    st.markdown("### 📋 Feeder Summary")

    st.dataframe(
        feeder_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# QUESTION-SPECIFIC ANALYTICS
# ============================================================

def show_question_analytics(question_data, dashboard_data):
    """
    Display analytics specifically related to
    the user's latest completed question.
    """

    question = question_data.get(
        "question",
        ""
    )

    answer = question_data.get(
        "answer",
        ""
    )

    columns = question_data.get(
        "columns",
        []
    )

    results = question_data.get(
        "results",
        []
    )

    question_lower = question.lower()

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown("## 🔎 Analysis of Your Question")

    st.info(
        f"**Question:** {question}"
    )

    st.success(
        answer
    )

    # ========================================================
    # NO RESULTS
    # ========================================================

    if not results:

        st.warning(
            "No matching database records were returned "
            "for this question."
        )

        return

    # ========================================================
    # RESULT DATAFRAME
    # ========================================================

    result_df = pd.DataFrame(
        results,
        columns=columns
    )

    st.markdown("### Query Result")

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # FEEDER POWER
    # ========================================================

    if (
        "feeder" in question_lower
        and "power" in question_lower
    ):

        st.markdown(
            "### ⚡ Feeder Power Analysis"
        )

        feeder_data = dashboard_data[
            "feeder_power"
        ]

        chart_df = pd.DataFrame(
            feeder_data,
            columns=[
                "Feeder",
                "Average Power"
            ]
        )

        st.bar_chart(
            chart_df.set_index("Feeder")
        )

        # Highlight result

        if "feeder_id" in columns:

            feeder_id = results[0][
                columns.index("feeder_id")
            ]

            st.success(
                f"🏆 Selected feeder: **{feeder_id}**"
            )

        return

    # ========================================================
    # TRANSFORMER POWER
    # ========================================================

    if (
        "transformer" in question_lower
        and "power" in question_lower
    ):

        st.markdown(
            "### 🔌 Transformer Power Analysis"
        )

        transformer_data = dashboard_data[
            "transformer_power"
        ]

        chart_df = pd.DataFrame(
            transformer_data,
            columns=[
                "Transformer",
                "Average Power"
            ]
        )

        st.bar_chart(
            chart_df.set_index("Transformer")
        )

        if "transformer_id" in columns:

            transformer_id = results[0][
                columns.index("transformer_id")
            ]

            st.success(
                f"🏆 Selected transformer: "
                f"**{transformer_id}**"
            )

        return

    # ========================================================
    # VOLTAGE
    # ========================================================

    if "voltage" in question_lower:

        st.markdown(
            "### 🔋 Voltage Analysis"
        )

        voltage_data = dashboard_data[
            "feeder_voltage"
        ]

        chart_df = pd.DataFrame(
            voltage_data,
            columns=[
                "Feeder",
                "Average Voltage"
            ]
        )

        st.bar_chart(
            chart_df.set_index("Feeder")
        )

        return

    # ========================================================
    # CURRENT
    # ========================================================

    if "current" in question_lower:

        st.markdown(
            "### 🔌 Current Analysis"
        )

        current_data = dashboard_data[
            "feeder_current"
        ]

        chart_df = pd.DataFrame(
            current_data,
            columns=[
                "Feeder",
                "Average Current"
            ]
        )

        st.bar_chart(
            chart_df.set_index("Feeder")
        )

        return

    # ========================================================
    # ENERGY
    # ========================================================

    if (
        "energy" in question_lower
        or "consumption" in question_lower
    ):

        st.markdown(
            "### ⚡ Energy Consumption Analysis"
        )

        energy_data = dashboard_data[
            "feeder_energy"
        ]

        chart_df = pd.DataFrame(
            energy_data,
            columns=[
                "Feeder",
                "Total Energy"
            ]
        )

        st.bar_chart(
            chart_df.set_index("Feeder")
        )

        return

    # ========================================================
    # GENERIC RESULT
    # ========================================================

    st.markdown(
        "### 📊 Result Visualization"
    )

    numeric_columns = result_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        st.bar_chart(
            result_df[numeric_columns]
        )

    else:

        st.info(
            "This result does not contain a numeric "
            "measurement suitable for a chart."
        )
