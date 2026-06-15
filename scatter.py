"""
visualizations/scatter.py
-------------------------
2.4 Multivariate Scatter Plot

Purpose: Encode five variables simultaneously in a single 2D chart using
position (x=age, y=fare), colour (survival), shape (gender), and point
size (passenger class). Reveals multi-attribute patterns at a glance.
"""

import altair as alt
import streamlit as st


def render(df):
    st.header("2.4 Multivariate Scatter Plot")
    st.write(
        "Relationships between age, fare, pclass, sex, and survival "
        "visualized using position, color, shape, and size."
    )

    chart = (
        alt.Chart(df)
        .mark_point(filled=True, opacity=0.75)
        .encode(
            x=alt.X("age:Q", title="Age (years)"),
            y=alt.Y("fare:Q", title="Fare (£)"),
            color=alt.Color(
                "survived_label:N",
                scale=alt.Scale(scheme="set1"),
                legend=alt.Legend(title="Survived"),
            ),
            shape=alt.Shape(
                "sex:N",
                legend=alt.Legend(title="Gender"),
            ),
            size=alt.Size(
                "pclass:Q",
                scale=alt.Scale(range=[30, 300]),
                legend=alt.Legend(title="Pclass (size)"),
            ),
            tooltip=["age", "fare", "sex", "survived_label", "pclass_label", "embarked"],
        )
        .properties(
            width=650,
            height=420,
            title="Multivariate Scatter: Age vs Fare "
                  "(color=Survival, shape=Gender, size=Class)",
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
    st.write(
        "Each point encodes 5 variables: x position (age), y position (fare), "
        "color (survival), shape (gender), and size (passenger class). "
        "Hover over points for full details. Scroll to zoom, click and drag to pan."
    )
    st.info(
        "💡 **Insight:** High-fare survivors (red) cluster among younger-to-middle-aged "
        "female passengers (circles) with small point sizes (1st class), confirming the "
        "'women and children first' evacuation pattern."
    )
    st.caption(
        "Task: Do female survivors tend to be younger or older? "
        "Do larger points (3rd class) survive more or less often?"
    )
