import streamlit as st
from PIL import Image

# Local imports
from about_page import about_page
from utils.narrative_analysis import display_narrative_analysis
from utils.data_loading import load_and_preprocess_data
from utils.data_filters import apply_sidebar_filters, filter_by_min_casualties, export_filtered_data
from utils.utils_common import display_header, display_latest_incident, metric_cards
from utils.charts import (
    plot_yearly_trend,
    display_monthly_analysis,
    display_day_of_week_analysis,
    display_key_factor_distribution,
    create_heatmap,
    plot_statewise_data,
    create_top_cities_bar_plot,
    display_top_tragic_incidents,
    plot_state_choropleth,
    display_map_scatter
)
from utils.observations import (
    generate_yearly_trend_observations,
    generate_monthly_trend_observations,
    generate_day_of_week_observations,
    generate_distribution_observations,
    generate_heatmap_observations,
    generate_statewise_observations,
    generate_top_cities_observations,
    generate_top_tragic_incidents_observation,
    generate_choropleth_observations
)
from about_page import about_page

def main():
    st.set_page_config(page_title="Gun-Schools", page_icon=":school:", layout="wide")

    # Sidebar Page Selector
    page = st.sidebar.selectbox("Choose a page", ["Dashboard", "About"])

    # Optional Logo in Sidebar
    try:
        logo = Image.open("Everytown_final_logo.png")
        st.sidebar.image(logo, use_container_width=True)
    except:
        st.sidebar.write("Logo not found or not provided.")
    
    # Page Navigation
    if page == "Dashboard":
        show_dashboard()
    else:
        about_page()

def show_dashboard():
    # Main title
    display_header()
    st.divider()

    # Load & Filter Data
    df = load_and_preprocess_data()
    df_filtered = apply_sidebar_filters(df)

    st.markdown(
        """<p style="font-size:80%; color:#757575;">
        <b>Note:</b> The insights below evolve with your filter selections. (Data for 2025 may be partial.)
        </p>""",
        unsafe_allow_html=True
    )
    st.divider()

    # Minimum casualties slider & export
    min_cas = st.slider("Minimum Total Casualties", 0, 50, 0, step=1)
    df_filtered = filter_by_min_casualties(df_filtered, min_cas)
    export_filtered_data(df_filtered)
    st.divider()

    # Sidebar: Latest Incident + Key Metrics
    display_latest_incident(df_filtered)
    metric_cards(df_filtered)

    # 1) Yearly Trend
    st.markdown("<h3>Yearly Trend Analysis</h3>", unsafe_allow_html=True)
    fig_yearly = plot_yearly_trend(df_filtered)
    st.plotly_chart(fig_yearly, use_container_width=True)
    st.markdown(generate_yearly_trend_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 2) Monthly Trend
    st.markdown("<h3>Monthly Trend Analysis</h3>", unsafe_allow_html=True)
    display_monthly_analysis(df_filtered)
    st.markdown(generate_monthly_trend_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 3) Day-of-Week
    st.markdown("<h3>Day-of-Week Analysis</h3>", unsafe_allow_html=True)
    display_day_of_week_analysis(df_filtered)
    st.markdown(generate_day_of_week_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 4) Distribution by Key Factor
    st.markdown("<h3>Distribution by Key Factor</h3>", unsafe_allow_html=True)
    display_key_factor_distribution(df_filtered)
    st.markdown(generate_distribution_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 5) Intent vs. Outcome Heatmap
    st.markdown("<h3>Intent vs. Outcome Heatmap</h3>", unsafe_allow_html=True)
    fig_heatmap = create_heatmap(df_filtered)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown(generate_heatmap_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 6) Statewise
    st.markdown("<h3>Statewise Analysis</h3>", unsafe_allow_html=True)
    fig_state_bar, fig_state_map_scatter = plot_statewise_data(df_filtered)
    st.plotly_chart(fig_state_bar, use_container_width=True)
    st.markdown(generate_statewise_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 7) Top 10 Most Impacted Cities
    st.markdown("<h3>Top 10 Most Impacted Cities</h3>", unsafe_allow_html=True)
    fig_cities = create_top_cities_bar_plot(df_filtered)
    st.plotly_chart(fig_cities, use_container_width=True)
    st.markdown(generate_top_cities_observations(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 8) Top 5 Most Tragic Incidents
    st.markdown("<h3>Top 5 Most Tragic Incidents</h3>", unsafe_allow_html=True)
    display_top_tragic_incidents(df_filtered)
    st.markdown(generate_top_tragic_incidents_observation(df_filtered), unsafe_allow_html=True)
    st.divider()

    # 9) Nationwide Map
    st.markdown("<h3>Nationwide Map</h3>", unsafe_allow_html=True)
    map_type = st.selectbox("Map Type", ["Scatter Bubble Map", "Choropleth by Incidents"])

    if map_type == "Scatter Bubble Map":
        display_map_scatter(fig_state_map_scatter)
    else:
        fig_choro = plot_state_choropleth(df_filtered)
        st.plotly_chart(fig_choro, use_container_width=True)
        st.markdown(generate_choropleth_observations(df_filtered), unsafe_allow_html=True)


    display_narrative_analysis(df_filtered)


if __name__ == "__main__":
    main()
