"""
data_loader.py
--------------
Loads and preprocesses the Titanic dataset from Seaborn.
Returns a clean DataFrame ready for all visualizations.
"""

import pandas as pd
import seaborn as sns
import streamlit as st


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
