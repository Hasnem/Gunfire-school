import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Optional, Union

# Comprehensive state mapping for US states and territories
STATE_MAPPING = {
    # Continental US
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    # Federal District and Territories
    'DC': 'District of Columbia', 'PR': 'Puerto Rico', 'GU': 'Guam', 'VI': 'Virgin Islands',
    'MP': 'Northern Mariana Islands', 'AS': 'American Samoa'
}

# Consistent color palette for the entire application
COLORS = {
    # Primary colors
    'primary': '#2c3e50',      # Dark blue-gray for main elements
    'secondary': '#34495e',    # Slightly lighter for secondary elements
    'accent': '#3498db',       # Bright blue for highlights
    
    # Status colors
    'success': '#27ae60',      # Green for positive metrics
    'warning': '#f39c12',      # Orange for warnings
    'danger': '#e74c3c',       # Red for critical data
    'info': '#3498db',         # Blue for informational
    
    # Neutral colors
    'light': '#ecf0f1',        # Light gray for backgrounds
    'dark': '#2c3e50',         # Dark for text
    'white': '#ffffff'         # Pure white
}


def display_header():
    """
    Display the main application header with title and source attribution.
    """
    header_html = """
        <div style="text-align: left; margin-bottom: 2rem;">
            <h1 style="color: #2c3e50; margin-bottom: 0.5rem; font-size: 2.5rem; font-weight: 600;">
                Gun Violence on U.S. School Grounds
            </h1>
            <p style="color: #7f8c8d; font-size: 1.1rem; margin: 0;">
                Comprehensive analysis powered by 
                <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/" 
                   target="_blank" 
                   style="color: #3498db; text-decoration: none; font-weight: 500;">
                   Everytown Research
                </a>
                data
            </p>
        </div>
    """
    st.html(header_html)


def display_metric_card(
    label: str, 
    value: str, 
    context: str = "", 
    color: str = "primary",
    icon: Optional[str] = None
) -> str:
    """
    Create a visually appealing metric card with consistent styling.
    
    Args:
        label: Metric label/title
        value: Main metric value to display
        context: Additional context or description
        color: Color theme from COLORS dict
        icon: Optional emoji or icon to display
        
    Returns:
        HTML string for the metric card
    """
    border_color = COLORS.get(color, COLORS['primary'])
    icon_html = f'<span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''
    
    return f"""
        <div style="
            background: #ffffff;
            border-left: 4px solid {border_color};
            padding: 1.25rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s;
            height: 100%;
        ">
            <div style="
                color: #7f8c8d; 
                font-size: 0.875rem; 
                font-weight: 600; 
                text-transform: uppercase; 
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
            ">
                {icon_html}{label}
            </div>
            <div style="
                color: #2c3e50; 
                font-size: 2.25rem; 
                font-weight: 700; 
                line-height: 1.1; 
                margin: 0.25rem 0;
            ">
                {value}
            </div>
            {f'<div style="color: #7f8c8d; font-size: 0.875rem; margin-top: 0.5rem;">{context}</div>' if context else ''}
        </div>
    """


def display_metric_cards(df: pd.DataFrame):
    """
    Display the main dashboard metrics in a clean card layout.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.warning("No data available to display metrics.")
        return
    
    # Calculate key metrics
    total_incidents = len(df)
    total_casualties = int(df["Total_Casualties"].sum())
    total_killed = int(df["Number Killed"].sum())
    total_wounded = int(df["Number Wounded"].sum())
    states_affected = df['State_name'].nunique()
    schools_affected = df['School name'].nunique()
    
    # Calculate additional context metrics
    avg_casualties = total_casualties / total_incidents if total_incidents > 0 else 0
    fatal_rate = (df['Is_Fatal'].sum() / total_incidents * 100) if total_incidents > 0 else 0
    
    # Display in responsive columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.html(
            display_metric_card(
                "Total Incidents",
                f"{total_incidents:,}",
                "Recorded events",
                "primary",
                "📊"
            )
        )
    
    with col2:
        casualty_context = f"{total_killed:,} killed • {total_wounded:,} wounded"
        st.html(
            display_metric_card(
                "Total Casualties",
                f"{total_casualties:,}",
                casualty_context,
                "danger",
                "🚨"
            )
        )
    
    with col3:
        state_context = f"{states_affected} of 50 states + territories"
        st.html(
            display_metric_card(
                "Geographic Reach",
                str(states_affected),
                state_context,
                "info",
                "📍"
            )
        )
    
    with col4:
        school_context = f"Avg {(schools_affected/states_affected):.1f} per state" if states_affected > 0 else "Unique locations"
        st.html(
            display_metric_card(
                "Schools Impacted",
                f"{schools_affected:,}",
                school_context,
                "warning",
                "🏫"
            )
        )


def display_latest_incident(df: pd.DataFrame):
    """
    Display the most recent incident in the sidebar with relevant details.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.sidebar.info("No incidents found for the selected filters.")
        return
    
    # Get the most recent incident
    latest_incident = df.loc[df["Incident Date"].idxmax()]
    
    # Format date and location
    date_str = latest_incident["Incident Date"].strftime("%B %d, %Y")
    days_ago = (datetime.now() - latest_incident["Incident Date"]).days
    
    # Build casualty summary
    casualties_parts = []
    if latest_incident['Number Killed'] > 0:
        casualties_parts.append(f"{int(latest_incident['Number Killed'])} killed")
    if latest_incident['Number Wounded'] > 0:
        casualties_parts.append(f"{int(latest_incident['Number Wounded'])} wounded")
    
    casualty_summary = " and ".join(casualties_parts) if casualties_parts else "No casualties reported"
    
    # Determine severity color
    if latest_incident['Total_Casualties'] == 0:
        severity_color = COLORS['success']
    elif latest_incident['Is_Fatal']:
        severity_color = COLORS['danger']
    else:
        severity_color = COLORS['warning']
    
    # Create informative card
    incident_html = f"""
        <div style="
            background: linear-gradient(to right, #ffffff 0%, #f8f9fa 100%);
            border-left: 4px solid {severity_color};
            padding: 1.25rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        ">
            <h4 style="color: #2c3e50; margin: 0 0 0.75rem 0; font-size: 1.1rem;">
                📅 Most Recent Incident
            </h4>
            <div style="color: #34495e; line-height: 1.6;">
                <p style="margin: 0.5rem 0;">
                    <strong>{date_str}</strong>
                    <span style="color: #7f8c8d; font-size: 0.875rem;">
                        ({days_ago} days ago)
                    </span>
                </p>
                <p style="margin: 0.5rem 0; font-size: 0.95rem;">
                    📍 <strong>{latest_incident['School name']}</strong><br>
                    <span style="margin-left: 1.5rem; color: #7f8c8d;">
                        {latest_incident['City']}, {latest_incident['State_name']}
                    </span>
                </p>
                <p style="margin: 0.5rem 0;">
                    💔 <strong>Impact:</strong> {casualty_summary}
                </p>
            </div>
        </div>
    """
    
    st.sidebar.html(incident_html)


def display_info_box(
    content: str, 
    title: str = "", 
    type: str = "info",
    icon: Optional[str] = None
) -> str:
    """
    Create a styled information box for displaying important messages.
    
    Args:
        content: HTML content to display
        title: Optional title for the box
        type: Box type (info, warning, success, danger)
        icon: Optional icon/emoji to display with title
        
    Returns:
        HTML string for the info box
    """
    # Color schemes for different box types
    color_schemes = {
        'info': ('#e8f4f8', '#3498db', '💡'),
        'warning': ('#fef5e7', '#f39c12', '⚠️'),
        'success': ('#eafaf1', '#27ae60', '✅'),
        'danger': ('#fadbd8', '#e74c3c', '🚨')
    }
    
    bg_color, border_color, default_icon = color_schemes.get(type, color_schemes['info'])
    display_icon = icon or default_icon
    
    title_html = ''
    if title:
        title_html = f'''
            <h4 style="margin: 0 0 0.75rem 0; color: #2c3e50; font-size: 1rem;">
                {display_icon} {title}
            </h4>
        '''
    
    return f"""
        <div style="
            background: {bg_color};
            border: 1px solid {border_color};
            border-left: 4px solid {border_color};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0.5rem;
            font-size: 0.95rem;
        ">
            {title_html}
            <div style="color: #2c3e50; line-height: 1.6;">
                {content}
            </div>
        </div>
    """


def display_definition_box(definitions: Dict[str, str], title: str = "Key Definitions") -> str:
    """
    Create a styled box for displaying definitions or terminology.
    
    Args:
        definitions: Dictionary of term: definition pairs
        title: Title for the definitions box
        
    Returns:
        HTML string for the definition box
    """
    # Build definition list
    items = []
    for term, definition in definitions.items():
        items.append(
            f'<li style="margin: 0.5rem 0;">'
            f'<strong style="color: #2c3e50;">{term}:</strong> '
            f'<span style="color: #5a6c7d;">{definition}</span>'
            f'</li>'
        )
    
    content = f'<ul style="margin: 0; padding-left: 1.25rem; list-style-type: none;">{"".join(items)}</ul>'
    
    return display_info_box(content, f"📖 {title}", type="info")


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a percentage value with consistent styling.
    
    Args:
        value: Percentage value (0-100)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_number(value: Union[int, float]) -> str:
    """
    Format a number with thousand separators.
    
    Args:
        value: Number to format
        
    Returns:
        Formatted number string
    """
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return f"{value:,}"


def create_summary_stats(df: pd.DataFrame) -> Dict[str, Union[int, float, str, pd.Timestamp]]:
    """
    Generate comprehensive summary statistics from the filtered data.
    
    Args:
        df: Filtered dataframe
        
    Returns:
        Dictionary containing key statistics
    """
    if df.empty:
        return {}
    
    current_year = datetime.now().year
    
    # Basic incident counts
    stats = {
        # Incident metrics
        'total_incidents': len(df),
        'total_casualties': int(df['Total_Casualties'].sum()),
        'total_killed': int(df['Number Killed'].sum()),
        'total_wounded': int(df['Number Wounded'].sum()),
        
        # Geographic spread
        'states_affected': df['State_name'].nunique(),
        'cities_affected': df['City'].nunique(),
        'schools_affected': df['School name'].nunique(),
        
        # Per-incident averages
        'avg_casualties_per_incident': df['Total_Casualties'].mean(),
        'avg_days_between_incidents': (df['Incident Date'].max() - df['Incident Date'].min()).days / len(df) if len(df) > 1 else 0,
    }
    
    # Calculate rates and percentages
    if stats['total_incidents'] > 0:
        stats.update({
            'no_casualty_rate': (len(df[df['Total_Casualties'] == 0]) / stats['total_incidents'] * 100),
            'fatal_rate': (len(df[df['Is_Fatal']]) / stats['total_incidents'] * 100),
            'mass_casualty_rate': (len(df[df['Total_Casualties'] >= 4]) / stats['total_incidents'] * 100),
            'weekday_rate': (len(df[~df['DayOfWeek_Num'].isin([5, 6])]) / stats['total_incidents'] * 100),
            'school_year_rate': (len(df[~df['Month'].isin(['Jun', 'Jul', 'Aug'])]) / stats['total_incidents'] * 100),
        })
    
    # Time-based statistics
    stats.update({
        'date_range_start': df['Incident Date'].min(),
        'date_range_end': df['Incident Date'].max(),
        'years_covered': df['Year'].nunique(),
        'current_year_partial': (df['Year'].max() == current_year),
        'days_since_last': (datetime.now() - df['Incident Date'].max()).days,
    })
    
    # Top locations (if data exists)
    if not df.empty:
        stats['top_state'] = df['State_name'].value_counts().index[0]
        stats['top_state_count'] = df['State_name'].value_counts().iloc[0]
        
        city_state_counts = df.groupby(['City', 'State_name']).size()
        if not city_state_counts.empty:
            top_city = city_state_counts.idxmax()
            stats['top_city'] = f"{top_city[0]}, {top_city[1]}"
            stats['top_city_count'] = city_state_counts.max()
    
    return stats


def display_data_quality_banner(quality_metrics: Dict[str, Union[int, float]]):
    """
    Display a banner showing data quality and completeness metrics.
    
    Args:
        quality_metrics: Dictionary containing quality scores
    """
    score = quality_metrics.get('completeness_score', 0)
    
    # Determine quality level and styling
    if score >= 90:
        quality_level = "Excellent"
        color = "success"
        emoji = "🌟"
    elif score >= 75:
        quality_level = "Good"
        color = "info"
        emoji = "👍"
    elif score >= 60:
        quality_level = "Fair"
        color = "warning"
        emoji = "⚠️"
    else:
        quality_level = "Limited"
        color = "danger"
        emoji = "⚡"
    
    # Build detailed quality information
    missing_data = []
    if quality_metrics.get('missing_dates', 0) > 0:
        missing_data.append(f"{quality_metrics['missing_dates']} missing dates")
    if quality_metrics.get('missing_coords', 0) > 0:
        missing_data.append(f"{quality_metrics['missing_coords']} missing locations")
    if quality_metrics.get('missing_narratives', 0) > 0:
        missing_data.append(f"{quality_metrics['missing_narratives']} missing narratives")
    
    missing_summary = " • ".join(missing_data) if missing_data else "All critical fields complete"
    
    content = f"""
        <strong>{emoji} Data Quality:</strong> {quality_level} ({score}% complete)<br>
        <small style="color: #7f8c8d;">
            {missing_summary}<br>
            Last updated: {quality_metrics.get('data_freshness', 'Unknown')} days ago
        </small>
    """
    
    st.html(display_info_box(content, type=color))


def display_latest_incident_ticker(df: pd.DataFrame):
    """
    Display the latest incident as a clean information bar.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        return
    
    # Get the most recent incident
    latest = df.loc[df["Incident Date"].idxmax()]
    
    # Format the information
    date_str = latest["Incident Date"].strftime("%B %d, %Y")
    days_ago = (datetime.now() - latest["Incident Date"]).days
    location = f"{latest['City']}, {latest['State_name']}"
    school = latest['School name']
    
    # Build casualty text
    casualties = []
    if latest['Number Killed'] > 0:
        casualties.append(f"{int(latest['Number Killed'])} killed")
    if latest['Number Wounded'] > 0:
        casualties.append(f"{int(latest['Number Wounded'])} wounded")
    
    casualty_text = " and ".join(casualties) if casualties else "No casualties reported"
    
    # Get narrative if available
    narrative = ""
    if pd.notna(latest.get('Narrative', '')) and latest['Narrative']:
        narrative = str(latest['Narrative'])
        # Truncate if too long
        if len(narrative) > 300:
            narrative = narrative[:297] + "..."
    
    # Determine severity for color coding
    if latest['Total_Casualties'] == 0:
        severity_color = "#27ae60"  # Green
        severity_emoji = "🟢"
        severity_text = "NO CASUALTIES"
    elif latest['Is_Fatal']:
        severity_color = "#e74c3c"  # Red
        severity_emoji = "🔴"
        severity_text = "FATAL INCIDENT"
    else:
        severity_color = "#f39c12"  # Orange
        severity_emoji = "🟡"
        severity_text = "INJURIES REPORTED"
    
    # Create clean info bar HTML
    ticker_html = f"""
    <div style="
        background: #2c3e50;
        color: white;
        padding: 16px 20px;
        margin: -1rem -1rem 2rem -1rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        border-left: 5px solid {severity_color};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    ">
        <!-- Header Row -->
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
            ">
                <span style="
                    font-weight: 700;
                    text-transform: uppercase;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                ">
                    {severity_emoji} LATEST INCIDENT
                </span>
                <span style="
                    background: {severity_color};
                    padding: 2px 10px;
                    border-radius: 3px;
                    font-size: 11px;
                    font-weight: 600;
                ">
                    {severity_text}
                </span>
            </div>
            <div style="
                font-size: 13px;
                color: #bdc3c7;
            ">
                {date_str} • {days_ago} days ago
            </div>
        </div>
        
        <!-- Main Info Row -->
        <div style="
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 15px;
        ">
            <div>
                📍 <strong>{location}</strong>
            </div>
            <div style="color: #ecf0f1;">
                🏫 {school}
            </div>
            <div style="color: #e74c3c;">
                {casualty_text}
            </div>
        </div>
    """
    
    # Add narrative if available
    if narrative:
        ticker_html += f"""
        <div style="
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 14px;
            color: #ecf0f1;
            line-height: 1.5;
        ">
            {narrative}
        </div>
        """
    
    ticker_html += """
    </div>
    """
    
    st.html(ticker_html)


def display_latest_incident_compact(df: pd.DataFrame):
    """
    Display a compact version of latest incident for sidebars.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.info("No incidents in current selection")
        return
    
    # Get the most recent incident
    latest = df.loc[df["Incident Date"].idxmax()]
    
    # Format the information
    date_str = latest["Incident Date"].strftime("%b %d, %Y")
    days_ago = (datetime.now() - latest["Incident Date"]).days
    
    # Casualty summary
    if latest['Total_Casualties'] == 0:
        impact = "No casualties"
        color = "#27ae60"
    elif latest['Is_Fatal']:
        impact = f"{int(latest['Number Killed'])} killed, {int(latest['Number Wounded'])} wounded"
        color = "#e74c3c"
    else:
        impact = f"{int(latest['Number Wounded'])} wounded"
        color = "#f39c12"
    
    # Compact news display
    compact_html = f"""
    <div style="
        background: #2c3e50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 13px;
        line-height: 1.5;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        ">
            <span style="
                background: {color};
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
            ">Latest</span>
            <span style="color: #ecf0f1;">{date_str} • {days_ago}d ago</span>
        </div>
        
        <div style="color: #ecf0f1; margin-bottom: 4px;">
            📍 {latest['City']}, {latest['State_name']}
        </div>
        
        <div style="color: #bdc3c7; font-size: 12px;">
            {impact}
        </div>
    </div>
    """
    
    st.html(compact_html)


def display_year_disclaimer(year: int):
    """
    Display a disclaimer for partial year data to prevent misinterpretation.
    
    Args:
        year: Year to check
    """
    current_year = datetime.now().year
    current_month = datetime.now().strftime('%B')
    
    if year == current_year:
        content = f"""
            <strong>⚠️ {year} Data Notice:</strong> This year is currently in progress 
            (as of {current_month} {year}). Statistics shown are based on incidents 
            recorded to date and will increase throughout the year. 
            <strong>Do not use for year-over-year comparisons.</strong>
        """
        st.html(display_info_box(content, type="warning"))


def create_download_button(
    data: Union[pd.DataFrame, str], 
    filename: str, 
    label: str = "Download",
    file_type: str = "csv"
) -> None:
    """
    Create a styled download button with timestamp.
    
    Args:
        data: Data to download (DataFrame or string)
        filename: Base filename (without extension)
        label: Button label
        file_type: File type (csv, html, etc.)
    """
    # Add timestamp to filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    full_filename = f"{filename}_{timestamp}.{file_type}"
    
    # Convert DataFrame to appropriate format
    if isinstance(data, pd.DataFrame):
        if file_type == "csv":
            data_str = data.to_csv(index=False)
            mime_type = "text/csv"
        else:
            data_str = data.to_html(index=False)
            mime_type = "text/html"
    else:
        data_str = data
        mime_type = f"text/{file_type}"
    
    st.download_button(
        label=f"📥 {label}",
        data=data_str,
        file_name=full_filename,
        mime=mime_type,
        help=f"Download {label.lower()} as {file_type.upper()}"
    )