import streamlit as st
import pandas as pd
from datetime import date
from typing import List, Tuple

def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    col1, col2, col3 = st.columns(3)
    with col1:
        states = sorted(df['State_name'].dropna().unique())
        selected_states = st.multiselect("State", states)
    with col2:
        intent_opts = sorted(df['Intent'].dropna().unique())
        selected_intent = st.multiselect("Intent", intent_opts)
    with col3:
        min_date, max_date = df['Incident Date'].min().date(), df['Incident Date'].max().date()
        today = date.today()
        default_end = max_date if today > max_date else today
        date_range = st.date_input("Incident Date Range", (min_date, default_end),
                                   min_value=min_date, max_value=max_date)
    return filter_data(df, selected_states, selected_intent, date_range)

def filter_data(df: pd.DataFrame, states: List[str], intent: List[str], date_range: Tuple[date,date]) -> pd.DataFrame:
    if states:
        df = df[df['State_name'].isin(states)]
    if intent:
        df = df[df['Intent'].isin(intent)]
    if date_range:
        start_date, end_date = date_range
        df = df[(df['Incident Date'] >= pd.to_datetime(start_date)) & (df['Incident Date'] <= pd.to_datetime(end_date))]
    return df

def filter_by_min_casualties(df: pd.DataFrame, min_cas: int) -> pd.DataFrame:
    if df.empty:
        return df
    df['Total_Casualties'] = df['Number Killed'] + df['Number Wounded']
    return df[df['Total_Casualties'] >= min_cas]

def export_filtered_data(df: pd.DataFrame):
    if df.empty:
        st.warning("No data to download with the current filters.")
        return
    csv_data = df.to_csv(index=False)
    st.download_button(
        "Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )
