"""
visualizations/grand_tour.py
-----------------------------
2.6 Grand Tour (3D Scatter Plot)

Purpose: Add a third spatial dimension (z=pclass) to reveal structure
hidden in 2D views. Users can rotate, zoom, and pan the interactive chart
to explore the point cloud from multiple angles and discover clusters or
outliers not visible from a single viewpoint.
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.header("2.6 Grand Tour: 3D Scatter Plot")
    st.write(
        "Explore age, fare, and pclass in a rotatable 3D space. "
        "Click and drag to rotate the view."
    )

    fig = px.scatter_3d(
        df,
        x="age",
        y="fare",
        z="pclass",
        color="survived_label",
        symbol="sex",
        size="fare",
        size_max=14,
        opacity=0.75,
        hover_data=["embarked", "who"],
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="3D Scatter: Age vs Fare vs Passenger Class",
    )
    fig.update_layout(
        scene=dict(
            xaxis_title="Age (years)",
            yaxis_title="Fare (£)",
            zaxis_title="Passenger Class",
        ),
        legend_title="Survived",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "Rotate the chart by clicking and dragging. Zoom with the scroll wheel. "
        "Color represents survival status, shape represents gender, "
        "and point size represents fare amount."
    )
    st.info(
        "💡 **Insight:** Rotating to view the Fare–Class plane clearly separates survivors "
        "(teal) at high fare / pclass=1 from non-survivors (orange) at low fare / pclass=3. "
        "Several high-fare outliers in 1st class appear as large isolated points."
    )
    st.caption(
        "Task: Rotate the chart to find the angle that best separates the survival groups. "
        "Can you identify any high-fare outliers in 3rd class?"
    )
