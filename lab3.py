"""
data_loader.py
--------------
Loads and preprocesses the Titanic dataset from Seaborn.
Returns a clean DataFrame ready for all visualizations.
"""

import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import altair as alt


COLUMNS = ["survived", "pclass", "sex", "age", "fare", "embarked", "who", "alone"]


@st.cache_data(show_spinner="Loading Titanic dataset...")
def load_titanic() -> pd.DataFrame:
    """
    Load the Titanic dataset from Seaborn, select relevant columns,
    drop rows with any missing values, and add human-readable label columns.

    Returns
    -------
    pd.DataFrame
        Clean DataFrame with added 'survived_label' and 'pclass_label' columns.
    """
    df = sns.load_dataset("titanic")
    df = df[COLUMNS].dropna().reset_index(drop=True)

    # Human-readable labels used by several visualizations
    df["survived_label"] = df["survived"].map({0: "Did Not Survive", 1: "Survived"})
    df["pclass_label"] = df["pclass"].map({1: "1st", 2: "2nd", 3: "3rd"})

    return df
"""
visualizations/mosaic.py
------------------------
2.1 Mosaic Plot (Marimekko)

Purpose: Visualize the proportional relationship between two categorical
variables (Passenger Class and Survival Status) using a normalized stacked
bar chart. Each bar's height represents the proportion of total fare
contributed by survivors vs. non-survivors within that class.
"""


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

"""
visualizations/trellis.py
-------------------------
2.2 Trellis Display

Purpose: Compare the same scatter plot (Age vs Fare) across multiple
subgroups (Passenger Class) using small multiples. Each panel uses the
same axis scale, making cross-group comparison accurate and direct.
"""


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

"""
visualizations/heatmap.py
-------------------------
2.3 Heatmap

Purpose: Represent the average fare as colour intensity across a grid of
Passenger Class (x) × Gender (y) cells. Darker blue cells indicate higher
average fares, making patterns visible at a glance.
"""


def render(df):
    st.header("2.3 Heatmap")
    st.write("Average fare for each Passenger Class and Gender combination.")

    # Aggregate: mean fare per class × gender
    heat_data = (
        df.groupby(["pclass_label", "sex"])["fare"]
        .mean()
        .reset_index()
        .rename(columns={"fare": "avg_fare"})
    )

    chart = (
        alt.Chart(heat_data)
        .mark_rect()
        .encode(
            x=alt.X(
                "pclass_label:N",
                title="Passenger Class",
                sort=["1st", "2nd", "3rd"],
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y("sex:N", title="Gender"),
            color=alt.Color(
                "avg_fare:Q",
                scale=alt.Scale(scheme="blues"),
                legend=alt.Legend(title="Avg Fare (£)"),
            ),
            tooltip=[
                alt.Tooltip("pclass_label:N", title="Class"),
                alt.Tooltip("sex:N", title="Gender"),
                alt.Tooltip("avg_fare:Q", title="Avg Fare (£)", format=".2f"),
            ],
        )
        .properties(
            width=500,
            height=200,
            title="Heatmap: Average Fare by Class and Gender",
        )
    )

    st.altair_chart(chart, use_container_width=True)
    st.write(
        "Darker blue cells indicate higher average fares. "
        "Hover over any cell to see the exact value."
    )
    st.info(
        "💡 **Insight:** Female passengers in 1st class paid the highest average fare. "
        "Gender differences narrow significantly in 3rd class, where fares are low for all."
    )
    st.caption(
        "Task: Which Class and Gender combination has the highest average fare? "
        "Does gender always correlate with fare differences?"
    )

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
"""
visualizations/parallel.py
--------------------------
2.5 Parallel Coordinate Plot

Purpose: Draw each passenger record as a line crossing four vertical axes
(age, fare, pclass, survived). Line colour encodes survival status.
Clusters of lines reveal shared patterns; crossing lines indicate inverse
relationships. Supports interactive brushing (drag on any axis to filter).
"""

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
    
