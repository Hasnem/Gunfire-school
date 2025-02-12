import os
import io
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import date
from typing import Tuple, List

# Global constants
FONT_SIZE = "16px"
STATE_MAPPING = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia', 
    'PR': 'Puerto Rico', 'GU': 'Guam', 'VI': 'Virgin Islands', 
    'MP': 'Northern Mariana Islands', 'AS': 'American Samoa'
}

###############################################################################
#                                DATA ETL                                     #
###############################################################################

def fetch_data() -> pd.DataFrame:
    """
    Fetches the raw CSV data from Everytown Research's Gunfire on School Grounds URL.
    Returns:
        pd.DataFrame: Raw data as a DataFrame.
    """
    csv_url = 'https://everytownresearch.org/wp-content/uploads/sites/4/etown-maps/gunfire-on-school-grounds/data.csv'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(csv_url, headers=headers)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    return df

def preprocess_data(df: pd.DataFrame, state_mapping: dict = STATE_MAPPING) -> pd.DataFrame:
    """
    Preprocesses the data:
      - Converts datetime columns.
      - Converts latitude/longitude to numeric.
      - Drops extraneous columns and rows with missing location data.
      - Adds grouping columns ('Year', 'Month', 'DayOfWeek') and maps state abbreviations.
    """
    datetime_cols = ['Incident Date', 'Created', 'Last Modified']
    numeric_cols = ['Latitude', 'Longitude']
    drop_cols = ['Source 2', 'URL 2', 'Source 3', 'URL 3', 'School Type']

    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime, errors='coerce')
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df = df.drop(columns=drop_cols, errors='ignore').dropna(subset=numeric_cols)

    df['Year'] = df['Incident Date'].dt.year
    df['Month'] = df['Incident Date'].dt.strftime('%b')
    df['DayOfWeek'] = df['Incident Date'].dt.strftime('%a')
    df['State_name'] = df['State'].map(state_mapping)

    return df

@st.cache_data
def load_and_preprocess_data() -> pd.DataFrame:
    """
    Loads and preprocesses the data. The result is cached.
    """
    df = fetch_data()
    return preprocess_data(df)

###############################################################################
#                                SIDEBAR FILTERS                              #
###############################################################################

def apply_filters(df: pd.DataFrame, state: List[str], intent: List[str],
                  incident_date_range: Tuple[date, date]) -> pd.DataFrame:
    """
    Applies filters for state, intent, and incident date range.
    """
    if state:
        df = df[df['State_name'].isin(state)]
    if intent:
        df = df[df['Intent'].isin(intent)]
    if incident_date_range:
        min_date, max_date = incident_date_range
        df = df[(df['Incident Date'] >= pd.to_datetime(min_date)) &
                (df['Incident Date'] <= pd.to_datetime(max_date))]
    return df

def get_date_range(df: pd.DataFrame) -> Tuple[date, date]:
    """
    Determines the min and max incident dates.
    """
    return df['Incident Date'].min().date(), df['Incident Date'].max().date()

def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders sidebar filter widgets and applies them.
    """
    col1, col2, col3 = st.columns(3)
    with col1:
        state_options = sorted(df['State_name'].dropna().unique())
        state = st.multiselect('State', options=state_options)

    with col2:
        intent_options = sorted(df['Intent'].dropna().unique())
        intent = st.multiselect('Intent', options=intent_options)

    with col3:
        min_date, max_date = get_date_range(df)
        today = date.today()
        default_end = max_date if today > max_date else today
        incident_date_range = st.date_input(
            'Incident Date Range',
            min_value=min_date,
            max_value=max_date,
            value=(min_date, default_end)
        )

    return apply_filters(df, state, intent, incident_date_range)

###############################################################################
#                             HEADER / SIDEBAR                                #
###############################################################################

def display_header() -> None:
    """
    Displays the main header/title of the dashboard.
    """
    st.markdown(
        """
        <h1 style="font-size: 2.5em;">
            <span style="color: red;">Gunfire</span> on U.S. School Grounds: 
            <span style="color: red;">A Real-Time Dashboard</span>
        </h1>
        """, unsafe_allow_html=True
    )
    st.markdown("Data source: [Everytown Research Gunfire on School Grounds](https://everytownresearch.org/maps/gunfire-on-school-grounds/)")

def display_latest_incident(df: pd.DataFrame) -> None:
    """
    Displays details of the most recent incident on the sidebar.
    """
    if df.empty:
        st.sidebar.subheader("No incidents found for the selected filters.")
        return

    max_date = df['Incident Date'].max()
    latest_incident_row = df[df['Incident Date'] == max_date].iloc[0]

    incident_date = latest_incident_row['Incident Date'].strftime('%B %d, %Y')
    news_line = (
        f"On <span style='font-weight:bold'>{incident_date}</span>, a heartbreaking event unfolded at "
        f"<span style='font-weight:bold'>{latest_incident_row['School name']}</span> in "
        f"<span style='font-weight:bold'>{latest_incident_row['City']}</span>, "
        f"<span style='font-weight:bold'>{latest_incident_row['State']}</span>. "
        f"With <span style='color:#ED2F2C; font-weight:bold'>{latest_incident_row['Number Killed']} lives lost</span> "
        f"and <span style='color:#08a88d; font-weight:bold'>{latest_incident_row['Number Wounded']} injured</span>, "
        f"this event reminds us of the urgent need for change."
    )
    st.sidebar.subheader("Latest Recorded Incident:")
    st.sidebar.markdown(news_line, unsafe_allow_html=True)

###############################################################################
#                               METRIC CARDS                                  #
###############################################################################

def calculate_metrics(df: pd.DataFrame) -> Tuple[int, int, int, int]:
    """
    Calculates key metrics for the filtered data.
    """
    if df.empty:
        return 0, 0, 0, 0

    num_victims = int(df[['Number Killed', 'Number Wounded']].sum().sum())
    num_incidents = len(df)
    num_killed = int(df['Number Killed'].sum())
    num_injured = int(df['Number Wounded'].sum())
    return num_victims, num_incidents, num_killed, num_injured

def metric_cards(df: pd.DataFrame) -> None:
    """
    Displays key metrics (victims, incidents, killed, injured) as cards.
    """
    num_victims, num_incidents, num_killed, num_injured = calculate_metrics(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Num of Victims", num_victims)
    col2.metric("Num of Incidents", num_incidents)
    col3.metric("Num Killed", num_killed)
    col4.metric("Num Injured", num_injured)

    style_metric_cards()
    st.markdown(
        f"""
        Since 2013, <span style="color: red; font-weight: bold;">{num_incidents}</span> incidents 
        have scarred school grounds, claiming <span style="color: red; font-weight: bold;">{num_killed}</span> lives 
        and leaving <span style="color: red; font-weight: bold;">{num_injured}</span> injured. 
        Each number tells a story of loss and a call for change.
        """, unsafe_allow_html=True
    )
    st.divider()

def style_metric_cards(background_color: str = "#FFF",
                       border_size_px: int = 1,
                       border_color: str = "#CCC",
                       border_radius_px: int = 5,
                       border_left_color: str = "#ED2F2C",
                       box_shadow: bool = True) -> None:
    """
    Applies custom CSS styling to metric cards.
    """
    box_shadow_str = ("box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;" 
                      if box_shadow else "box-shadow: none !important;")
    st.markdown(
        f"""
        <style>
            div[data-testid="stMetric"],
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """, unsafe_allow_html=True,
    )

###############################################################################
#                             YEARLY TREND                                    #
###############################################################################

def display_trends(df: pd.DataFrame) -> go.Figure:
    """
    Creates a multi-series line chart showing yearly trends of incidents, killed, and wounded.
    """
    df['Year'] = pd.to_datetime(df['Incident Date']).dt.year
    fig = plot_trends(df)
    fig.update_layout(autosize=True, height=400)
    return fig

def plot_trends(df: pd.DataFrame) -> go.Figure:
    """
    Builds a Plotly line chart that shows incidents, killed, and wounded per year.
    """
    if df.empty:
        return go.Figure()

    metrics = {
        'Total Incidents': df.groupby('Year').size(),
        'Number Killed': df.groupby('Year')['Number Killed'].sum(),
        'Number Wounded': df.groupby('Year')['Number Wounded'].sum()
    }
    colors = ['#ED2F2C', '#065388', '#09A0B2']
    fig = go.Figure()
    for (label, series), color in zip(metrics.items(), colors):
        fig.add_trace(go.Scatter(
            x=series.index,
            y=series.values,
            mode='lines+markers',
            name=label,
            line=dict(color=color),
            hoverinfo="x+y+name"
        ))

    fig.update_layout(
        title='Yearly Trend: Incidents, Killed & Injured',
        xaxis_title='Year',
        yaxis_title='Count',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99, font=dict(size=12, color="black"), bgcolor="rgba(0,0,0,0)")
    )
    return fig

###############################################################################
#                            MONTHLY TREND                                    #
###############################################################################

def monthly_trend_analysis(
    df: pd.DataFrame,
    graph_title: str = "Monthly Trend: Incidents Over the Calendar Year"
) -> go.Figure:
    """
    Creates a bar chart for monthly incident counts with an average line.
    """
    if df.empty:
        return go.Figure()

    monthly_counts = df['Month'].value_counts()
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_counts = monthly_counts.reindex(months_order, fill_value=0)
    df_monthly = pd.DataFrame({'Month': monthly_counts.index, 'Count': monthly_counts.values})

    color_scale = [[0, 'lightgray'], [1, '#00629b']]
    fig = px.bar(df_monthly, x='Month', y='Count', title=graph_title,
                 color='Count', color_continuous_scale=color_scale)

    avg_count = df_monthly['Count'].mean()
    fig.add_hline(
        y=avg_count,
        line_dash="dash",
        line_color="#ED2F2C",
        annotation_text=f"Monthly Avg: {avg_count:.2f}",
        annotation_position="top left",
        annotation_font_color="#ED2F2C"
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Incident Count',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        autosize=True,
        height=400
    )
    return fig

###############################################################################
#                         DISTRIBUTION BY KEY FACTOR                          #
###############################################################################

def display_key_factor_distribution(df: pd.DataFrame) -> None:
    """
    Displays a bar chart that shows distribution by chosen factor (Outcome or Intent).
    """
    if df.empty:
        st.info("No data available for distribution analysis.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<div style='font-size: {FONT_SIZE}; font-weight: bold;'>Distribution by Key Factor</div>",
            unsafe_allow_html=True
        )
    with col2:
        option = st.selectbox("Select Factor", ('Outcome', 'Intent'))

    chart = plot_factor_distribution(df, option)
    st.plotly_chart(chart, use_container_width=True)

def plot_factor_distribution(df: pd.DataFrame, column_name: str) -> go.Figure:
    """
    Creates a horizontal bar chart showing counts and percentages for a given column.
    """
    if df.empty:
        return go.Figure()

    df_count = df[column_name].value_counts().reset_index()
    df_count.columns = [column_name, 'Count']
    total_count = df_count['Count'].sum()
    df_count['Percent'] = (df_count['Count'] / total_count) * 100 if total_count else 0

    fig = px.bar(
        df_count,
        x='Count',
        y=column_name,
        orientation='h',
        color='Count',
        color_continuous_scale=['#ED2F2C', '#065388', '#09A0B2']
    )

    for i, row in df_count.iterrows():
        fig.add_annotation(
            text=f"{row['Percent']:.2f}%",
            x=row['Count'],
            y=row[column_name],
            showarrow=False,
            font=dict(size=14)
        )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(tickangle=-30),
        autosize=True,
        height=400
    )
    return fig

###############################################################################
#                           HEATMAP (INTENT vs OUTCOME)                       #
###############################################################################

def create_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Creates a heatmap of Intent vs. Outcome that displays both the incident counts and
    the percentage of the total incidents in hover text.
    """
    if df.empty:
        return go.Figure()

    pivot_table = pd.pivot_table(df, values='ID', index='Intent', columns='Outcome', aggfunc='count').fillna(0)
    if pivot_table.empty:
        return go.Figure()

    colorscale = 'Blues'
    max_val = pivot_table.values.max()
    overall_total = pivot_table.values.sum()
    percent_matrix = (pivot_table.values / overall_total) * 100 if overall_total else pivot_table.values

    heatmap_trace = go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns.tolist(),
        y=pivot_table.index.tolist(),
        colorscale=colorscale,
        zmin=0,
        zmax=max_val,
        colorbar=dict(title='Incident Count'),
        customdata=percent_matrix,
        hovertemplate=(
            "Outcome: %{x}<br>"
            "Intent: %{y}<br>"
            "Incidents: %{z}<br>"
            "Percent of Total: %{customdata:.1f}%<extra></extra>"
        )
    )

    annotations = []
    for i, row in enumerate(pivot_table.values):
        for j, value in enumerate(row):
            annotations.append(dict(
                x=pivot_table.columns[j],
                y=pivot_table.index[i],
                text=str(int(value)),
                showarrow=False,
                font=dict(color='black' if value < (max_val / 2) else 'white', size=12)
            ))

    fig = go.Figure(data=[heatmap_trace])
    fig.update_layout(
        title='Intent vs. Outcome: Heatmap Analysis',
        xaxis_title='Outcome',
        yaxis_title='Intent',
        annotations=annotations,
        margin=dict(l=100, r=100, t=100, b=100),
        width=1200,
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig

###############################################################################
#                            STATEWISE ANALYSIS                               #
###############################################################################

def plot_statewise_data(df: pd.DataFrame) -> Tuple[go.Figure, go.Figure]:
    """
    Generates a dual-axis bar+line chart and an enhanced US map for statewise analysis.
    """
    if df.empty:
        return go.Figure(), go.Figure()

    incidents_by_state = df['State_name'].value_counts().reset_index()
    incidents_by_state.columns = ['State_name', 'Number of Incidents']
    incidents_by_state.sort_values(by='Number of Incidents', ascending=False, inplace=True)

    total_incidents = incidents_by_state['Number of Incidents'].sum()
    incidents_by_state['Running % of Total'] = (
        incidents_by_state['Number of Incidents'].cumsum() / total_incidents * 100
    )

    colors = ['#065388'] * len(incidents_by_state)
    fig_bar_line = plot_dual_axis_bar_and_line(
        incidents_by_state, 
        'Number of Incidents', 
        "Running % of Total", 
        colors
    )
    fig_bar_line.update_layout(autosize=True, height=400)

    fig_map = generate_density_map(df)
    return fig_bar_line, fig_map

def plot_dual_axis_bar_and_line(
    data: pd.DataFrame,
    bar_col: str,
    line_col: str,
    colors: List[str]
) -> go.Figure:
    """
    Creates a dual-axis chart with bars (incidents) and a line (cumulative percentage).
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['State_name'],
        y=data[bar_col],
        marker_color=colors,
        name=bar_col
    ))
    fig.add_trace(go.Scatter(
        x=data['State_name'],
        y=data[line_col],
        mode='lines+markers',
        line=dict(color='red'),
        name=line_col,
        yaxis='y2'
    ))
    fig.update_layout(
        title='Statewise Overview: Incidents & Cumulative Impact',
        xaxis=dict(title='State', tickangle=90),
        yaxis=dict(title=bar_col),
        yaxis2=dict(
            title=line_col, 
            overlaying='y',
            side='right',
            tickfont=dict(color='red')
        ),
        legend=dict(x=0, y=1)
    )
    return fig

def generate_density_map(
    df: pd.DataFrame,
    lat_col: str = 'Latitude',
    lon_col: str = 'Longitude',
    killed_col: str = 'Number Killed',
    wounded_col: str = 'Number Wounded'
) -> go.Figure:
    """
    Creates a bubble map of incidents across the US using Plotly's scatter_geo.
    """
    if df.empty:
        return go.Figure()

    df_valid = df.dropna(subset=[lat_col, lon_col]).copy()
    df_valid[lat_col] = pd.to_numeric(df_valid[lat_col], errors='coerce')
    df_valid[lon_col] = pd.to_numeric(df_valid[lon_col], errors='coerce')
    df_valid = df_valid.dropna(subset=[lat_col, lon_col])

    df_valid['Total Casualties'] = df_valid[killed_col] + df_valid[wounded_col]

    fig = px.scatter_geo(
        df_valid,
        lat=lat_col,
        lon=lon_col,
        color='Total Casualties',
        size='Total Casualties',
        size_max=30,
        hover_name='City' if 'City' in df_valid.columns else None,
        hover_data={
            'State': True if 'State' in df_valid.columns else False,
            'Total Casualties': True,
            killed_col: True,
            wounded_col: True
        },
        color_continuous_scale='Reds',
        scope='usa',
        projection='albers usa'
    )

    fig.update_layout(
        width=1200,
        height=700,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='white'
    )
    return fig

def create_top_cities_bar_plot(df: pd.DataFrame) -> go.Figure:
    """
    Creates a horizontal bar chart for the top 10 cities with the most incidents.
    """
    if df.empty:
        return go.Figure()

    city_counts = df['City'].value_counts().head(10)
    df_top_cities = pd.DataFrame({'City': city_counts.index, 'Number of Incidents': city_counts.values})

    color_scale = px.colors.sequential.RdBu[::-1]
    fig = px.bar(
        df_top_cities,
        y='City',
        x='Number of Incidents',
        orientation='h',
        color='Number of Incidents',
        color_continuous_scale=color_scale,
        text='Number of Incidents'
    )
    fig.update_layout(
        title='Top 10 Most Impacted Cities',
        xaxis_title='Incident Count',
        yaxis_title='City',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        autosize=True,
        height=400
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    return fig

###############################################################################
#                        DYNAMIC OBSERVATION FUNCTIONS                        #
###############################################################################

def generate_yearly_trend_observations(df: pd.DataFrame) -> str:
    """
    Generates a storytelling HTML snippet with observations on yearly trends.
    This interpretation goes deeper into how the data evolves from the earliest
    available year to the latest, highlights peak years, and notes major shifts
    or anomalies (e.g., the pandemic).
    """
    if df.empty:
        return "<p><em>No data available to narrate the yearly journey.</em></p>"

    yearly_counts = df.groupby('Year').size().sort_index()
    if yearly_counts.empty:
        return "<p><em>No valid yearly data found.</em></p>"

    earliest_year = int(yearly_counts.index.min())
    latest_year = int(yearly_counts.index.max())
    peak_year = int(yearly_counts.idxmax())
    peak_count = int(yearly_counts.max())
    start_count = int(yearly_counts.loc[earliest_year])
    end_count = int(yearly_counts.loc[latest_year])
    from_peak_change = ((end_count - peak_count) / peak_count * 100) if peak_count else 0
    change_from_start = ((end_count - start_count) / start_count * 100) if start_count else 0

    notes = []
    # Example note for partial data in a future year
    if 2025 in yearly_counts.index:
        notes.append(
            "<div><b style='font-size:80%; color:#f44336;'>Partial Data Disclaimer:</b> "
            "<span style='font-size:70%;'>Some 2025 incidents may not yet be reported, so trends for this year are still unfolding.</span></div>"
        )

    # Example reflection on the dip in 2020
    if {2019, 2020, 2021}.issubset(yearly_counts.index):
        avg_around = (yearly_counts.loc[2019] + yearly_counts.loc[2021]) / 2
        if avg_around and yearly_counts.loc[2020] < (avg_around * 0.8):
            notes.append(
                "<div><b style='font-size:80%; color:#f44336;'>Pandemic Impact:</b> "
                "<span style='font-size:70%;'>A noticeable dip in 2020 may reflect school closures or underreporting during the pandemic.</span></div>"
            )

    notes_html = "".join(notes)

    html_obs = f"""
    <p style="font-size:90%;"><b>Yearly Trend Analysis:</b></p>
    <div style="font-size:90%;">
        <div><b style="font-size:80%; color:#f44336;">Start of Record ({earliest_year}):</b> {start_count} incidents</div>
        <div><b style="font-size:80%; color:#f44336;">Peak Year ({peak_year}):</b> {peak_count} incidents</div>
        <div><b style="font-size:80%; color:#f44336;">Latest Year ({latest_year}):</b> {end_count} incidents</div>
        <div><b style="font-size:80%; color:#f44336;">Change from Peak:</b> {from_peak_change:.1f}%</div>
        <div><b style="font-size:80%; color:#f44336;">Overall Shift Since {earliest_year}:</b> {change_from_start:.1f}%</div>
        {notes_html}
    </div>
    <p style="font-size:90%;">
        Overall, this chart helps contextualize how incidents have evolved over time.
        A rising trend may indicate worsening circumstances or better reporting, while 
        decreases might reflect successful interventions or external factors.
    </p>
    """
    return html_obs


def generate_monthly_trend_observations(df: pd.DataFrame) -> str:
    """
    Generates a storytelling HTML snippet with observations on monthly trends.
    This highlights the highest and lowest incidence months and discusses
    potential reasons behind seasonal or monthly fluctuations.
    """
    if df.empty:
        return "<p><em>No monthly data available to share the story.</em></p>"

    monthly_counts = df['Month'].value_counts()
    if monthly_counts.empty:
        return "<p><em>Monthly data is missing.</em></p>"

    top_month = monthly_counts.idxmax()
    top_count = monthly_counts.max()
    bottom_month = monthly_counts.idxmin()
    bottom_count = monthly_counts.min()
    total_incidents = df.shape[0]

    html_obs = f"""
    <p style="font-size: 90%;"><b>Monthly Trend Insights:</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size: 80%; color: #f44336;">Highest Activity:</b>
            <span style="font-size:70%;">
                {top_month} logged {top_count} incidents, possibly reflecting factors 
                like school in-session schedules or significant local events.
            </span>
        </li>
        <li><b style="font-size: 80%; color: #f44336;">Lowest Activity:</b>
            <span style="font-size:70%;">
                {bottom_month} had only {bottom_count} incidents, which could coincide 
                with holiday breaks or other cyclical slowdowns.
            </span>
        </li>
        <li><b style="font-size: 80%; color: #f44336;">Total Records Analyzed:</b>
            <span style="font-size:70%;">{total_incidents} incidents across all months.</span>
        </li>
    </ul>
    <p style="font-size:90%;">
        These monthly variations may hint at seasonal effects, school calendars, or 
        broader societal patterns influencing when incidents are most likely to occur.
    </p>
    """
    return html_obs


def generate_distribution_observations(df: pd.DataFrame) -> str:
    """
    Generates a narrative HTML snippet about distribution of Intent and Outcome.
    Provides context on the most common motives or outcomes and how they
    shape our understanding of the data.
    """
    if df.empty:
        return "<p><em>No distribution data available to reflect upon.</em></p>"

    intent_counts = df['Intent'].value_counts()
    outcome_counts = df['Outcome'].value_counts()

    # Build lines for the top intent and top outcome
    intent_line = ""
    if not intent_counts.empty:
        top_intent = intent_counts.idxmax()
        intent_pct = (intent_counts[top_intent] / intent_counts.sum() * 100)
        intent_line = (
            f"<li><b style='font-size:80%; color:#f44336;'>Most Common Intent:</b> "
            f"<span style='font-size:70%;'>{top_intent}</span> "
            f"(~{intent_pct:.1f}% of all cases)</li>"
        )

    outcome_line = ""
    if not outcome_counts.empty:
        top_outcome = outcome_counts.idxmax()
        outcome_pct = (outcome_counts[top_outcome] / outcome_counts.sum() * 100)
        outcome_line = (
            f"<li><b style='font-size:80%; color:#f44336;'>Most Common Outcome:</b> "
            f"<span style='font-size:70%;'>{top_outcome}</span> "
            f"(~{outcome_pct:.1f}% of reported outcomes)</li>"
        )

    if not intent_line and not outcome_line:
        return "<p><em>No distribution observations can be drawn due to insufficient data.</em></p>"

    html_obs = f"""
    <p style="font-size: 90%;"><b>Distribution Insights: Intent & Outcome</b></p>
    <ul style="font-size: 90%;">
        {intent_line}
        {outcome_line}
    </ul>
    <p style="font-size:90%;">
        Understanding the distribution of intentions and outcomes provides a clearer 
        picture of how and why these incidents occur, potentially guiding targeted 
        interventions or policy measures. 
    </p>
    """
    return html_obs


def generate_heatmap_observations(df: pd.DataFrame) -> str:
    """
    Generates a narrative HTML snippet with insights from the heatmap (Intent vs. Outcome).
    Explains which Intent-Outcome combination appears most frequently and interprets
    what that might signify about real-world circumstances.
    """
    if df.empty:
        return "<p><em>No data available to extract heatmap insights.</em></p>"

    pivot_table = pd.pivot_table(df, values='ID', index='Intent', columns='Outcome', aggfunc='count').fillna(0)
    if pivot_table.empty:
        return "<p><em>No valid data found in the heatmap.</em></p>"

    melted = pivot_table.reset_index().melt(id_vars='Intent', var_name='Outcome', value_name='Count')
    melted.sort_values(by='Count', ascending=False, inplace=True)
    if melted.empty or melted['Count'].max() == 0:
        return "<p><em>No significant patterns to report in the heatmap.</em></p>"

    # Top combination
    top_combo = melted.iloc[0]
    intent_name = top_combo['Intent']
    outcome_name = top_combo['Outcome']
    combo_count = int(top_combo['Count'])

    html_obs = f"""
    <p style="font-size: 90%;"><b>Heatmap Interpretation: Intent vs. Outcome</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size:80%; color:#f44336;">Dominant Pattern:</b>
            <span style="font-size:70%;">
                The combination of Intent: <i>{intent_name}</i> and Outcome: <i>{outcome_name}</i> 
                appears most frequently, with {combo_count} incidents recorded.
            </span>
        </li>
    </ul>
    <p style="font-size:90%;">
        This viewpoint reveals how certain motives align with specific outcomes more often 
        than others, indicating possible risk factors or intervention points. 
        Exploring less common pairings may also uncover unique scenarios worth further study.
    </p>
    """
    return html_obs


def generate_statewise_observations(df: pd.DataFrame) -> str:
    """
    Generates a narrative HTML snippet with statewise insights. Highlights which states
    bear the highest number of incidents, how that compares to the overall total,
    and the top three states' combined contribution.
    """
    if df.empty:
        return "<p><em>No state data available for insights.</em></p>"

    state_counts = df['State_name'].value_counts()
    if state_counts.empty:
        return "<p><em>No state information available.</em></p>"

    total = state_counts.sum()
    top_states = state_counts.head(3)
    top_list = [f"{st} ({val})" for st, val in top_states.items()]
    top3_pct = (top_states.sum() / total * 100) if total else 0
    top_state = top_states.index[0]
    top_state_count = top_states.iloc[0]
    top_state_pct = (top_state_count / total * 100) if total else 0

    html_obs = f"""
    <p style="font-size: 90%;"><b>Statewise Analysis:</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size:80%; color:#f44336;">Leading States:</b>
            <span style="font-size:70%;">
                Top three states collectively: {", ".join(top_list)} — 
                contributing ~{top3_pct:.1f}% of all incidents.
            </span>
        </li>
        <li><b style="font-size:80%; color:#f44336;">Highest Concentration:</b>
            <span style="font-size:70%;">
                {top_state} alone accounts for ~{top_state_pct:.1f}% 
                ({top_state_count} incidents) of the dataset.
            </span>
        </li>
    </ul>
    <p style="font-size:90%;">
        States with higher counts might reflect larger populations, differing gun laws, 
        or other localized factors. Further analysis could explore per-capita rates or 
        demographic variables to provide deeper context.
    </p>
    """
    return html_obs


def generate_top_cities_observations(df: pd.DataFrame) -> str:
    """
    Generates a narrative HTML snippet with observations on top cities. Emphasizes
    how concentrated incidents can be in certain urban areas and highlights the
    other most impacted locations.
    """
    if df.empty:
        return "<p><em>No data available on top cities.</em></p>"

    city_counts = df['City'].value_counts()
    if city_counts.empty:
        return "<p><em>No city data to report.</em></p>"

    top_city = city_counts.index[0]
    top_city_count = city_counts.iloc[0]
    next_cities = city_counts.index[1:4]  # up to the next 3
    next_cities_str = ", ".join(next_cities) if len(next_cities) > 0 else "None listed"

    html_obs = f"""
    <p style="font-size: 90%;"><b>City-Level Observations:</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size:80%; color:#f44336;">Highest Incidence City:</b>
            <span style="font-size:70%;">
                {top_city} leads with {top_city_count} recorded incidents.
            </span>
        </li>
        <li><b style="font-size:80%; color:#f44336;">Other Noteworthy Hubs:</b>
            <span style="font-size:70%;">
                {next_cities_str}
            </span>
        </li>
    </ul>
    <p style="font-size:90%;">
        These city-specific patterns suggest that particular urban centers experience 
        repeated incidents, possibly due to population density or localized risk factors. 
        Identifying these hubs is crucial for targeted prevention strategies.
    </p>
    """
    return html_obs
