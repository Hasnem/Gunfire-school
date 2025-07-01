import pandas as pd
import numpy as np
import requests
import io
import streamlit as st
from datetime import datetime, timedelta
import time

from utils.utils_common import STATE_MAPPING

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_and_preprocess_data() -> tuple[pd.DataFrame, dict]:
    """
    Load and preprocess gunfire incident data with comprehensive quality tracking.
    
    Returns:
        tuple: (processed_dataframe, quality_metrics_dict)
    """
    start_time = time.time()
    
    # Data source configuration
    url = 'https://everytownresearch.org/wp-content/uploads/sites/4/etown-maps/gunfire-on-school-grounds/data.csv'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Fetch data with error handling
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {str(e)}")
        return pd.DataFrame(), {}
    
    # Load CSV data
    df = pd.read_csv(io.StringIO(resp.text))
    initial_rows = len(df)
    
    # Initialize quality tracking
    quality_metrics = {
        'initial_rows': initial_rows,
        'missing_dates': 0,
        'missing_coords': 0,
        'missing_narratives': 0,
        'duplicate_incidents': 0,
        'data_freshness': None,
        'load_time': 0
    }
    
    # 1. Parse and validate dates
    df['Incident Date'] = pd.to_datetime(df['Incident Date'], errors='coerce')
    quality_metrics['missing_dates'] = df['Incident Date'].isna().sum()
    
    # Calculate data freshness (days since most recent incident)
    if not df['Incident Date'].isna().all():
        latest_date = df['Incident Date'].max()
        days_old = (datetime.now() - latest_date).days
        quality_metrics['data_freshness'] = days_old
    
    # 2. Process geographic coordinates
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    quality_metrics['missing_coords'] = df[['Latitude', 'Longitude']].isna().any(axis=1).sum()
    
    # 3. Remove duplicate incidents
    duplicate_mask = df.duplicated(
        subset=['Incident Date', 'City', 'State', 'School name'], 
        keep='first'
    )
    quality_metrics['duplicate_incidents'] = duplicate_mask.sum()
    df = df[~duplicate_mask]
    
    # 4. Track narrative completeness
    quality_metrics['missing_narratives'] = df['Narrative'].isna().sum()
    
    # 5. Clean up unnecessary columns
    cols_to_drop = [
        'Source 2', 'URL 2', 'Source 3', 'URL 3', 
        'School Type', 'Created', 'Last Modified'
    ]
    df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)
    
    # 6. Create temporal features for analysis
    df['Year'] = df['Incident Date'].dt.year
    df['Month'] = df['Incident Date'].dt.strftime('%b')
    df['Month_Num'] = df['Incident Date'].dt.month
    df['DayOfWeek'] = df['Incident Date'].dt.strftime('%a')
    df['DayOfWeek_Num'] = df['Incident Date'].dt.dayofweek
    df['Quarter'] = df['Incident Date'].dt.quarter
    df['Days_Since_Incident'] = (datetime.now() - df['Incident Date']).dt.days
    
    # Academic year calculation (Aug-Jul cycle)
    df['School_Year'] = df.apply(
        lambda x: f"{x['Year']-1}-{x['Year']}" if x['Month_Num'] < 8 
        else f"{x['Year']}-{x['Year']+1}",
        axis=1
    )
    
    # 7. Standardize state names
    df['State_name'] = df['State'].map(STATE_MAPPING)
    
    # 8. Calculate severity metrics
    df['Total_Casualties'] = df['Number Killed'] + df['Number Wounded']
    df['Is_Fatal'] = df['Number Killed'] > 0
    df['Mass_Casualty'] = df['Total_Casualties'] >= 4  # FBI definition
    
    # 9. Create clear severity categories
    def classify_severity(row):
        """Classify incident severity based on casualties."""
        if row['Total_Casualties'] == 0:
            return 'No Casualties'
        elif row['Number Killed'] == 0:
            return 'Injuries Only'
        elif row['Number Killed'] == 1 and row['Number Wounded'] == 0:
            return 'Single Fatality'
        elif row['Total_Casualties'] >= 4:
            return 'Mass Casualty'
        else:
            return 'Multiple Casualties'
    
    df['Severity'] = df.apply(classify_severity, axis=1)
    
    # 10. Calculate time between incidents by state
    df['Days_Since_Previous'] = (
        df.sort_values('Incident Date')
        .groupby('State')['Incident Date']
        .diff()
        .dt.days
    )
    
    # Finalize quality metrics
    quality_metrics['load_time'] = round(time.time() - start_time, 2)
    quality_metrics['final_rows'] = len(df)
    
    # Calculate overall data completeness score
    quality_metrics['completeness_score'] = round(
        (1 - (quality_metrics['missing_dates'] + 
              quality_metrics['missing_coords'] + 
              quality_metrics['missing_narratives']) / 
         (initial_rows * 3)) * 100, 
        1
    )
    
    return df, quality_metrics


@st.cache_data
def calculate_rolling_statistics(df: pd.DataFrame, window_days: int = 365) -> pd.DataFrame:
    """
    Calculate rolling statistics for trend analysis.
    
    Args:
        df: Input dataframe with incident data
        window_days: Number of days for rolling window (default: 365)
    
    Returns:
        DataFrame with rolling statistics by date
    """
    if df.empty:
        return pd.DataFrame()
    
    df_sorted = df.sort_values('Incident Date').copy()
    
    # Create continuous daily time series
    date_range = pd.date_range(
        start=df_sorted['Incident Date'].min(),
        end=df_sorted['Incident Date'].max(),
        freq='D'
    )
    
    # Aggregate incidents by day
    daily_counts = df_sorted.groupby(df_sorted['Incident Date'].dt.date).agg({
        'ID': 'count',
        'Number Killed': 'sum',
        'Number Wounded': 'sum',
        'Total_Casualties': 'sum'
    }).reindex(date_range.date, fill_value=0)
    
    # Calculate rolling statistics
    rolling_stats = pd.DataFrame(index=daily_counts.index)
    
    # Rolling sums
    rolling_stats['incidents_rolling'] = (
        daily_counts['ID']
        .rolling(window=window_days, min_periods=1)
        .sum()
    )
    rolling_stats['killed_rolling'] = (
        daily_counts['Number Killed']
        .rolling(window=window_days, min_periods=1)
        .sum()
    )
    rolling_stats['wounded_rolling'] = (
        daily_counts['Number Wounded']
        .rolling(window=window_days, min_periods=1)
        .sum()
    )
    rolling_stats['casualties_rolling'] = (
        daily_counts['Total_Casualties']
        .rolling(window=window_days, min_periods=1)
        .sum()
    )
    
    # Calculate 30-day rate of change
    rolling_stats['incidents_change_rate'] = (
        rolling_stats['incidents_rolling']
        .pct_change(periods=30)
        .fillna(0) * 100
    )
    
    return rolling_stats


@st.cache_data
def get_statistical_summary(df: pd.DataFrame) -> dict:
    """
    Generate comprehensive statistical summary of the data.
    
    Args:
        df: Processed incident dataframe
    
    Returns:
        Dictionary containing categorized statistics
    """
    if df.empty:
        return {}
    
    summary = {
        'temporal': {},
        'geographic': {},
        'severity': {},
        'patterns': {}
    }
    
    # Temporal statistics
    yearly_counts = df.groupby('Year').size()
    if not yearly_counts.empty:
        summary['temporal'] = {
            'avg_incidents_per_year': yearly_counts.mean(),
            'year_with_most_incidents': yearly_counts.idxmax(),
            'avg_days_between_incidents': df['Days_Since_Previous'].mean() if 'Days_Since_Previous' in df else None,
            'median_days_between_incidents': df['Days_Since_Previous'].median() if 'Days_Since_Previous' in df else None,
            'trend_direction': 'increasing' if yearly_counts.iloc[-5:].mean() > yearly_counts.iloc[:5].mean() else 'decreasing'
        }
    
    # Geographic statistics
    summary['geographic'] = {
        'states_affected': df['State'].nunique(),
        'cities_affected': df['City'].nunique(),
        'schools_affected': df['School name'].nunique(),
        'concentration_index': (
            df.groupby('State').size().std() / 
            df.groupby('State').size().mean()
            if df.groupby('State').size().mean() > 0 else 0
        )
    }
    
    # Severity statistics
    total_incidents = len(df)
    if total_incidents > 0:
        summary['severity'] = {
            'fatality_rate': (df['Is_Fatal'].sum() / total_incidents) * 100,
            'avg_casualties_per_incident': df['Total_Casualties'].mean(),
            'mass_casualty_rate': (df['Mass_Casualty'].sum() / total_incidents) * 100,
            'avg_killed_when_fatal': (
                df[df['Is_Fatal']]['Number Killed'].mean() 
                if df['Is_Fatal'].sum() > 0 else 0
            ),
            'avg_wounded_when_injuries': (
                df[df['Number Wounded'] > 0]['Number Wounded'].mean()
                if (df['Number Wounded'] > 0).sum() > 0 else 0
            )
        }
    
    # Pattern statistics
    summary['patterns'] = {
        'most_common_day': (
            df['DayOfWeek'].mode().iloc[0] 
            if not df['DayOfWeek'].mode().empty else 'N/A'
        ),
        'most_common_month': (
            df['Month'].mode().iloc[0] 
            if not df['Month'].mode().empty else 'N/A'
        ),
        'most_common_intent': (
            df['Intent'].mode().iloc[0] 
            if 'Intent' in df and not df['Intent'].mode().empty else 'N/A'
        ),
        'weekend_vs_weekday_ratio': (
            len(df[df['DayOfWeek_Num'].isin([5,6])]) / 
            len(df[df['DayOfWeek_Num'].isin([0,1,2,3,4])])
            if len(df[df['DayOfWeek_Num'].isin([0,1,2,3,4])]) > 0 else 0
        )
    }
    
    return summary