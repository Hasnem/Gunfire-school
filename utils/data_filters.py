import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply clean, organized filters through the sidebar.
    
    Args:
        df: Original dataframe with incident data
        
    Returns:
        Filtered dataframe based on user selections
    """
    # Store original length for summary
    original_length = len(df)
    
    st.sidebar.markdown("## 🔍 Data Filters")
    
    # Quick presets at the top for easy access
    preset = st.sidebar.selectbox(
        "Quick Presets",
        ["All Data", "Last Year Complete", "Last 5 Years", "Fatal Only", 
         "Mass Casualties", "Current Year"],
        help="Quick filter presets"
    )
    
    if preset != "All Data":
        df = apply_preset(df, preset)
    
    st.sidebar.markdown("---")
    
    # Time filters
    df = apply_time_filters(df)
    
    # Location filters  
    df = apply_location_filters(df)
    
    # Severity filters
    df = apply_severity_filters(df)
    
    # Show filter summary
    display_filter_summary(df, original_length)
    
    return df


def apply_time_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply time-based filters with date range option."""
    
    with st.sidebar.expander("📅 Time Period", expanded=True):
        
        # Time filter type
        time_filter_type = st.radio(
            "Filter by",
            ["All Time", "Date Range", "Specific Years"],
            horizontal=True
        )
        
        if time_filter_type == "Date Range":
            # Date range picker
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=df['Incident Date'].min(),
                    min_value=df['Incident Date'].min().date(),
                    max_value=df['Incident Date'].max().date()
                )
            
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=df['Incident Date'].max(),
                    min_value=df['Incident Date'].min().date(),
                    max_value=df['Incident Date'].max().date()
                )
            
            # Apply date range filter
            df = df[(df['Incident Date'].dt.date >= start_date) & 
                   (df['Incident Date'].dt.date <= end_date)]
            
        elif time_filter_type == "Specific Years":
            # Year selector
            years = sorted(df['Year'].unique(), reverse=True)
            selected_years = st.multiselect(
                "Select Years",
                years,
                default=years[:5]  # Default to last 5 years
            )
            
            if selected_years:
                df = df[df['Year'].isin(selected_years)]
                
                # Warning for current year
                current_year = datetime.now().year
                if current_year in selected_years:
                    st.warning(f"⚠️ {current_year} data is incomplete")
        
        # Optional: Filter by months
        if st.checkbox("Filter by months", value=False):
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            # Quick selections
            col1, col2 = st.columns(2)
            with col1:
                if st.button("School Months", width='stretch'):
                    selected_months = ['Sep', 'Oct', 'Nov', 'Dec', 
                                     'Jan', 'Feb', 'Mar', 'Apr', 'May']
                else:
                    selected_months = None
            with col2:
                if st.button("Summer", width='stretch'):
                    selected_months = ['Jun', 'Jul', 'Aug']
                else:
                    selected_months = None
            
            if selected_months is None:
                selected_months = st.multiselect("Select months", months, default=months)
            
            if selected_months:
                df = df[df['Month'].isin(selected_months)]
    
    return df


def apply_location_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply location-based filters."""
    
    with st.sidebar.expander("📍 Location", expanded=False):
        
        # Location filter type
        location_type = st.radio(
            "Show",
            ["All Locations", "Specific States", "Top N States"],
            horizontal=True
        )
        
        if location_type == "Specific States":
            states = sorted(df['State_name'].dropna().unique())
            selected_states = st.multiselect(
                "Select states",
                states,
                help="Choose one or more states"
            )
            
            if selected_states:
                df = df[df['State_name'].isin(selected_states)]
                
        elif location_type == "Top N States":
            n_states = st.slider(
                "Number of top states",
                min_value=5,
                max_value=20,
                value=10,
                step=5
            )
            
            # Get top N states
            top_states = df['State_name'].value_counts().head(n_states).index.tolist()
            df = df[df['State_name'].isin(top_states)]
            
            # Show which states
            with st.container():
                st.caption(f"Showing: {', '.join(top_states[:3])}...")
    
    return df


def apply_severity_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply incident severity filters."""
    
    with st.sidebar.expander("⚠️ Incident Type", expanded=False):
        
        # Severity level
        severity = st.select_slider(
            "Minimum Severity",
            options=["All", "With Casualties", "Fatal", "Mass Casualty"],
            value="All"
        )
        
        if severity == "With Casualties":
            df = df[df['Total_Casualties'] > 0]
        elif severity == "Fatal":
            df = df[df['Is_Fatal'] == True]
        elif severity == "Mass Casualty":
            df = df[df['Total_Casualties'] >= 4]
        
        # Intent filter (if available)
        if 'Intent' in df.columns and st.checkbox("Filter by intent"):
            intents = sorted(df['Intent'].dropna().unique())
            selected_intents = st.multiselect(
                "Select intent types",
                intents
            )
            
            if selected_intents:
                df = df[df['Intent'].isin(selected_intents)]
    
    return df


def apply_preset(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    """Apply preset filters."""
    
    current_year = datetime.now().year
    
    if preset == "Last Year Complete":
        df = df[df['Year'] == current_year - 1]
        
    elif preset == "Last 5 Years":
        df = df[df['Year'] >= current_year - 5]
        
    elif preset == "Fatal Only":
        df = df[df['Is_Fatal'] == True]
        
    elif preset == "Mass Casualties":
        df = df[df['Total_Casualties'] >= 4]
        
    elif preset == "Current Year":
        df = df[df['Year'] == current_year]
    
    return df


def display_filter_summary(df_filtered: pd.DataFrame, original_count: int):
    """Display a clean filter summary."""
    
    st.sidebar.markdown("---")
    
    filtered_count = len(df_filtered)
    reduction_pct = ((original_count - filtered_count) / original_count * 100) if original_count > 0 else 0
    
    # Simple metrics
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric("Showing", f"{filtered_count:,}")
    
    with col2:
        st.metric("Filtered", f"-{reduction_pct:.0f}%")
    
    # Key active filters
    if filtered_count < original_count:
        active_filters = []
        
        # Check years
        if hasattr(df_filtered, 'Year'):
            years = sorted(df_filtered['Year'].unique())
            if len(years) <= 3:
                active_filters.append(f"Years: {', '.join(map(str, years))}")
            else:
                active_filters.append(f"Years: {years[0]}-{years[-1]}")
        
        # Check states
        states_shown = df_filtered['State_name'].nunique()
        if states_shown < 50:
            active_filters.append(f"States: {states_shown}")
        
        # Show active filters
        if active_filters:
            st.sidebar.caption("Active filters:")
            for filter_text in active_filters:
                st.sidebar.caption(f"• {filter_text}")