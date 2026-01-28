import pandas as pd
import requests
import io
import streamlit as st
from datetime import datetime

from utils.utils_common import STATE_MAPPING

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_and_preprocess_data() -> tuple[pd.DataFrame, dict]:
    """
    **ETL Pipeline: Data Ingestion & Transformation Layer**
    
    Orchestrates the extraction of raw incident data, performs cleaning/validation,
    and constructs analytical features.
    
    **Process Flow:**
    1. **Extract**: Fetch live CSV from Everytown Research.
    2. **Transform**: 
       - Deduplicate records based on composite keys.
       - Validate geospatial variance.
       - Engineer features (School Year, Days Since, Severity Class).
    3. **Load**: Return optimized DataFrame for dashboard consumption.

    Returns:
        tuple: (processed_dataframe, quality_metrics_dict)
    """
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
        'data_freshness': None
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