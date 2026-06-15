"""
visualizations/parallel.py
--------------------------
2.5 Parallel Coordinate Plot

Purpose: Draw each passenger record as a line crossing four vertical axes
(age, fare, pclass, survived). Line colour encodes survival status.
Clusters of lines reveal shared patterns; crossing lines indicate inverse
relationships. Supports interactive brushing (drag on any axis to filter).
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.header("2.5 Parallel Coordinate Plot")
    st.write(
        "Each line represents one passenger record traced across "
        "age, fare, pclass, and survived axes."
    )

    fig = px.parallel_coordinates(
        df,
        dimensions=["age", "fare", "pclass", "survived"],
        color="survived",
        color_continuous_scale=px.colors.diverging.RdYlGn,
        labels={
            "age": "Age",
            "fare": "Fare (£)",
            "pclass": "Passenger Class",
            "survived": "Survived (0=No, 1=Yes)",
        },
        title="Parallel Coordinate Plot: Age, Fare, Class, and Survival",
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Survived",
            tickvals=[0, 1],
            ticktext=["No", "Yes"],
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "Green lines are survivors; red lines did not survive. "
        "Lines cluster together when records share similar patterns. "
        "**Drag on any axis** to filter and highlight subsets of data."
    )
    st.info(
        "💡 **Insight:** Filtering survivors (drag the 'survived' axis to 1) reveals "
        "they cluster at pclass=1 and higher fares. Non-survivors dominate pclass=3 "
        "with low fares. Age alone is a weaker predictor of survival."
    )
    st.caption(
        "Task: Drag the tip axis to select only fares above £50. "
        "Which passenger class is most common for high-fare passengers?"
    )
