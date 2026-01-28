import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime

# Local imports
from about_page import about_page
from utils.narrative_analysis import display_narrative_analysis
from utils.data_loading import load_and_preprocess_data
from utils.data_filters import apply_sidebar_filters
from utils.utils_common import (
    display_header, display_metric_cards, display_latest_incident,
    display_year_disclaimer, create_summary_stats, format_percentage,
    format_number, display_latest_incident_ticker, display_latest_incident_compact
)
from utils.charts import (
    plot_yearly_trend, display_monthly_analysis, display_day_of_week_analysis,
    display_key_factor_distribution, create_heatmap, plot_statewise_data,
    create_top_cities_bar_plot, display_top_tragic_incidents, create_state_choropleth
)
from utils.observations import (
    generate_yearly_trend_observations, generate_monthly_trend_observations,
    generate_day_of_week_observations, generate_distribution_observations,
    generate_heatmap_observations, generate_statewise_observations,
    generate_top_cities_observations, generate_top_tragic_incidents_observation,
    generate_choropleth_observations, get_observation_styles
)
from utils.executive_report import generate_executive_report


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="School Gun Violence Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## Navigation")
        page = st.selectbox(
            "Select View",
            ["Dashboard", "Executive Report", "About"]
        )
        
        # Add logo if available
        try:
            logo = Image.open("Everytown_final_logo.png")
            st.image(logo, width='stretch')
        except:
            pass
    
    # Route to appropriate page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Executive Report":
        show_executive_report()
    else:
        about_page()


def apply_custom_css():
    """Apply minimal custom CSS for clean appearance."""
    st.markdown("""
    <style>
    /* Clean typography */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Remove default Streamlit styling */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* Clean metric styling */
    [data-testid="metric-container"] {
        background-color: #f8f9fa;
        border-left: 3px solid #3498db;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add observation styles
    st.html(get_observation_styles())


def show_dashboard():
    """Display the main dashboard."""
    
    # Header
    display_header()
    
    # Load data
    with st.spinner("Loading data..."):
        df, quality_metrics = load_and_preprocess_data()
    
    if df.empty:
        st.error("Unable to load data. Please check your connection and try again.")
        return
    
    # Apply filters
    df_filtered = apply_sidebar_filters(df)
    
    # Display latest incident as news ticker at the top
    display_latest_incident_ticker(df_filtered)
    
    # Display key metrics
    display_metric_cards(df_filtered)
    
    # Check for current year data
    current_year = datetime.now().year
    if current_year in df_filtered['Year'].values:
        display_year_disclaimer(current_year)
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Trends", 
        "📍 Geography", 
        "⚠️ Severity",
        "📝 Narratives"
    ])
    
    with tab1:
        show_trends_tab(df_filtered)
    
    with tab2:
        show_geography_tab(df_filtered)
    
    with tab3:
        show_severity_tab(df_filtered)
    
    with tab4:
        display_narrative_analysis(df_filtered)
    
    # Data quality note
    with st.expander("ℹ️ About the Data", expanded=False):
        show_data_info(quality_metrics, df_filtered)


def show_trends_tab(df: pd.DataFrame):
    """Show temporal trends analysis."""
    
    # Yearly trend
    st.markdown("### Annual Trends")
    yearly_fig = plot_yearly_trend(df)
    st.plotly_chart(yearly_fig, width='stretch')
    generate_yearly_trend_observations(df)
    
    st.markdown("---")
    
    # Monthly and weekly patterns in columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Monthly Patterns")
        display_monthly_analysis(df)
        generate_monthly_trend_observations(df)
    
    with col2:
        st.markdown("### Weekly Patterns")
        display_day_of_week_analysis(df)
        generate_day_of_week_observations(df)


def show_geography_tab(df: pd.DataFrame):
    """Show geographic distribution analysis."""
    
    # State-level analysis
    st.markdown("### Geographic Distribution")
    
    # Bar chart and observations
    state_bar, _ = plot_statewise_data(df)
    st.plotly_chart(state_bar, width='stretch')
    generate_statewise_observations(df)
    
    st.markdown("---")
    
    # Map visualization
    st.markdown("### National Heat Map")
    choropleth_fig = create_state_choropleth(df)
    st.plotly_chart(choropleth_fig, width='stretch')
    generate_choropleth_observations(df)
    
    st.markdown("---")
    
    # City analysis
    st.markdown("### Cities Most Affected")
    city_fig = create_top_cities_bar_plot(df)
    st.plotly_chart(city_fig, width='stretch')
    generate_top_cities_observations(df)


def show_severity_tab(df: pd.DataFrame):
    """Show incident severity analysis."""
    
    # Severity distribution
    st.markdown("### Incident Severity")
    display_key_factor_distribution(df)
    generate_distribution_observations(df)
    
    st.markdown("---")
    
    # Intent vs Outcome patterns
    st.markdown("### Intent and Outcome Patterns")
    heatmap_fig = create_heatmap(df)
    st.plotly_chart(heatmap_fig, width='stretch')
    generate_heatmap_observations(df)
    
    st.markdown("---")
    
    # High-impact incidents
    st.markdown("### High-Impact Incidents")
    display_top_tragic_incidents(df, n=10)
    generate_top_tragic_incidents_observation(df)


def show_data_info(quality_metrics: dict, df: pd.DataFrame):
    """Show concise data information."""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Records Loaded", f"{len(df):,}")
    
    with col2:
        completeness = quality_metrics.get('completeness_score', 0)
        st.metric("Data Completeness", f"{completeness}%")
    
    with col3:
        date_range = f"{df['Incident Date'].min():%Y-%m-%d} to {df['Incident Date'].max():%Y-%m-%d}"
        st.caption("**Date Range**")
        st.caption(date_range)
    
    st.markdown("""
    **Data Source:** [Everytown Research](https://everytownresearch.org/maps/gunfire-on-school-grounds/)
    
    **Note:** Data is updated regularly as new incidents are verified. Some records may have 
    incomplete location or narrative information.
    """)


def show_executive_report():
    """Show the executive report generator."""
    
    st.markdown("# Executive Report Generator")
    st.markdown("Generate a comprehensive analysis report with insights and recommendations.")
    
    # Report options
    st.markdown("### Select Report Sections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sections = st.multiselect(
            "Include in report:",
            ["Executive Summary", "Trend Analysis", "Geographic Insights", 
             "Severity Assessment", "Recommendations"],
            default=["Executive Summary", "Trend Analysis", "Geographic Insights"]
        )
    
    with col2:
        st.info("Reports are generated in HTML format for easy viewing and sharing.")
    
    # Generate button
    if st.button("Generate Report", type="primary", width='stretch'):
        with st.spinner("Generating report..."):
            # Load data
            df, quality_metrics = load_and_preprocess_data()
            
            if df.empty:
                st.error("Failed to load data for report generation.")
                return
            
            # Apply filters
            df_filtered = apply_sidebar_filters(df)
            
            # Generate report
            report_html = generate_executive_report(
                df_filtered, 
                quality_metrics,
                sections,
                "HTML"
            )
            
            # Success message and download
            st.success("✅ Report generated successfully!")
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                label="📥 Download Report",
                data=report_html,
                file_name=f"school_violence_report_{timestamp}.html",
                mime="text/html"
            )


if __name__ == "__main__":
    main()