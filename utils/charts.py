import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
# Import the state mapping from our utils_common (RELATIVE import)
from utils.utils_common import STATE_MAPPING

def plot_yearly_trend(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    df['Year'] = pd.to_datetime(df['Incident Date']).dt.year
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
            line=dict(color=color)
        ))
    fig.update_layout(
        title="Yearly Trend: Incidents, Killed & Injured",
        xaxis_title="Year",
        yaxis_title="Count",
        autosize=True,
        height=400
    )
    return fig

def display_monthly_analysis(df: pd.DataFrame):
    if df.empty:
        st.warning("No data for Monthly Analysis.")
        return
    option = st.selectbox("Choose Metric for Monthly Trend", ["Number of Incidents","Total Casualties"])
    fig = plot_monthly_metric(df, option)
    st.plotly_chart(fig, use_container_width=True)

def plot_monthly_metric(df: pd.DataFrame, metric: str) -> go.Figure:
    if "Total_Casualties" not in df.columns:
        df['Total_Casualties'] = df['Number Killed'] + df['Number Wounded']
    months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if metric == "Number of Incidents":
        monthly_series = df.groupby('Month').size()
        title = "Monthly Trend: Number of Incidents"
    else:
        monthly_series = df.groupby('Month')['Total_Casualties'].sum()
        title = "Monthly Trend: Total Casualties"
    monthly_series = monthly_series.reindex(months_order, fill_value=0)
    chart_df = pd.DataFrame({"Month":monthly_series.index, "Value":monthly_series.values})
    fig = px.bar(
        chart_df, x="Month", y="Value", title=title, 
        color="Value", color_continuous_scale=[[0,'lightgray'],[1,'#00629b']]
    )
    avg_val = chart_df["Value"].mean()
    fig.add_hline(y=avg_val, line_dash="dash", line_color="#ED2F2C", annotation_text=f"Monthly Avg: {avg_val:.2f}")
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=metric,
        autosize=True,
        height=400
    )
    return fig

def display_day_of_week_analysis(df: pd.DataFrame):
    if df.empty:
        st.warning("No data for Day-of-Week Analysis.")
        return
    option = st.selectbox("Choose Metric for Day-of-Week Trend", ["Number of Incidents","Total Casualties"])
    fig = plot_day_of_week_distribution(df, option)
    st.plotly_chart(fig, use_container_width=True)

def plot_day_of_week_distribution(df: pd.DataFrame, metric: str) -> go.Figure:
    if "Total_Casualties" not in df.columns:
        df['Total_Casualties'] = df['Number Killed'] + df['Number Wounded']
    day_order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    if metric == "Number of Incidents":
        series = df.groupby("DayOfWeek").size()
        title = "Day-of-Week: Number of Incidents"
    else:
        series = df.groupby("DayOfWeek")["Total_Casualties"].sum()
        title = "Day-of-Week: Total Casualties"
    series = series.reindex(day_order, fill_value=0)
    chart_df = pd.DataFrame({"DayOfWeek":series.index, "Value":series.values})
    fig = px.bar(
        chart_df, x="DayOfWeek", y="Value", title=title,
        color="Value", color_continuous_scale=px.colors.sequential.OrRd
    )
    fig.update_layout(autosize=True, height=400)
    return fig

def display_key_factor_distribution(df: pd.DataFrame):
    if df.empty:
        st.info("No data available for distribution analysis.")
        return
    factor = st.selectbox("Select Factor", ("Outcome","Intent"))
    fig = plot_factor_distribution(df, factor)
    st.plotly_chart(fig, use_container_width=True)

def plot_factor_distribution(df: pd.DataFrame, column_name: str) -> go.Figure:
    if df.empty:
        return go.Figure()
    counts = df[column_name].value_counts().reset_index()
    counts.columns = [column_name, "Count"]
    total_count = counts["Count"].sum()
    counts["Percent"] = (counts["Count"]/total_count)*100 if total_count else 0
    fig = px.bar(counts, x="Count", y=column_name, orientation='h', color="Count",
                 color_continuous_scale=['#ED2F2C','#065388','#09A0B2'])
    for i, row in counts.iterrows():
        fig.add_annotation(text=f"{row['Percent']:.1f}%", x=row["Count"], y=row[column_name], showarrow=False)
    fig.update_layout(autosize=True, height=400)
    return fig

def create_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    pivot = pd.pivot_table(df, values='ID', index='Intent', columns='Outcome', aggfunc='count').fillna(0)
    if pivot.empty:
        return go.Figure()
    total = pivot.values.sum()
    perc_matrix = pivot.values/total*100 if total else pivot.values
    heatmap = go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale='Blues',
        customdata=perc_matrix,
        hovertemplate="Outcome: %{x}<br>Intent: %{y}<br>Incidents: %{z}<br>Percent: %{customdata:.1f}%<extra></extra>"
    )
    fig = go.Figure(data=[heatmap])
    fig.update_layout(
        title="Intent vs. Outcome Heatmap",
        autosize=True,
        height=600
    )
    return fig

def plot_statewise_data(df: pd.DataFrame):
    if df.empty:
        return go.Figure(), go.Figure()
    st_counts = df['State_name'].value_counts().reset_index()
    st_counts.columns = ['State_name','Number of Incidents']
    st_counts.sort_values(by='Number of Incidents', ascending=False, inplace=True)
    total_inc = st_counts['Number of Incidents'].sum()
    st_counts['Running %'] = st_counts['Number of Incidents'].cumsum()/total_inc*100

    fig_bar_line = go.Figure()
    fig_bar_line.add_trace(go.Bar(
        x=st_counts['State_name'],
        y=st_counts['Number of Incidents'],
        name='Number of Incidents',
        marker_color='#065388'
    ))
    fig_bar_line.add_trace(go.Scatter(
        x=st_counts['State_name'],
        y=st_counts['Running %'],
        mode='lines+markers',
        line=dict(color='red'),
        name='Running %',
        yaxis='y2'
    ))
    fig_bar_line.update_layout(
        title="Statewise Overview: Incidents & Cumulative Impact",
        xaxis=dict(title="State",tickangle=90),
        yaxis=dict(title="Incidents"),
        yaxis2=dict(title="Running %",overlaying='y',side='right'),
        autosize=True,
        height=400
    )

    fig_map = generate_density_map(df)
    return fig_bar_line, fig_map

def generate_density_map(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    df_valid = df.dropna(subset=['Latitude','Longitude']).copy()
    df_valid['Total_Casualties'] = df_valid['Number Killed'] + df_valid['Number Wounded']
    fig = px.scatter_geo(
        df_valid,
        lat='Latitude',
        lon='Longitude',
        color='Total_Casualties',
        size='Total_Casualties',
        size_max=30,
        hover_data=['City','State','Number Killed','Number Wounded','Total_Casualties'],
        color_continuous_scale='Reds',
        scope='usa',
        projection='albers usa'
    )
    fig.update_layout(autosize=True, height=700)
    return fig

def create_top_cities_bar_plot(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    top_cities = df['City'].value_counts().head(10)
    df_top = pd.DataFrame({"City":top_cities.index,"Incidents":top_cities.values})
    fig = px.bar(df_top, y='City', x='Incidents', orientation='h', color='Incidents',
                 color_continuous_scale=px.colors.sequential.RdBu[::-1])
    fig.update_layout(title="Top 10 Most Impacted Cities", autosize=True, height=400)
    return fig

def display_top_tragic_incidents(df: pd.DataFrame, n:int=5):
    if df.empty:
        st.info("No data to identify top tragic incidents.")
        return
    df['Total_Casualties'] = df['Number Killed'] + df['Number Wounded']
    sorted_df = df.sort_values(by='Total_Casualties', ascending=False).head(n)
    st.table(sorted_df[['Incident Date','City','State_name','Number Killed','Number Wounded','Total_Casualties']])

def display_map_scatter(fig):
    # Just display the map as is (no color scale select)
    st.plotly_chart(fig, use_container_width=True)

def plot_state_choropleth(df: pd.DataFrame, color_scale:str="Reds") -> go.Figure:
    if df.empty:
        return go.Figure()
    # Use the STATE_MAPPING from utils_common
    rev_map = {v:k for k,v in STATE_MAPPING.items()}
    st_counts = df['State_name'].value_counts().reset_index()
    st_counts.columns=['State_name','Incidents']
    st_counts['Abbrev'] = st_counts['State_name'].map(rev_map)
    st_counts.dropna(subset=['Abbrev'], inplace=True)
    fig = px.choropleth(
        st_counts,
        locations='Abbrev',
        color='Incidents',
        locationmode='USA-states',
        scope='usa',
        color_continuous_scale=color_scale,
        hover_name='State_name'
    )
    fig.update_layout(title="Choropleth: Incident Counts by State", autosize=True, height=700)
    return fig
