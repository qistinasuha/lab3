"""
visualizations/mosaic.py
------------------------
2.1 Mosaic Plot (Marimekko)

Purpose: Visualize the proportional relationship between two categorical
variables (Passenger Class and Survival Status) using a normalized stacked
bar chart. Each bar's height represents the proportion of total fare
contributed by survivors vs. non-survivors within that class.
"""

import altair as alt
import streamlit as st


def render(df):
    st.header("2.1 Mosaic Plot (Marimekko)")
    st.write("Shows fare distribution grouped by Passenger Class and Survival Status.")

    # Aggregate: sum of fare per class × survival combination
    mosaic_data = (
        df.groupby(["pclass_label", "survived_label"])["fare"]
        .sum()
        .reset_index()
    )

    chart = (
        alt.Chart(mosaic_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "pclass_label:N",
                title="Passenger Class",
                sort=["1st", "2nd", "3rd"],
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "fare:Q",
                stack="normalize",
                title="Proportion of Total Fare",
            ),
            color=alt.Color(
                "survived_label:N",
                scale=alt.Scale(scheme="tableau10"),
                legend=alt.Legend(title="Survival Status"),
            ),
            tooltip=["pclass_label", "survived_label", "fare"],
        )
        .properties(
            width=600,
            height=400,
            title="Mosaic Plot: Fare Distribution by Class and Survival",
        )
    )

    st.altair_chart(chart, use_container_width=True)
    st.write(
        "Each bar shows the proportion of total fare contributed by survivors vs. "
        "non-survivors within each passenger class."
    )
    st.info(
        "💡 **Insight:** In 1st class, survivors contributed a noticeably higher "
        "proportion of fare, reflecting the higher survival rate of wealthier passengers. "
        "3rd class shows the opposite — non-survivors dominate."
    )
    st.caption("Task: Which passenger class shows the highest proportion of survivors?")
