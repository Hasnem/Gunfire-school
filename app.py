import streamlit as st
from PIL import Image
from helpers import (
    style_metric_cards,
    load_and_preprocess_data,
    apply_sidebar_filters,
    display_header,
    display_latest_incident,
    metric_cards,
    display_trends,
    monthly_trend_analysis,
    display_key_factor_distribution,  # RENAMED
    create_heatmap,
    plot_statewise_data,
    create_top_cities_bar_plot,
    generate_yearly_trend_observations,
    generate_monthly_trend_observations,
    generate_distribution_observations,
    generate_heatmap_observations,
    generate_statewise_observations,
    generate_top_cities_observations
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

    # 2) Load data & Apply filters
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

    # 3) Latest incident details (on the sidebar) & Key Metrics
    display_latest_incident(df_filtered)
    metric_cards(df_filtered)

    # 4) Yearly Trend Analysis
    fig_yearly = display_trends(df_filtered)  # Multi-series line chart
    st.plotly_chart(fig_yearly, use_container_width=True)
    yearly_obs = generate_yearly_trend_observations(df_filtered)
    st.markdown(yearly_obs, unsafe_allow_html=True)
    st.divider()

    # 5) Monthly Trend Analysis
    fig_monthly = monthly_trend_analysis(df_filtered)
    st.plotly_chart(fig_monthly, use_container_width=True)
    monthly_obs = generate_monthly_trend_observations(df_filtered)
    st.markdown(monthly_obs, unsafe_allow_html=True)
    st.divider()

    # 6) Distribution by Key Factor (Outcome vs. Intent)
    display_key_factor_distribution(df_filtered)
    dist_obs = generate_distribution_observations(df_filtered)
    st.markdown(dist_obs, unsafe_allow_html=True)
    st.divider()

    # 7) Heatmap: Intent vs. Outcome
    fig_heatmap = create_heatmap(df_filtered)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    heatmap_obs = generate_heatmap_observations(df_filtered)
    st.markdown(heatmap_obs, unsafe_allow_html=True)
    st.divider()

    # 8) Statewise Analysis: Dual-axis chart & enhanced US map
    fig_state_bar, fig_state_map = plot_statewise_data(df_filtered)
    st.plotly_chart(fig_state_bar, use_container_width=True)
    statewise_obs = generate_statewise_observations(df_filtered)
    st.markdown(statewise_obs, unsafe_allow_html=True)
    st.divider()

    # 9) Top 10 Most Impacted Cities
    fig_cities = create_top_cities_bar_plot(df_filtered)
    st.plotly_chart(fig_cities, use_container_width=True)
    top_cities_obs = generate_top_cities_observations(df_filtered)
    st.markdown(top_cities_obs, unsafe_allow_html=True)
    st.divider()

    # 10) Nationwide Map
    display_map(fig_state_map)

def display_map(fig):
    st.markdown(
        f"<div style='font-size: {FONT_SIZE}; font-weight: bold;'>Nationwide Map of Incidents</div>",
        unsafe_allow_html=True
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
