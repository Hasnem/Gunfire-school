import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots
from typing import Tuple, Optional, Union
from utils.utils_common import STATE_MAPPING

# Consistent color palette aligned with the application theme
COLORS = {
    'primary': '#4a5568',      # Dark gray for main elements
    'secondary': '#718096',    # Medium gray for secondary elements
    'accent': '#3182ce',       # Blue for highlights and trends
    'danger': '#e53e3e',       # Red for critical/fatal data
    'warning': '#f6ad55',      # Orange for warnings/summer months
    'success': '#48bb78',      # Green for positive/safe metrics
    'neutral': '#e2e8f0',      # Light gray for backgrounds/grids
    'info': '#4299e1'          # Light blue for informational elements
}

# Chart configuration defaults
CHART_CONFIG = {
    'font_family': "Arial, sans-serif",
    'title_size': 18,
    'axis_title_size': 14,
    'tick_size': 11,
    'annotation_size': 12,
    'height_default': 400,
    'margin': dict(l=60, r=30, t=60, b=60)
}


def create_clean_layout(
    fig: go.Figure, 
    title: str = "", 
    height: int = None,
    show_legend: bool = False
) -> go.Figure:
    """
    Apply consistent, clean styling to all charts.
    
    Args:
        fig: Plotly figure object
        title: Chart title
        height: Chart height (uses default if None)
        show_legend: Whether to show legend
        
    Returns:
        Styled figure object
    """
    fig.update_layout(
        # Title styling
        title={
            'text': title,
            'font': {
                'size': CHART_CONFIG['title_size'], 
                'color': COLORS['primary'],
                'family': CHART_CONFIG['font_family']
            },
            'x': 0,
            'xanchor': 'left',
            'pad': {'l': 0, 't': 10}
        },
        # General font settings
        font=dict(
            family=CHART_CONFIG['font_family'], 
            size=12, 
            color=COLORS['primary']
        ),
        # Clean background
        plot_bgcolor='white',
        paper_bgcolor='white',
        # Dimensions
        height=height or CHART_CONFIG['height_default'],
        margin=CHART_CONFIG['margin'],
        # Interaction
        hovermode='closest',
        showlegend=show_legend,
        # Axis styling
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS['neutral'],
            linecolor=COLORS['neutral'],
            tickfont=dict(size=CHART_CONFIG['tick_size']),
            title_font=dict(size=CHART_CONFIG['axis_title_size'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['neutral'],
            linecolor=COLORS['neutral'],
            tickfont=dict(size=CHART_CONFIG['tick_size']),
            title_font=dict(size=CHART_CONFIG['axis_title_size'])
        )
    )
    return fig


def plot_yearly_trend(df: pd.DataFrame) -> go.Figure:
    """
    Create an informative yearly trend visualization with proper context.
    
    Args:
        df: Filtered dataframe with incident data
        
    Returns:
        Plotly figure showing yearly trends
    """
    if df.empty:
        return create_empty_figure("No data available for yearly analysis")
    
    # Prepare yearly statistics
    current_year = datetime.now().year
    yearly_stats = df.groupby('Year').agg({
        'ID': 'count',
        'Total_Casualties': 'sum',
        'Number Killed': 'sum'
    }).reset_index()
    yearly_stats.columns = ['Year', 'Incidents', 'Total_Casualties', 'Deaths']
    
    # Identify complete vs partial years
    yearly_stats['Is_Complete'] = yearly_stats['Year'] < current_year
    
    # Create figure with bar chart
    fig = go.Figure()
    
    # Add incident bars with color coding
    fig.add_trace(go.Bar(
        x=yearly_stats['Year'],
        y=yearly_stats['Incidents'],
        name='Incidents',
        marker_color=[
            COLORS['primary'] if complete else COLORS['secondary'] 
            for complete in yearly_stats['Is_Complete']
        ],
        text=yearly_stats['Incidents'],
        textposition='outside',
        textfont=dict(size=11),
        hovertemplate=(
            'Year: %{x}<br>' +
            'Incidents: %{y}<br>' +
            'Casualties: %{customdata[0]}<br>' +
            'Deaths: %{customdata[1]}<extra></extra>'
        ),
        customdata=yearly_stats[['Total_Casualties', 'Deaths']].values
    ))
    
    # Add trend line for complete years only
    complete_years = yearly_stats[yearly_stats['Is_Complete']]
    if len(complete_years) >= 3:  # Need at least 3 points for meaningful trend
        # Calculate linear regression
        z = np.polyfit(complete_years['Year'], complete_years['Incidents'], 1)
        p = np.poly1d(z)
        trend_line = p(complete_years['Year'])
        
        fig.add_trace(go.Scatter(
            x=complete_years['Year'],
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color=COLORS['accent'], width=2, dash='dash'),
            hovertemplate='Trend: %{y:.0f}<extra></extra>'
        ))
        
        # Add trend annotation
        trend_direction = "increasing" if z[0] > 0 else "decreasing"
        annual_change = abs(z[0])
        fig.add_annotation(
            x=complete_years['Year'].iloc[-1],
            y=trend_line[-1],
            text=f"Trend: {trend_direction}<br>~{annual_change:.1f}/year",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=COLORS['accent'],
            ax=50,
            ay=-30,
            bgcolor="white",
            bordercolor=COLORS['accent'],
            borderwidth=1,
            font=dict(size=CHART_CONFIG['annotation_size'])
        )
    
    # Highlight current year if partial
    if current_year in yearly_stats['Year'].values:
        current_data = yearly_stats[yearly_stats['Year'] == current_year].iloc[0]
        current_month = datetime.now().strftime('%B')
        
        fig.add_annotation(
            x=current_year,
            y=current_data['Incidents'],
            text=f"{current_year}<br>(Through {current_month})",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=COLORS['warning'],
            ax=0,
            ay=-50,
            bgcolor="rgba(254, 245, 231, 0.9)",
            bordercolor=COLORS['warning'],
            borderwidth=1,
            font=dict(size=11, color=COLORS['warning'])
        )
    
    # Apply clean layout
    fig = create_clean_layout(fig, "Annual Incident Trends", height=450)
    fig.update_yaxes(title_text="Number of Incidents", rangemode='tozero')
    fig.update_xaxes(title_text="Year", dtick=1, tickangle=0)
    
    return fig


def display_monthly_analysis(df: pd.DataFrame):
    """
    Create monthly visualization with school calendar context.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.warning("No data available for monthly analysis.")
        return
    
    # Define month order and calculate statistics
    months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly_counts = df.groupby('Month').size().reindex(months_order, fill_value=0)
    monthly_casualties = df.groupby('Month')['Total_Casualties'].sum().reindex(months_order, fill_value=0)
    
    # Create figure
    fig = go.Figure()
    
    # Color code by school calendar period
    colors = []
    for month in months_order:
        if month in ['Jun', 'Jul', 'Aug']:
            colors.append(COLORS['warning'])  # Summer break
        elif month in ['Dec', 'Jan']:
            colors.append(COLORS['info'])     # Winter break
        else:
            colors.append(COLORS['primary'])  # Regular school year
    
    # Add incident bars
    fig.add_trace(go.Bar(
        x=months_order,
        y=monthly_counts.values,
        name='Incidents',
        marker_color=colors,
        text=monthly_counts.values,
        textposition='outside',
        hovertemplate=(
            '%{x}<br>' +
            'Incidents: %{y}<br>' +
            'Casualties: %{customdata}<extra></extra>'
        ),
        customdata=monthly_casualties.values
    ))
    
    # Add monthly average line
    avg_incidents = monthly_counts.mean()
    fig.add_hline(
        y=avg_incidents,
        line_dash="dot",
        line_color=COLORS['secondary'],
        annotation_text=f"Monthly Average: {avg_incidents:.0f}",
        annotation_position="right",
        annotation_font_size=11
    )
    
    # Add school calendar annotations
    annotation_y = monthly_counts.max() * 1.15
    
    # Summer break annotation
    fig.add_annotation(
        x=6.5,  # Position between Jun and Aug
        y=annotation_y,
        text="Summer Break",
        showarrow=False,
        font=dict(size=12, color=COLORS['warning']),
        bgcolor="rgba(246, 173, 85, 0.1)",
        bordercolor=COLORS['warning'],
        borderwidth=1,
        borderpad=4
    )
    
    # School year annotation
    fig.add_annotation(
        x=2,  # Position for spring semester
        y=annotation_y,
        text="School in Session",
        showarrow=False,
        font=dict(size=12, color=COLORS['primary']),
        bgcolor="rgba(74, 85, 104, 0.1)",
        bordercolor=COLORS['primary'],
        borderwidth=1,
        borderpad=4
    )
    
    # Apply clean layout
    fig = create_clean_layout(fig, "Monthly Incident Distribution", height=450)
    fig.update_yaxes(title_text="Number of Incidents", rangemode='tozero')
    fig.update_xaxes(title_text="Month")
    
    # Add insight text below chart
    summer_pct = (monthly_counts[['Jun', 'Jul', 'Aug']].sum() / monthly_counts.sum() * 100)
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"📊 Summer months account for {summer_pct:.1f}% of incidents, showing clear correlation with school schedules.")


def display_day_of_week_analysis(df: pd.DataFrame):
    """
    Create weekday vs weekend comparison with educational context.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.warning("No data available for day-of-week analysis.")
        return
    
    # Calculate weekday vs weekend statistics
    df['Is_Weekday'] = ~df['DayOfWeek_Num'].isin([5, 6])  # 5=Sat, 6=Sun
    
    # Create comparison data
    comparison = pd.DataFrame({
        'Period': ['School Days (Mon-Fri)', 'Weekend (Sat-Sun)'],
        'Incidents': [
            df[df['Is_Weekday']].shape[0],
            df[~df['Is_Weekday']].shape[0]
        ]
    })
    
    comparison['Percentage'] = (comparison['Incidents'] / comparison['Incidents'].sum() * 100).round(1)
    comparison['Avg_Per_Day'] = [
        comparison.iloc[0]['Incidents'] / 5,  # 5 weekdays
        comparison.iloc[1]['Incidents'] / 2   # 2 weekend days
    ]
    
    # Create donut chart
    fig = go.Figure()
    
    # Add pie chart with custom styling
    fig.add_trace(go.Pie(
        labels=comparison['Period'],
        values=comparison['Incidents'],
        hole=.5,
        marker=dict(
            colors=[COLORS['primary'], COLORS['secondary']],
            line=dict(color='white', width=2)
        ),
        text=[f"{row['Incidents']}<br>{row['Percentage']}%" for _, row in comparison.iterrows()],
        textinfo='text',
        textfont=dict(size=14, color='white'),
        hovertemplate=(
            '%{label}<br>' +
            'Incidents: %{value}<br>' +
            'Percentage: %{percent}<br>' +
            'Avg per day: %{customdata:.1f}<extra></extra>'
        ),
        customdata=comparison['Avg_Per_Day']
    ))
    
    # Add center annotation
    fig.add_annotation(
        text=f"<b>Total<br>{comparison['Incidents'].sum()}</b><br>incidents",
        x=0.5, y=0.5,
        font=dict(size=16, color=COLORS['primary']),
        showarrow=False
    )
    
    # Apply clean layout
    fig = create_clean_layout(fig, "School Schedule Impact", height=400, show_legend=True)
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add insight below
    weekday_rate = comparison.iloc[0]['Avg_Per_Day']
    weekend_rate = comparison.iloc[1]['Avg_Per_Day']
    ratio = weekday_rate / weekend_rate if weekend_rate > 0 else float('inf')
    
    st.caption(f"📊 Weekdays average {weekday_rate:.1f} incidents/day vs {weekend_rate:.1f} on weekends ({ratio:.1f}x higher)")


def display_key_factor_distribution(df: pd.DataFrame):
    """
    Display incident severity distribution with clear visual hierarchy.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.info("No data available for severity analysis.")
        return
    
    # Verify severity column exists
    if 'Severity' not in df.columns:
        st.warning("Severity data not available.")
        return
    
    # Define severity order and colors
    severity_order = [
        'No Casualties', 
        'Injuries Only', 
        'Single Fatality', 
        'Multiple Casualties', 
        'Mass Casualty'
    ]
    
    severity_colors = [
        COLORS['success'],    # No casualties - green
        COLORS['warning'],    # Injuries - orange
        COLORS['danger'],     # Single fatality - red
        COLORS['danger'],     # Multiple casualties - red
        '#8b0000'            # Mass casualty - dark red
    ]
    
    # Calculate severity counts
    severity_counts = df['Severity'].value_counts().reindex(severity_order, fill_value=0)
    total_incidents = severity_counts.sum()
    
    # Create horizontal bar chart for better label readability
    fig = go.Figure()
    
    # Add bars with percentage labels
    percentages = (severity_counts.values / total_incidents * 100).round(1)
    
    fig.add_trace(go.Bar(
        y=severity_order,
        x=severity_counts.values,
        orientation='h',
        marker_color=severity_colors,
        text=[f"{count:,} ({pct}%)" for count, pct in zip(severity_counts.values, percentages)],
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate=(
            '%{y}<br>' +
            'Count: %{x:,}<br>' +
            'Percentage: %{customdata:.1f}%<extra></extra>'
        ),
        customdata=percentages
    ))
    
    # Add dividing line between non-fatal and fatal
    if 'Injuries Only' in severity_order and 'Single Fatality' in severity_order:
        divide_y = (severity_order.index('Injuries Only') + severity_order.index('Single Fatality')) / 2
        fig.add_hline(
            y=divide_y,
            line_dash="dash",
            line_color=COLORS['danger'],
            annotation_text="Fatal Threshold",
            annotation_position="top right",
            annotation_font_color=COLORS['danger']
        )
    
    # Apply clean layout
    fig = create_clean_layout(fig, "Incident Severity Breakdown", height=400)
    fig.update_xaxes(title_text="Number of Incidents", rangemode='tozero')
    fig.update_yaxes(title_text="", categoryorder='array', categoryarray=severity_order[::-1])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add key insights
    no_casualty_pct = percentages[0] if len(percentages) > 0 else 0
    fatal_incidents = severity_counts[severity_counts.index.isin(['Single Fatality', 'Multiple Casualties', 'Mass Casualty'])].sum()
    fatal_pct = (fatal_incidents / total_incidents * 100) if total_incidents > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("No Physical Harm", f"{no_casualty_pct:.1f}%", help="Incidents with no casualties")
    with col2:
        st.metric("Fatal Incidents", f"{fatal_pct:.1f}%", help="Incidents resulting in death")


def create_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create intent vs outcome heatmap showing incident patterns.
    
    Args:
        df: Filtered dataframe with incident data
        
    Returns:
        Plotly heatmap figure
    """
    if df.empty or 'Intent' not in df.columns or 'Outcome' not in df.columns:
        return create_empty_figure("Insufficient data for intent-outcome analysis")
    
    # Create pivot table
    pivot = pd.pivot_table(
        df, 
        values='ID', 
        index='Intent', 
        columns='Outcome', 
        aggfunc='count'
    ).fillna(0)
    
    # Limit to top categories for clarity
    top_intents = df['Intent'].value_counts().head(6).index
    top_outcomes = df['Outcome'].value_counts().head(6).index
    
    pivot_filtered = pivot.loc[
        pivot.index.intersection(top_intents),
        pivot.columns.intersection(top_outcomes)
    ]
    
    if pivot_filtered.empty:
        return create_empty_figure("No data for selected categories")
    
    # Create annotations for cells
    annotations = []
    for i, intent in enumerate(pivot_filtered.index):
        for j, outcome in enumerate(pivot_filtered.columns):
            value = pivot_filtered.loc[intent, outcome]
            if value > 0:  # Only annotate non-zero cells
                annotations.append(
                    dict(
                        text=str(int(value)),
                        x=j,
                        y=i,
                        xref='x',
                        yref='y',
                        showarrow=False,
                        font=dict(
                            color='white' if value > pivot_filtered.values.max() * 0.5 else 'black',
                            size=12
                        )
                    )
                )
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_filtered.values,
        x=pivot_filtered.columns,
        y=pivot_filtered.index,
        colorscale=[
            [0, 'white'],
            [0.2, COLORS['neutral']],
            [0.5, COLORS['info']],
            [0.8, COLORS['primary']],
            [1, COLORS['danger']]
        ],
        hovertemplate=(
            'Intent: %{y}<br>' +
            'Outcome: %{x}<br>' +
            'Count: %{z}<extra></extra>'
        ),
        colorbar=dict(
            title="Incidents",
            thickness=15,
            len=0.7
        )
    ))
    
    # Add annotations
    fig.update_layout(annotations=annotations)
    
    # Apply clean layout
    fig = create_clean_layout(fig, "Intent vs Outcome Patterns", height=500)
    fig.update_xaxes(title_text="Outcome", side="bottom", tickangle=-45)
    fig.update_yaxes(title_text="Intent", side="left")
    
    return fig


def plot_statewise_data(df: pd.DataFrame) -> Tuple[go.Figure, go.Figure]:
    """
    Create state-level visualizations with geographic insights.
    
    Args:
        df: Filtered dataframe with incident data
        
    Returns:
        Tuple of (bar chart figure, map figure)
    """
    if df.empty:
        empty_fig = create_empty_figure("No state data available")
        return empty_fig, empty_fig
    
    # Calculate state statistics
    state_stats = df.groupby('State_name').agg({
        'ID': 'count',
        'Total_Casualties': 'sum',
        'School name': 'nunique'
    }).reset_index()
    state_stats.columns = ['State', 'Incidents', 'Casualties', 'Schools']
    state_stats = state_stats.sort_values('Incidents', ascending=False)
    
    # Focus on top 15 states for bar chart
    top_states = state_stats.head(15)
    
    # Create bar chart
    fig_bar = go.Figure()
    
    # Add incident bars
    fig_bar.add_trace(go.Bar(
        x=top_states['State'],
        y=top_states['Incidents'],
        name='Incidents',
        marker_color=COLORS['primary'],
        text=top_states['Incidents'],
        textposition='outside',
        yaxis='y',
        hovertemplate=(
            '%{x}<br>' +
            'Incidents: %{y}<br>' +
            'Casualties: %{customdata[0]}<br>' +
            'Schools affected: %{customdata[1]}<extra></extra>'
        ),
        customdata=top_states[['Casualties', 'Schools']].values
    ))
    
    # Add cumulative percentage line
    total_incidents = state_stats['Incidents'].sum()
    top_states['Cumulative_Pct'] = (top_states['Incidents'].cumsum() / total_incidents * 100).round(1)
    
    fig_bar.add_trace(go.Scatter(
        x=top_states['State'],
        y=top_states['Cumulative_Pct'],
        mode='lines+markers',
        name='Cumulative %',
        yaxis='y2',
        line=dict(color=COLORS['accent'], width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Cumulative: %{y:.1f}%<extra></extra>'
    ))
    
    # Add 80% reference line manually as a shape
    fig_bar.add_shape(
        type="line",
        x0=0,
        x1=1,
        y0=80,
        y1=80,
        xref="paper",
        yref="y2",
        line=dict(
            color=COLORS['warning'],
            width=1,
            dash="dash"
        )
    )
    
    # Add annotation for the line
    fig_bar.add_annotation(
        x=1,
        y=80,
        xref="paper",
        yref="y2",
        text="80% of incidents",
        showarrow=False,
        xanchor="left",
        yanchor="middle",
        font=dict(color=COLORS['warning'])
    )
    
    # Apply layout
    fig_bar.update_layout(
        title="Geographic Concentration: Top 15 States",
        xaxis=dict(title="State", tickangle=-45),
        yaxis=dict(title="Number of Incidents", side='left', rangemode='tozero'),
        yaxis2=dict(
            title="Cumulative Percentage", 
            side='right', 
            overlaying='y', 
            range=[0, 105],
            ticksuffix='%'
        ),
        height=500,
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'),
        hovermode='x unified'
    )
    fig_bar = create_clean_layout(fig_bar, "Geographic Concentration: Top 15 States", height=500, show_legend=True)
    
    # Create choropleth map
    fig_map = create_state_choropleth(df)
    
    return fig_bar, fig_map


def create_state_choropleth(df: pd.DataFrame) -> go.Figure:
    """
    Create a choropleth map showing incident density by state.
    
    Args:
        df: Filtered dataframe with incident data
        
    Returns:
        Plotly choropleth figure
    """
    if df.empty:
        return create_empty_figure("No geographic data available")
    
    # Calculate state statistics
    state_stats = df.groupby('State_name').size().reset_index(name='Incidents')
    
    # Map state names to abbreviations
    reverse_state_map = {v: k for k, v in STATE_MAPPING.items()}
    state_stats['State_Abbr'] = state_stats['State_name'].map(reverse_state_map)
    state_stats = state_stats.dropna(subset=['State_Abbr'])
    
    # Create choropleth
    fig = go.Figure(data=go.Choropleth(
        locations=state_stats['State_Abbr'],
        z=state_stats['Incidents'],
        locationmode='USA-states',
        colorscale=[
            [0, 'white'],
            [0.2, '#e8f4f8'],
            [0.4, COLORS['info']],
            [0.7, COLORS['primary']],
            [1, COLORS['danger']]
        ],
        marker_line_color='white',
        marker_line_width=1,
        colorbar=dict(
            title="Incidents",
            thickness=15,
            len=0.7,
            x=1.0,
            tickmode='linear',
            tick0=0,
            dtick=state_stats['Incidents'].max() // 5
        ),
        text=state_stats['State_name'],
        hovertemplate='%{text}<br>Incidents: %{z}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title="Incident Distribution Across the United States",
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showlakes=False,
            bgcolor='white',
            lakecolor='white'
        ),
        height=500
    )
    
    return fig


def create_top_cities_bar_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create visualization of cities with most incidents.
    
    Args:
        df: Filtered dataframe with incident data
        
    Returns:
        Plotly bar chart figure
    """
    if df.empty:
        return create_empty_figure("No city data available")
    
    # Calculate city statistics
    city_stats = df.groupby(['City', 'State']).agg({
        'ID': 'count',
        'Total_Casualties': 'sum',
        'School name': 'nunique'
    }).reset_index()
    
    # Create city-state identifier
    city_stats['Location'] = city_stats['City'] + ', ' + city_stats['State']
    city_stats = city_stats.sort_values('ID', ascending=False).head(12)
    
    # Create horizontal bar chart for better readability
    fig = go.Figure()
    
    # Color bars based on casualty severity
    colors = []
    for _, row in city_stats.iterrows():
        if row['Total_Casualties'] == 0:
            colors.append(COLORS['success'])
        elif row['Total_Casualties'] < 5:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['danger'])
    
    fig.add_trace(go.Bar(
        y=city_stats['Location'],
        x=city_stats['ID'],
        orientation='h',
        marker_color=colors,
        text=city_stats['ID'],
        textposition='outside',
        hovertemplate=(
            '%{y}<br>' +
            'Incidents: %{x}<br>' +
            'Total Casualties: %{customdata[0]}<br>' +
            'Schools affected: %{customdata[1]}<extra></extra>'
        ),
        customdata=city_stats[['Total_Casualties', 'School name']].values
    ))
    
    # Add severity legend as annotations
    fig.add_annotation(
        text="🟢 No casualties  🟡 <5 casualties  🔴 5+ casualties",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=11, color=COLORS['secondary']),
        xanchor='center'
    )
    
    # Apply clean layout
    fig = create_clean_layout(fig, "Cities with Most Incidents", height=500)
    fig.update_xaxes(title_text="Number of Incidents", rangemode='tozero')
    fig.update_yaxes(title_text="", autorange='reversed')
    
    return fig


def display_top_tragic_incidents(df: pd.DataFrame, n: int = 10):
    """
    Display high-casualty incidents with appropriate context and sensitivity.
    
    Args:
        df: Filtered dataframe with incident data
        n: Number of incidents to display
    """
    if df.empty:
        st.info("No data available for analysis.")
        return
    
    # Sort by casualties and get top N
    sorted_df = df.sort_values('Total_Casualties', ascending=False).head(n)
    
    if sorted_df.empty or sorted_df['Total_Casualties'].sum() == 0:
        st.info("No incidents with casualties in current selection.")
        return
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mass_casualty_count = len(sorted_df[sorted_df['Total_Casualties'] >= 4])
        st.metric(
            "Mass Casualty Events",
            mass_casualty_count,
            help="FBI definition: 4+ casualties"
        )
    
    with col2:
        avg_casualties = sorted_df['Total_Casualties'].mean()
        st.metric(
            "Average Casualties",
            f"{avg_casualties:.1f}",
            help="In high-impact incidents"
        )
    
    with col3:
        total_impact = sorted_df['Total_Casualties'].sum()
        st.metric(
            "Total Impact",
            f"{total_impact:,}",
            help="Combined casualties"
        )
    
    # Create visualization
    fig = go.Figure()
    
    # Prepare data for visualization
    display_df = sorted_df.head(n).copy()
    display_df['Date_Str'] = display_df['Incident Date'].dt.strftime('%Y-%m-%d')
    display_df['Label'] = display_df['State_name'] + ' (' + display_df['Date_Str'] + ')'
    
    # Create stacked bar chart
    fig.add_trace(go.Bar(
        y=display_df['Label'],
        x=display_df['Number Killed'],
        name='Killed',
        orientation='h',
        marker_color=COLORS['danger'],
        hovertemplate='Killed: %{x}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=display_df['Label'],
        x=display_df['Number Wounded'],
        name='Wounded',
        orientation='h',
        marker_color=COLORS['warning'],
        hovertemplate='Wounded: %{x}<extra></extra>'
    ))
    
    # Apply layout
    fig.update_layout(
        title=f"High-Impact Incidents (Top {n})",
        xaxis_title="Number of Casualties",
        yaxis_title="",
        barmode='stack',
        height=400,
        showlegend=True,
        legend=dict(x=0.7, y=1),
        hovermode='y unified'
    )
    fig = create_clean_layout(fig, f"High-Impact Incidents (Top {n})", height=400, show_legend=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add context note
    st.caption(
        "📊 This visualization focuses on incidents with the highest casualty counts to understand "
        "the most severe events and inform prevention strategies."
    )


def create_empty_figure(message: str) -> go.Figure:
    """
    Create a clean placeholder figure when no data is available.
    
    Args:
        message: Message to display
        
    Returns:
        Empty plotly figure with message
    """
    fig = go.Figure()
    
    fig.add_annotation(
        text=f"<b>{message}</b>",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color=COLORS['secondary']),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor=COLORS['neutral'],
        borderwidth=1,
        borderpad=20
    )
    
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        showlegend=False
    )
    
    return fig