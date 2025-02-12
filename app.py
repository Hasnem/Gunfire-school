import streamlit as st
from PIL import Image
from helpers import (
    # Original imports
    style_metric_cards,
    load_and_preprocess_data,
    apply_sidebar_filters,
    display_header,
    display_latest_incident,
    metric_cards,
    display_trends,
    monthly_trend_analysis,
    display_key_factor_distribution,
    create_heatmap,
    plot_statewise_data,
    create_top_cities_bar_plot,
    plot_state_choropleth,
    display_top_tragic_incidents,
    generate_yearly_trend_observations,
    generate_monthly_trend_observations,
    generate_distribution_observations,
    generate_heatmap_observations,
    generate_statewise_observations,
    generate_top_cities_observations,
    generate_top_tragic_incidents_observation,
    generate_choropleth_observations,
    # NEW
    display_day_of_week_analysis,
    generate_day_of_week_observations,
    filter_by_min_casualties,  # For min casualties slider
    export_filtered_data       # For download button
)
from pages import about_page

FONT_SIZE = "16px"

def main():
    st.set_page_config(page_title="Gun-Schools", page_icon=":school:", layout="wide")

    # Sidebar navigation and logo
    page = st.sidebar.selectbox("Choose a page", ["Dashboard", "About"])
    try:
        image = Image.open('Everytown_final_logo.png')
        st.sidebar.image(image, use_container_width=True)
    except Exception:
        st.sidebar.write("Logo Image Not Found or Not Provided.")

    if page == "Dashboard":
        dashboard_page()
    else:
        about_page()

def dashboard_page():
    # 1) Main Title / Header
    display_header()
    st.divider()

    # 2) Load data & Apply basic filters
    df = load_and_preprocess_data()
    df_filtered = apply_sidebar_filters(df)

    st.markdown(
        """
        <p style="font-size: 80%; color: #757575;">
            <b>Note:</b> The insights below evolve with your filter selections. (Data for 2025 may be partial.)
        </p>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    # 3) Additional filter: Minimum casualties
    min_cas = st.slider(
        "Minimum Total Casualties (Killed + Wounded)",
        min_value=0, max_value=50, value=0, step=1,
        help="Filter out incidents that have total casualties below this threshold."
    )
    df_filtered = filter_by_min_casualties(df_filtered, min_cas)

    # 4) Download filtered data button
    export_filtered_data(df_filtered)

    st.divider()

    # 5) Sidebar: Latest incident details & Key Metrics
    display_latest_incident(df_filtered)
    metric_cards(df_filtered)

    # 6) Yearly Trend
    fig_yearly = display_trends(df_filtered)
    st.plotly_chart(fig_yearly, use_container_width=True)
    yearly_obs = generate_yearly_trend_observations(df_filtered)
    st.markdown(yearly_obs, unsafe_allow_html=True)
    st.divider()

    # 7) Monthly Trend
    fig_monthly = monthly_trend_analysis(df_filtered)
    st.plotly_chart(fig_monthly, use_container_width=True)
    monthly_obs = generate_monthly_trend_observations(df_filtered)
    st.markdown(monthly_obs, unsafe_allow_html=True)
    st.divider()

    # 8) Distribution by Outcome/Intent
    display_key_factor_distribution(df_filtered)
    dist_obs = generate_distribution_observations(df_filtered)
    st.markdown(dist_obs, unsafe_allow_html=True)
    st.divider()

    # 9) Heatmap (Intent vs. Outcome)
    fig_heatmap = create_heatmap(df_filtered)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    heatmap_obs = generate_heatmap_observations(df_filtered)
    st.markdown(heatmap_obs, unsafe_allow_html=True)
    st.divider()

    # 10) Day-of-Week Analysis
    display_day_of_week_analysis(df_filtered)
    dow_obs = generate_day_of_week_observations(df_filtered)
    st.markdown(dow_obs, unsafe_allow_html=True)
    st.divider()

    # 11) Statewise Analysis (bar+line)
    fig_state_bar, fig_state_map_scatter = plot_statewise_data(df_filtered)
    st.plotly_chart(fig_state_bar, use_container_width=True)
    statewise_obs = generate_statewise_observations(df_filtered)
    st.markdown(statewise_obs, unsafe_allow_html=True)
    st.divider()

    # 12) Top 10 Cities
    fig_cities = create_top_cities_bar_plot(df_filtered)
    st.plotly_chart(fig_cities, use_container_width=True)
    top_cities_obs = generate_top_cities_observations(df_filtered)
    st.markdown(top_cities_obs, unsafe_allow_html=True)
    st.divider()

    # 13) Top 5 Most Tragic Incidents
    display_top_tragic_incidents(df_filtered)
    tragic_obs = generate_top_tragic_incidents_observation(df_filtered)
    st.markdown(tragic_obs, unsafe_allow_html=True)
    st.divider()

    # 14) Improved Nationwide Map
    map_option = st.selectbox(
        "Map Type",
        ["Scatter Bubble Map", "Choropleth by Incidents"],
        help="Choose between a bubble-based scatter map or a color-coded choropleth map."
    )

    color_scale_option = st.selectbox(
        "Map Color Scale",
        ["Reds", "Blues", "Viridis", "Turbo", "Bluered", "Inferno", "Sunsetdark"],
        help="Select a color scale for map visualization."
    )

    if map_option == "Scatter Bubble Map":
        display_map_scatter(fig_state_map_scatter, color_scale_option)
    else:
        fig_choropleth = plot_state_choropleth(df_filtered, color_scale=color_scale_option)
        st.plotly_chart(fig_choropleth, use_container_width=True)
        choro_obs = generate_choropleth_observations(df_filtered)
        st.markdown(choro_obs, unsafe_allow_html=True)


def display_map_scatter(fig, color_scale: str):
    """
    Renders the scatter map with a user-selected color scale.
    """
    # Let's update the color scale of the figure if possible
    if fig.data and hasattr(fig.data[0], 'marker'):
        fig.data[0].marker.colorscale = color_scale
    st.markdown(
        f"<div style='font-size: {FONT_SIZE}; font-weight: bold;'>Nationwide Scatter Map of Incidents</div>",
        unsafe_allow_html=True
    )
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
