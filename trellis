"""
visualizations/trellis.py
-------------------------
2.2 Trellis Display

Purpose: Compare the same scatter plot (Age vs Fare) across multiple
subgroups (Passenger Class) using small multiples. Each panel uses the
same axis scale, making cross-group comparison accurate and direct.
"""

import altair as alt
import streamlit as st


def render(df):
    st.header("2.2 Trellis Display")
    st.write("Scatter plots of Age vs Fare, one panel per Passenger Class.")

    chart = (
        alt.Chart(df)
        .mark_circle(size=55, opacity=0.65)
        .encode(
            x=alt.X("age:Q", title="Age (years)"),
            y=alt.Y("fare:Q", title="Fare (£)"),
            color=alt.Color(
                "survived_label:N",
                scale=alt.Scale(scheme="set1"),
                legend=alt.Legend(title="Survived"),
            ),
            tooltip=["age", "fare", "sex", "pclass_label", "survived_label"],
        )
        .facet(
            facet=alt.Facet(
                "pclass_label:N",
                title="Passenger Class",
                sort=["1st", "2nd", "3rd"],
            ),
            columns=3,
        )
        .properties(title="Trellis: Age vs Fare by Passenger Class")
    )

    st.altair_chart(chart, use_container_width=True)
    st.write(
        "Each panel shows the Age vs Fare relationship for one passenger class. "
        "Notice how fare variance increases dramatically in 1st class."
    )
    st.info(
        "💡 **Insight:** 1st class has the widest fare spread — older, wealthier passengers "
        "paid very high fares. 3rd class fares cluster tightly near zero regardless of age."
    )
    st.caption(
        "Task: Which class shows the strongest positive relationship between age and fare?"
    )
