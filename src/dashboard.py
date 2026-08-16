import streamlit as st
import pandas as pd

from src.analytics import get_dashboard_data


def show_dashboard():
    """
    Display the Smart Grid analytics dashboard.
    """

    st.markdown("## ⚡ Grid Analytics")

    st.caption(
        "Overview of power, voltage, current, "
        "energy consumption, feeders, and transformers."
    )

    data = get_dashboard_data()

    summary = data["summary"]

    total_records = summary[0]
    average_power = summary[1]
    average_voltage = summary[2]
    average_current = summary[3]
    total_energy = summary[4]

    highest_feeder = data["highest_feeder"]
    lowest_feeder = data["lowest_feeder"]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # ENERGY + FEEDER HIGHLIGHTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # FEEDER POWER
    # --------------------------------------------------------

    st.markdown("### Feeder Power")

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

    # --------------------------------------------------------
    # TRANSFORMER POWER
    # --------------------------------------------------------

    st.markdown("### Transformer Power")

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

    # --------------------------------------------------------
    # FEEDER TABLE
    # --------------------------------------------------------

    st.markdown("### Feeder Summary")

    st.dataframe(
        feeder_data,
        use_container_width=True,
        hide_index=True
    )
