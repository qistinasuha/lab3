"""
visualizations/sunburst.py
--------------------------
2.7 Sunburst Chart  (Additional / Extra Visualization)

Purpose: Display a three-level hierarchy — Passenger Class → Gender →
Survival Status — where each sector's size is proportional to total fare.
Supports interactive drill-down by clicking any sector to zoom in.

Why chosen: Complements the Mosaic plot by adding a third categorical level
and enabling hierarchical exploration not possible in a flat bar chart.
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.header("2.7 Sunburst Chart (Additional Visualization)")
    st.write(
        "Hierarchical breakdown of total fare by "
        "Passenger Class → Gender → Survival Status."
    )

    fig = px.sunburst(
        df,
        path=["pclass_label", "sex", "survived_label"],
        values="fare",
        color="survived_label",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Sunburst: Total Fare by Class → Gender → Survival",
    )
    fig.update_traces(textinfo="label+percent parent")

    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "Each ring level represents one level of the hierarchy: "
        "class (inner) → gender (middle) → survival (outer). "
        "Sector size is proportional to total fare paid. "
        "**Click any sector** to zoom into that sub-group."
    )
    st.info(
        "💡 **Insight:** Female survivors in 1st class dominate their sector's fare total, "
        "reflecting both higher ticket prices and higher survival rates. "
        "In 3rd class, non-survivors of both genders account for the majority of fare."
    )
    st.caption(
        "Task: Click into '3rd' class. Which gender has a higher proportion of survivors?"
    )
