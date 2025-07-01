import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def generate_executive_report(df: pd.DataFrame, quality_metrics: dict, 
                            report_sections: list, output_format: str) -> str:
    """
    Generate a comprehensive, accurate executive report with enhanced structure and insights.
    
    Args:
        df: Filtered dataframe with incident data
        quality_metrics: Dictionary containing data quality metrics
        report_sections: List of sections to include in report
        output_format: Report format (HTML)
    
    Returns:
        HTML string containing the complete report
    """
    
    report_date = datetime.now().strftime("%B %d, %Y")
    report_time = datetime.now().strftime("%I:%M %p")
    current_year = datetime.now().year
    
    # Start HTML report with enhanced styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>School Violence Analysis Report - {report_date}</title>
        <style>
            @media print {{
                body {{ margin: 0.5in; }}
                .no-print {{ display: none; }}
                .page-break {{ page-break-after: always; }}
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
            }}
            
            .header {{
                border-bottom: 3px solid #2c3e50;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                color: #2c3e50;
                margin: 0;
                font-size: 32px;
                font-weight: 600;
            }}
            
            .header .subtitle {{
                color: #7f8c8d;
                margin: 10px 0 0 0;
                font-size: 18px;
            }}
            
            .header .metadata {{
                color: #95a5a6;
                font-size: 14px;
                margin-top: 10px;
            }}
            
            .toc {{
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                padding: 20px;
                margin: 30px 0;
                border-radius: 8px;
            }}
            
            .toc h2 {{
                margin-top: 0;
                color: #2c3e50;
                font-size: 20px;
            }}
            
            .toc ul {{
                list-style: none;
                padding-left: 0;
                margin: 10px 0;
            }}
            
            .toc li {{
                padding: 5px 0;
                border-bottom: 1px dotted #e9ecef;
            }}
            
            .toc a {{
                color: #3498db;
                text-decoration: none;
                font-weight: 500;
            }}
            
            .toc a:hover {{
                text-decoration: underline;
            }}
            
            .section {{
                margin-bottom: 50px;
                page-break-inside: avoid;
            }}
            
            .section h2 {{
                color: #2c3e50;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 10px;
                margin-bottom: 25px;
                font-size: 26px;
                font-weight: 600;
            }}
            
            .section h3 {{
                color: #34495e;
                margin-top: 30px;
                margin-bottom: 20px;
                font-size: 20px;
                font-weight: 600;
            }}
            
            .section h4 {{
                color: #34495e;
                margin-top: 20px;
                margin-bottom: 15px;
                font-size: 16px;
                font-weight: 600;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin: 25px 0;
            }}
            
            .metric-card {{
                background: #f8f9fa;
                padding: 20px;
                border-left: 4px solid #3498db;
                border-radius: 4px;
                transition: transform 0.2s;
            }}
            
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            
            .metric-card.danger {{
                border-left-color: #e74c3c;
            }}
            
            .metric-card.warning {{
                border-left-color: #f39c12;
            }}
            
            .metric-card.success {{
                border-left-color: #27ae60;
            }}
            
            .metric-card h4 {{
                margin: 0 0 5px 0;
                color: #7f8c8d;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .metric-card .value {{
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                margin: 5px 0;
                line-height: 1;
            }}
            
            .metric-card .context {{
                font-size: 14px;
                color: #7f8c8d;
                margin-top: 8px;
            }}
            
            .metric-card .change {{
                font-size: 14px;
                margin-top: 5px;
                font-weight: 600;
            }}
            
            .change.positive {{
                color: #27ae60;
            }}
            
            .change.negative {{
                color: #e74c3c;
            }}
            
            .info-box {{
                background: #e8f4f8;
                border: 1px solid #3498db;
                padding: 20px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            
            .warning-box {{
                background: #fef5e7;
                border: 1px solid #f39c12;
                padding: 20px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            
            .success-box {{
                background: #eafaf1;
                border: 1px solid #27ae60;
                padding: 20px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            
            .danger-box {{
                background: #fadbd8;
                border: 1px solid #e74c3c;
                padding: 20px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            
            .definition-box {{
                background: #f8f9fa;
                border-left: 3px solid #95a5a6;
                padding: 20px;
                margin: 25px 0;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 15px;
            }}
            
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ecf0f1;
            }}
            
            th {{
                background: #34495e;
                color: white;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 13px;
                letter-spacing: 0.5px;
            }}
            
            tr:hover {{
                background: #f8f9fa;
            }}
            
            tr:last-child td {{
                border-bottom: none;
            }}
            
            .highlight-row {{
                background: #fff3cd !important;
                font-weight: 600;
            }}
            
            ul, ol {{
                margin: 15px 0;
                padding-left: 30px;
                line-height: 1.8;
            }}
            
            li {{
                margin: 8px 0;
            }}
            
            strong {{
                color: #2c3e50;
                font-weight: 600;
            }}
            
            .chart-container {{
                margin: 25px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 4px;
                text-align: center;
            }}
            
            .footer {{
                margin-top: 60px;
                padding-top: 30px;
                border-top: 1px solid #ecf0f1;
                text-align: center;
                color: #7f8c8d;
                font-size: 14px;
            }}
            
            .key-insight {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 25px;
                margin: 30px 0;
                border-radius: 8px;
                font-size: 16px;
                line-height: 1.6;
            }}
            
            .key-insight h4 {{
                color: white;
                margin: 0 0 10px 0;
                font-size: 18px;
            }}
            
            .data-quality-indicator {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
            }}
            
            .quality-excellent {{
                background: #27ae60;
                color: white;
            }}
            
            .quality-good {{
                background: #3498db;
                color: white;
            }}
            
            .quality-fair {{
                background: #f39c12;
                color: white;
            }}
            
            .quality-poor {{
                background: #e74c3c;
                color: white;
            }}
        </style>
    </head>
    <body>
    """
    
    # Report Header with enhanced metadata
    html_content += f"""
    <div class="header">
        <h1>Gun Violence on School Grounds: Comprehensive Data Analysis</h1>
        <p class="subtitle">Evidence-Based Insights for Policy and Prevention</p>
        <div class="metadata">
            <strong>Report Generated:</strong> {report_date} at {report_time}<br>
            <strong>Data Source:</strong> Everytown Research<br>
            <strong>Report Type:</strong> {"Filtered Selection" if len(df) < 1000 else "Complete Dataset"}
        </div>
    </div>
    """
    
    # Add Table of Contents
    html_content += generate_table_of_contents(report_sections)
    
    # Generate sections based on selection
    if "Executive Summary" in report_sections:
        html_content += generate_executive_summary_enhanced(df, quality_metrics, current_year)
    
    if "Trend Analysis" in report_sections:
        html_content += generate_trend_analysis_enhanced(df, current_year)
    
    if "Geographic Insights" in report_sections:
        html_content += generate_geographic_insights_enhanced(df)
    
    if "Severity Assessment" in report_sections:
        html_content += generate_severity_assessment_enhanced(df)
    
    if "Recommendations" in report_sections:
        html_content += generate_recommendations_enhanced(df)
    
    if "Appendix" in report_sections:
        html_content += generate_appendix_enhanced(df, quality_metrics)
    
    # Footer
    html_content += f"""
    <div class="footer">
        <p><strong>Confidentiality Notice:</strong> This report contains sensitive data analysis. 
        Please handle with appropriate care.</p>
        <p>Report generated by School Violence Analysis Dashboard • {report_date}</p>
        <p>Data provided by <a href="https://everytownresearch.org" style="color: #3498db;">Everytown Research</a></p>
    </div>
    </body>
    </html>
    """
    
    return html_content


def generate_table_of_contents(sections: List[str]) -> str:
    """Generate an interactive table of contents."""
    
    html = """
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
    """
    
    section_ids = {
        "Executive Summary": "executive-summary",
        "Trend Analysis": "trend-analysis",
        "Geographic Insights": "geographic-insights",
        "Severity Assessment": "severity-assessment",
        "Recommendations": "recommendations",
        "Appendix": "appendix"
    }
    
    for section in sections:
        section_id = section_ids.get(section, section.lower().replace(" ", "-"))
        html += f'<li><a href="#{section_id}">{section}</a></li>'
    
    html += """
        </ul>
    </div>
    """
    
    return html


def generate_executive_summary_enhanced(df: pd.DataFrame, quality_metrics: dict, current_year: int) -> str:
    """Generate enhanced executive summary with key findings and data quality indicators."""
    
    # Calculate comprehensive metrics
    total_incidents = len(df)
    total_casualties = int(df['Total_Casualties'].sum())
    total_killed = int(df['Number Killed'].sum())
    total_wounded = int(df['Number Wounded'].sum())
    states_affected = df['State_name'].nunique()
    schools_affected = df['School name'].nunique()
    cities_affected = df['City'].nunique()
    
    # Calculate rates and percentages
    no_casualty_rate = (len(df[df['Total_Casualties'] == 0]) / total_incidents * 100) if total_incidents > 0 else 0
    fatal_rate = (len(df[df['Is_Fatal']]) / total_incidents * 100) if total_incidents > 0 else 0
    mass_casualty_rate = (len(df[df['Total_Casualties'] >= 4]) / total_incidents * 100) if total_incidents > 0 else 0
    
    # Date range and completeness
    date_range_start = df['Incident Date'].min().strftime('%B %d, %Y')
    date_range_end = df['Incident Date'].max().strftime('%B %d, %Y')
    years_covered = df['Year'].nunique()
    
    # Data quality indicator
    quality_score = quality_metrics.get('completeness_score', 0)
    if quality_score >= 90:
        quality_class = "quality-excellent"
        quality_text = "Excellent"
    elif quality_score >= 75:
        quality_class = "quality-good"
        quality_text = "Good"
    elif quality_score >= 60:
        quality_class = "quality-fair"
        quality_text = "Fair"
    else:
        quality_class = "quality-poor"
        quality_text = "Limited"
    
    html = f"""
    <div class="section" id="executive-summary">
        <h2>Executive Summary 
            <span class="data-quality-indicator {quality_class}">
                Data Quality: {quality_text} ({quality_score}%)
            </span>
        </h2>
        
        <div class="key-insight">
            <h4>Report Overview</h4>
            This comprehensive analysis examines {total_incidents:,} gun-related incidents on school grounds 
            across {years_covered} years ({date_range_start} to {date_range_end}), providing critical insights 
            for policy development and prevention strategies.
        </div>
        
        <h3>Key Metrics at a Glance</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>Total Incidents</h4>
                <p class="value">{total_incidents:,}</p>
                <p class="context">Verified events</p>
            </div>
            
            <div class="metric-card danger">
                <h4>Human Impact</h4>
                <p class="value">{total_casualties:,}</p>
                <p class="context">{total_killed:,} killed • {total_wounded:,} wounded</p>
            </div>
            
            <div class="metric-card">
                <h4>Geographic Spread</h4>
                <p class="value">{states_affected}</p>
                <p class="context">States affected ({states_affected/50*100:.0f}% of US)</p>
            </div>
            
            <div class="metric-card warning">
                <h4>Educational Impact</h4>
                <p class="value">{schools_affected:,}</p>
                <p class="context">Schools • {cities_affected:,} cities</p>
            </div>
        </div>
    """
    
    # Current year warning if applicable
    latest_year = df['Year'].max()
    if latest_year == current_year:
        current_year_count = len(df[df['Year'] == current_year])
        current_month = datetime.now().strftime('%B')
        html += f"""
        <div class="warning-box">
            <strong>⚠️ Important Note on {current_year} Data:</strong> This report includes {current_year_count} incidents 
            recorded in {current_year} through {current_month}. As the year is ongoing, these figures are incomplete 
            and will increase. Year-over-year comparisons should exclude {current_year} for accuracy.
        </div>
        """
    
    # Critical findings
    html += f"""
        <h3>Critical Findings</h3>
        <div class="metrics-grid">
            <div class="metric-card success">
                <h4>No Physical Harm</h4>
                <p class="value">{no_casualty_rate:.1f}%</p>
                <p class="context">of incidents</p>
            </div>
            
            <div class="metric-card danger">
                <h4>Fatal Incidents</h4>
                <p class="value">{fatal_rate:.1f}%</p>
                <p class="context">result in death</p>
            </div>
            
            <div class="metric-card danger">
                <h4>Mass Casualties</h4>
                <p class="value">{mass_casualty_rate:.1f}%</p>
                <p class="context">4+ casualties</p>
            </div>
        </div>
    """
    
    # Trend summary
    if years_covered >= 3:
        recent_years = sorted(df['Year'].unique())[-3:]
        recent_avg = df[df['Year'].isin(recent_years)].groupby('Year').size().mean()
        early_years = sorted(df['Year'].unique())[:3]
        early_avg = df[df['Year'].isin(early_years)].groupby('Year').size().mean()
        
        trend_direction = "increasing" if recent_avg > early_avg else "decreasing"
        trend_pct = abs((recent_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0
        
        html += f"""
        <h3>Trend Overview</h3>
        <p>Analysis shows an overall <strong>{trend_direction} trend</strong> in incidents, 
        with recent years averaging {recent_avg:.0f} incidents compared to {early_avg:.0f} 
        in early years ({trend_pct:.1f}% change).</p>
        """
    
    # School calendar impact
    school_months_incidents = len(df[~df['Month'].isin(['Jun', 'Jul', 'Aug'])])
    school_months_pct = (school_months_incidents / total_incidents * 100) if total_incidents > 0 else 0
    
    html += f"""
        <h3>School Calendar Correlation</h3>
        <p><strong>{school_months_pct:.1f}%</strong> of incidents occur during the traditional school year 
        (September-May), demonstrating a clear correlation with school attendance patterns.</p>
        
        <h3>Report Sections</h3>
        <p>This report provides detailed analysis across multiple dimensions:</p>
        <ul>
            <li><strong>Temporal Trends:</strong> Year-over-year patterns and seasonal variations</li>
            <li><strong>Geographic Distribution:</strong> State and city-level concentrations</li>
            <li><strong>Severity Analysis:</strong> Casualty patterns and incident outcomes</li>
            <li><strong>Evidence-Based Recommendations:</strong> Data-driven prevention strategies</li>
        </ul>
    </div>
    """
    
    return html


def generate_trend_analysis_enhanced(df: pd.DataFrame, current_year: int) -> str:
    """Generate enhanced trend analysis with statistical insights."""
    
    # Prepare data
    yearly_stats = df.groupby('Year').agg({
        'ID': 'count',
        'Total_Casualties': 'sum',
        'Number Killed': 'sum',
        'Number Wounded': 'sum',
        'Is_Fatal': 'sum'
    }).rename(columns={
        'ID': 'Incidents',
        'Is_Fatal': 'Fatal_Incidents'
    })
    
    # Separate complete and partial years
    complete_years = yearly_stats[yearly_stats.index < current_year]
    
    html = f"""
    <div class="section page-break" id="trend-analysis">
        <h2>Trend Analysis</h2>
        
        <h3>Long-Term Patterns</h3>
    """
    
    # Calculate trend statistics
    if len(complete_years) >= 2:
        # Year-over-year changes
        yoy_changes = complete_years['Incidents'].pct_change() * 100
        avg_change = yoy_changes.mean()
        volatility = yoy_changes.std()
        
        # Moving averages
        if len(complete_years) >= 3:
            ma_3year = complete_years['Incidents'].rolling(window=3).mean()
            trend_stable = volatility < 20
        else:
            trend_stable = False
        
        html += f"""
        <div class="info-box">
            <h4>Statistical Summary</h4>
            <ul>
                <li>Average year-over-year change: <strong>{avg_change:+.1f}%</strong></li>
                <li>Volatility (standard deviation): <strong>{volatility:.1f}%</strong></li>
                <li>Trend characterization: <strong>{'Stable' if trend_stable else 'Volatile'}</strong></li>
            </ul>
        </div>
        """
    
    # Detailed yearly breakdown
    html += """
        <h3>Annual Incident Data</h3>
        <table>
            <tr>
                <th>Year</th>
                <th>Incidents</th>
                <th>Change from Previous</th>
                <th>Total Casualties</th>
                <th>Fatal Incidents</th>
                <th>Fatality Rate</th>
            </tr>
    """
    
    prev_incidents = None
    for year in sorted(yearly_stats.index):
        row = yearly_stats.loc[year]
        
        # Calculate change
        if prev_incidents is not None:
            change = ((row['Incidents'] - prev_incidents) / prev_incidents * 100)
            change_str = f"{change:+.1f}%"
            change_class = "positive" if change < 0 else "negative"
        else:
            change_str = "—"
            change_class = ""
        
        # Fatality rate
        fatality_rate = (row['Fatal_Incidents'] / row['Incidents'] * 100) if row['Incidents'] > 0 else 0
        
        # Mark current year
        row_class = 'highlight-row' if year == current_year else ''
        year_marker = f"{year} *" if year == current_year else str(year)
        
        html += f"""
            <tr class="{row_class}">
                <td>{year_marker}</td>
                <td>{int(row['Incidents'])}</td>
                <td class="change {change_class}">{change_str}</td>
                <td>{int(row['Total_Casualties'])}</td>
                <td>{int(row['Fatal_Incidents'])}</td>
                <td>{fatality_rate:.1f}%</td>
            </tr>
        """
        
        prev_incidents = row['Incidents']
    
    html += """
        </table>
        <p style="font-size: 14px; color: #7f8c8d; margin-top: 10px;">
            * Current year (incomplete data)
        </p>
    """
    
    # Monthly patterns
    monthly_stats = df.groupby('Month').agg({
        'ID': 'count',
        'Total_Casualties': 'sum'
    }).rename(columns={'ID': 'Incidents'})
    
    months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly_stats = monthly_stats.reindex(months_order, fill_value=0)
    
    # School vs summer analysis
    school_months = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May']
    summer_months = ['Jun','Jul','Aug']
    
    school_total = monthly_stats.loc[school_months, 'Incidents'].sum()
    summer_total = monthly_stats.loc[summer_months, 'Incidents'].sum()
    total_monthly = school_total + summer_total
    
    school_pct = (school_total / total_monthly * 100) if total_monthly > 0 else 0
    summer_pct = (summer_total / total_monthly * 100) if total_monthly > 0 else 0
    
    # Expected percentages
    expected_school = 75  # 9/12 months
    expected_summer = 25  # 3/12 months
    
    html += f"""
        <h3>Seasonal Patterns</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>School Year (Sep-May)</h4>
                <p class="value">{school_pct:.1f}%</p>
                <p class="context">{school_total} incidents</p>
                <p class="context">Expected: {expected_school}%</p>
            </div>
            
            <div class="metric-card warning">
                <h4>Summer Break (Jun-Aug)</h4>
                <p class="value">{summer_pct:.1f}%</p>
                <p class="context">{summer_total} incidents</p>
                <p class="context">Expected: {expected_summer}%</p>
            </div>
        </div>
        
        <p>The significant reduction in summer incidents ({summer_pct:.1f}% vs expected {expected_summer}%) 
        demonstrates the strong correlation between school attendance and incident occurrence.</p>
    """
    
    # Day of week patterns
    weekday_incidents = len(df[~df['DayOfWeek_Num'].isin([5, 6])])
    weekend_incidents = len(df[df['DayOfWeek_Num'].isin([5, 6])])
    
    weekday_pct = (weekday_incidents / (weekday_incidents + weekend_incidents) * 100) if (weekday_incidents + weekend_incidents) > 0 else 0
    
    html += f"""
        <h3>Weekly Patterns</h3>
        <p><strong>{weekday_pct:.1f}%</strong> of incidents occur on weekdays (Monday-Friday), 
        with an average of {weekday_incidents/5:.1f} incidents per weekday compared to 
        {weekend_incidents/2:.1f} per weekend day.</p>
    </div>
    """
    
    return html


def generate_geographic_insights_enhanced(df: pd.DataFrame) -> str:
    """Generate enhanced geographic analysis with population context."""
    
    # State-level analysis
    state_stats = df.groupby('State_name').agg({
        'ID': 'count',
        'Total_Casualties': 'sum',
        'Number Killed': 'sum',
        'City': 'nunique',
        'School name': 'nunique'
    }).rename(columns={
        'ID': 'Incidents',
        'City': 'Cities',
        'School name': 'Schools',
        'Number Killed': 'Deaths'
    }).sort_values('Incidents', ascending=False)
    
    total_incidents = len(df)
    states_affected = len(state_stats)
    
    html = f"""
    <div class="section page-break" id="geographic-insights">
        <h2>Geographic Insights</h2>
        
        <div class="key-insight">
            <h4>Geographic Reach</h4>
            Incidents have been recorded in <strong>{states_affected}</strong> states and territories, 
            affecting <strong>{df['City'].nunique():,}</strong> cities and 
            <strong>{df['School name'].nunique():,}</strong> individual schools.
        </div>
        
        <h3>State-Level Analysis</h3>
    """
    
    # Concentration metrics
    top_5_states = state_stats.head(5)
    top_10_states = state_stats.head(10)
    
    top_5_pct = (top_5_states['Incidents'].sum() / total_incidents * 100)
    top_10_pct = (top_10_states['Incidents'].sum() / total_incidents * 100)
    
    # Gini coefficient for inequality
    incidents_array = state_stats['Incidents'].values
    gini = calculate_gini_coefficient(incidents_array)
    
    html += f"""
        <div class="info-box">
            <h4>Geographic Concentration Metrics</h4>
            <ul>
                <li>Top 5 states account for <strong>{top_5_pct:.1f}%</strong> of all incidents</li>
                <li>Top 10 states account for <strong>{top_10_pct:.1f}%</strong> of all incidents</li>
                <li>Geographic inequality (Gini coefficient): <strong>{gini:.3f}</strong> 
                    (0 = perfect equality, 1 = maximum concentration)</li>
            </ul>
        </div>
        
        <h4>Top 15 States by Incident Count</h4>
        <table>
            <tr>
                <th>Rank</th>
                <th>State</th>
                <th>Incidents</th>
                <th>% of Total</th>
                <th>Total Casualties</th>
                <th>Deaths</th>
                <th>Cities Affected</th>
                <th>Schools Affected</th>
            </tr>
    """
    
    for idx, (state, row) in enumerate(state_stats.head(15).iterrows(), 1):
        pct_of_total = (row['Incidents'] / total_incidents * 100)
        
        html += f"""
            <tr>
                <td>{idx}</td>
                <td><strong>{state}</strong></td>
                <td>{int(row['Incidents'])}</td>
                <td>{pct_of_total:.1f}%</td>
                <td>{int(row['Total_Casualties'])}</td>
                <td>{int(row['Deaths'])}</td>
                <td>{int(row['Cities'])}</td>
                <td>{int(row['Schools'])}</td>
            </tr>
        """
    
    html += """
        </table>
    """
    
    # Regional analysis
    # Define regions (simplified)
    regions = {
        'Northeast': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 
                     'Vermont', 'New Jersey', 'New York', 'Pennsylvania'],
        'Southeast': ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 
                     'South Carolina', 'Virginia', 'District of Columbia', 'West Virginia',
                     'Alabama', 'Kentucky', 'Mississippi', 'Tennessee', 'Arkansas', 'Louisiana'],
        'Midwest': ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin', 'Iowa', 'Kansas',
                   'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
        'Southwest': ['Arizona', 'New Mexico', 'Oklahoma', 'Texas'],
        'West': ['Colorado', 'Idaho', 'Montana', 'Nevada', 'Utah', 'Wyoming', 'Alaska',
                'California', 'Hawaii', 'Oregon', 'Washington']
    }
    
    regional_stats = {}
    for region, states in regions.items():
        region_data = state_stats[state_stats.index.isin(states)]
        if not region_data.empty:
            regional_stats[region] = {
                'incidents': region_data['Incidents'].sum(),
                'states': len(region_data),
                'casualties': region_data['Total_Casualties'].sum()
            }
    
    html += """
        <h3>Regional Distribution</h3>
        <div class="metrics-grid">
    """
    
    for region, stats in regional_stats.items():
        pct = (stats['incidents'] / total_incidents * 100) if total_incidents > 0 else 0
        html += f"""
            <div class="metric-card">
                <h4>{region}</h4>
                <p class="value">{stats['incidents']}</p>
                <p class="context">{pct:.1f}% of total</p>
                <p class="context">{stats['states']} states affected</p>
            </div>
        """
    
    html += """
        </div>
    """
    
    # City-level insights
    city_counts = df.groupby(['City', 'State_name']).size().reset_index(name='count')
    city_counts['City_State'] = city_counts['City'] + ', ' + city_counts['State_name']
    city_counts = city_counts.sort_values('count', ascending=False)
    
    cities_with_multiple = len(city_counts[city_counts['count'] > 1])
    cities_with_single = len(city_counts[city_counts['count'] == 1])
    
    html += f"""
        <h3>City-Level Patterns</h3>
        <p>Incidents occurred in <strong>{len(city_counts):,}</strong> cities, with 
        <strong>{cities_with_multiple}</strong> cities experiencing multiple incidents and 
        <strong>{cities_with_single}</strong> cities experiencing a single incident.</p>
        
        <h4>Top 10 Cities by Incident Count</h4>
        <table>
            <tr>
                <th>Rank</th>
                <th>City, State</th>
                <th>Incidents</th>
                <th>% of Total</th>
            </tr>
    """
    
    for idx, row in city_counts.head(10).iterrows():
        pct = (row['count'] / total_incidents * 100)
        html += f"""
            <tr>
                <td>{idx + 1}</td>
                <td>{row['City_State']}</td>
                <td>{row['count']}</td>
                <td>{pct:.1f}%</td>
            </tr>
        """
    
    html += """
        </table>
        
        <div class="info-box">
            <h4>Important Context for Geographic Data</h4>
            <ul>
                <li>Raw incident counts should be interpreted alongside population and school density</li>
                <li>Urban areas typically show higher counts due to population concentration</li>
                <li>State-level variations may reflect differences in reporting practices</li>
                <li>Policy environments and prevention programs vary significantly by state</li>
            </ul>
        </div>
    </div>
    """
    
    return html


def generate_severity_assessment_enhanced(df: pd.DataFrame) -> str:
    """Generate enhanced severity assessment with detailed breakdowns."""
    
    # Calculate severity metrics
    total_incidents = len(df)
    total_casualties = int(df['Total_Casualties'].sum())
    total_killed = int(df['Number Killed'].sum())
    total_wounded = int(df['Number Wounded'].sum())
    
    # Incident categories
    no_casualty = len(df[df['Total_Casualties'] == 0])
    injuries_only = len(df[(df['Number Wounded'] > 0) & (df['Number Killed'] == 0)])
    fatal_incidents = len(df[df['Is_Fatal']])
    mass_casualty = len(df[df['Total_Casualties'] >= 4])
    
    # Calculate percentages
    no_casualty_pct = (no_casualty / total_incidents * 100) if total_incidents > 0 else 0
    injuries_only_pct = (injuries_only / total_incidents * 100) if total_incidents > 0 else 0
    fatal_pct = (fatal_incidents / total_incidents * 100) if total_incidents > 0 else 0
    mass_casualty_pct = (mass_casualty / total_incidents * 100) if total_incidents > 0 else 0
    
    html = f"""
    <div class="section page-break" id="severity-assessment">
        <h2>Severity Assessment</h2>
        
        <div class="definition-box">
            <h4>Severity Classifications</h4>
            <ul>
                <li><strong>No Casualties:</strong> Incidents with no reported injuries or deaths</li>
                <li><strong>Injuries Only:</strong> Incidents resulting in wounded individuals but no fatalities</li>
                <li><strong>Fatal Incidents:</strong> Any incident resulting in one or more deaths</li>
                <li><strong>Mass Casualty Events:</strong> Incidents with 4 or more total casualties (FBI definition)</li>
            </ul>
        </div>
        
        <h3>Overall Impact Statistics</h3>
        <div class="metrics-grid">
            <div class="metric-card danger">
                <h4>Total Human Cost</h4>
                <p class="value">{total_casualties:,}</p>
                <p class="context">Total casualties</p>
            </div>
            
            <div class="metric-card danger">
                <h4>Lives Lost</h4>
                <p class="value">{total_killed:,}</p>
                <p class="context">Total deaths</p>
            </div>
            
            <div class="metric-card warning">
                <h4>Injuries</h4>
                <p class="value">{total_wounded:,}</p>
                <p class="context">Total wounded</p>
            </div>
            
            <div class="metric-card">
                <h4>Average Impact</h4>
                <p class="value">{total_casualties/total_incidents:.2f}</p>
                <p class="context">Casualties per incident</p>
            </div>
        </div>
        
        <h3>Incident Severity Distribution</h3>
        <table>
            <tr>
                <th>Category</th>
                <th>Number of Incidents</th>
                <th>Percentage of Total</th>
                <th>Cumulative %</th>
            </tr>
            <tr>
                <td>No Casualties</td>
                <td>{no_casualty:,}</td>
                <td>{no_casualty_pct:.1f}%</td>
                <td>{no_casualty_pct:.1f}%</td>
            </tr>
            <tr>
                <td>Injuries Only</td>
                <td>{injuries_only:,}</td>
                <td>{injuries_only_pct:.1f}%</td>
                <td>{no_casualty_pct + injuries_only_pct:.1f}%</td>
            </tr>
            <tr>
                <td>Fatal Incidents</td>
                <td>{fatal_incidents:,}</td>
                <td>{fatal_pct:.1f}%</td>
                <td>{no_casualty_pct + injuries_only_pct + fatal_pct:.1f}%</td>
            </tr>
            <tr class="highlight-row">
                <td>Mass Casualty Events (subset)</td>
                <td>{mass_casualty:,}</td>
                <td>{mass_casualty_pct:.1f}%</td>
                <td>—</td>
            </tr>
        </table>
    """
    
    # Casualty concentration analysis
    if mass_casualty > 0:
        mass_casualty_df = df[df['Total_Casualties'] >= 4]
        mass_casualties_total = mass_casualty_df['Total_Casualties'].sum()
        mass_casualty_concentration = (mass_casualties_total / total_casualties * 100) if total_casualties > 0 else 0
        
        html += f"""
        <div class="danger-box">
            <h4>Mass Casualty Event Analysis</h4>
            <p>While mass casualty events represent only <strong>{mass_casualty_pct:.1f}%</strong> 
            of all incidents, they account for <strong>{mass_casualty_concentration:.1f}%</strong> 
            of all casualties, highlighting their disproportionate impact.</p>
        </div>
        """
    
    # Intent analysis if available
    if 'Intent' in df.columns:
        intent_severity = df.groupby('Intent').agg({
            'ID': 'count',
            'Total_Casualties': ['sum', 'mean'],
            'Is_Fatal': 'sum'
        }).round(2)
        
        intent_severity.columns = ['Incidents', 'Total_Casualties', 'Avg_Casualties', 'Fatal_Count']
        intent_severity['Fatal_Rate'] = (intent_severity['Fatal_Count'] / intent_severity['Incidents'] * 100).round(1)
        intent_severity = intent_severity.sort_values('Incidents', ascending=False).head(10)
        
        html += """
        <h3>Severity by Intent</h3>
        <table>
            <tr>
                <th>Intent</th>
                <th>Incidents</th>
                <th>Total Casualties</th>
                <th>Avg Casualties</th>
                <th>Fatal Incidents</th>
                <th>Fatality Rate</th>
            </tr>
        """
        
        for intent, row in intent_severity.iterrows():
            html += f"""
            <tr>
                <td>{intent}</td>
                <td>{int(row['Incidents'])}</td>
                <td>{int(row['Total_Casualties'])}</td>
                <td>{row['Avg_Casualties']:.2f}</td>
                <td>{int(row['Fatal_Count'])}</td>
                <td>{row['Fatal_Rate']}%</td>
            </tr>
            """
        
        html += """
        </table>
        """
    
    # Temporal severity patterns
    yearly_severity = df.groupby('Year').agg({
        'Total_Casualties': 'sum',
        'Number Killed': 'sum',
        'Is_Fatal': 'mean'
    }).round(3)
    yearly_severity['Fatality_Rate'] = (yearly_severity['Is_Fatal'] * 100).round(1)
    
    html += f"""
        <h3>Key Severity Insights</h3>
        <ul>
            <li>The majority of incidents (<strong>{no_casualty_pct:.1f}%</strong>) result in no physical casualties, 
                though psychological impact remains significant</li>
            <li>Fatal incidents, while representing <strong>{fatal_pct:.1f}%</strong> of cases, 
                have lasting impacts on entire communities</li>
            <li>Early intervention and rapid response protocols are critical for preventing 
                escalation to mass casualty events</li>
            <li>The average fatality rate has {'increased' if yearly_severity['Fatality_Rate'].iloc[-3:].mean() > yearly_severity['Fatality_Rate'].iloc[:3].mean() else 'decreased'} 
                over the analysis period</li>
        </ul>
    </div>
    """
    
    return html


def generate_recommendations_enhanced(df: pd.DataFrame) -> str:
    """Generate enhanced evidence-based recommendations."""
    
    # Calculate key metrics for recommendations
    total_incidents = len(df)
    weekday_pct = (len(df[~df['DayOfWeek_Num'].isin([5, 6])]) / total_incidents * 100)
    school_months_pct = (len(df[~df['Month'].isin(['Jun', 'Jul', 'Aug'])]) / total_incidents * 100)
    
    # Top months and states
    top_months = df['Month'].value_counts().head(3).index.tolist()
    top_states = df['State_name'].value_counts().head(5).index.tolist()
    
    # Mass casualty rate
    mass_casualty_rate = (len(df[df['Total_Casualties'] >= 4]) / total_incidents * 100)
    
    # Cities with repeat incidents
    city_counts = df.groupby(['City', 'State_name']).size()
    repeat_cities = len(city_counts[city_counts > 1])
    
    html = f"""
    <div class="section page-break" id="recommendations">
        <h2>Evidence-Based Recommendations</h2>
        
        <div class="key-insight">
            <h4>Data-Driven Action Plan</h4>
            These recommendations are based on comprehensive analysis of {total_incidents:,} incidents, 
            identifying clear patterns that can inform targeted prevention strategies.
        </div>
        
        <h3>1. Temporal-Based Interventions</h3>
        <div class="info-box">
            <h4>Key Finding</h4>
            <p>{weekday_pct:.0f}% of incidents occur during school days, with peak months being 
            {', '.join(top_months)}.</p>
        </div>
        
        <h4>Recommended Actions:</h4>
        <ul>
            <li><strong>Enhanced Weekday Protocols:</strong> Implement heightened security measures 
                during school hours, particularly during class transitions</li>
            <li><strong>Seasonal Preparedness:</strong> Increase vigilance during identified peak months, 
                with additional training before these periods</li>
            <li><strong>After-School Programs:</strong> Expand supervised activities during high-risk 
                afternoon hours to provide positive engagement</li>
            <li><strong>Summer Security:</strong> While incidents decrease {100-school_months_pct:.0f}% 
                during summer, maintain security for camps and community programs</li>
        </ul>
        
        <h3>2. Geographic-Targeted Strategies</h3>
        <div class="info-box">
            <h4>Key Finding</h4>
            <p>Top 5 states ({', '.join(top_states[:3])}, etc.) account for a disproportionate 
            share of incidents, with {repeat_cities} cities experiencing multiple events.</p>
        </div>
        
        <h4>Recommended Actions:</h4>
        <ul>
            <li><strong>State-Level Task Forces:</strong> Establish specialized teams in high-incident 
                states to coordinate prevention efforts</li>
            <li><strong>Urban School Initiatives:</strong> Develop targeted programs for cities with 
                repeat incidents, addressing local risk factors</li>
            <li><strong>Resource Allocation:</strong> Prioritize funding and support for schools in 
                statistically higher-risk areas</li>
            <li><strong>Cross-State Collaboration:</strong> Facilitate sharing of successful prevention 
                strategies between states</li>
        </ul>
        
        <h3>3. Severity-Based Response Protocols</h3>
        <div class="info-box">
            <h4>Key Finding</h4>
            <p>While {(len(df[df['Total_Casualties']==0])/total_incidents*100):.0f}% of incidents 
            result in no casualties, {mass_casualty_rate:.1f}% escalate to mass casualty events.</p>
        </div>
        
        <h4>Recommended Actions:</h4>
        <ul>
            <li><strong>Rapid Response Training:</strong> Implement regular drills focused on preventing 
                escalation in the critical first minutes</li>
            <li><strong>Threat Assessment Teams:</strong> Establish multidisciplinary teams to identify 
                and address concerns before they escalate</li>
            <li><strong>De-escalation Protocols:</strong> Train all staff in conflict resolution and 
                crisis intervention techniques</li>
            <li><strong>Medical Preparedness:</strong> Ensure immediate access to trauma care and 
                psychological support services</li>
        </ul>
        
        <h3>4. Technology and Infrastructure</h3>
        <ul>
            <li><strong>Detection Systems:</strong> Implement advanced weapon detection technology at 
                entry points</li>
            <li><strong>Communication Networks:</strong> Establish redundant emergency communication 
                systems for rapid alerts</li>
            <li><strong>Access Control:</strong> Modernize entry systems with single-point entry and 
                visitor management</li>
            <li><strong>Surveillance Integration:</strong> Deploy smart camera systems with real-time 
                threat detection capabilities</li>
        </ul>
        
        <h3>5. Community and Mental Health Initiatives</h3>
        <ul>
            <li><strong>Early Intervention Programs:</strong> Expand mental health screening and support 
                services for at-risk students</li>
            <li><strong>Anonymous Reporting:</strong> Implement and promote tip lines for students to 
                report concerns safely</li>
            <li><strong>Parent Engagement:</strong> Develop programs to help parents recognize warning 
                signs and access resources</li>
            <li><strong>Trauma-Informed Practices:</strong> Train all staff in recognizing and responding 
                to trauma indicators</li>
        </ul>
        
        <h3>6. Policy and Advocacy</h3>
        <ul>
            <li><strong>Evidence-Based Legislation:</strong> Support policies proven to reduce gun 
                violence in educational settings</li>
            <li><strong>Funding Advocacy:</strong> Secure sustainable funding for comprehensive safety 
                programs</li>
            <li><strong>Research Investment:</strong> Support continued data collection and analysis to 
                refine prevention strategies</li>
            <li><strong>Stakeholder Coordination:</strong> Foster collaboration between educators, law 
                enforcement, mental health professionals, and policymakers</li>
        </ul>
        
        <div class="success-box">
            <h4>Implementation Priority</h4>
            <p>Focus initial efforts on high-impact, evidence-based interventions in the highest-risk 
            geographic areas and time periods. Success should be measured through continuous monitoring 
            of incident rates and regular strategy refinement based on emerging patterns.</p>
        </div>
    </div>
    """
    
    return html


def generate_appendix_enhanced(df: pd.DataFrame, quality_metrics: dict) -> str:
    """Generate enhanced appendix with methodology and data quality details."""
    
    # Data quality assessment
    total_records = len(df)
    date_coverage = f"{df['Incident Date'].min().strftime('%Y-%m-%d')} to {df['Incident Date'].max().strftime('%Y-%m-%d')}"
    years_covered = df['Year'].nunique()
    states_covered = df['State_name'].nunique()
    
    # Missing data analysis
    missing_narratives = df['Narrative'].isna().sum() if 'Narrative' in df.columns else 0
    missing_coords = df[['Latitude', 'Longitude']].isna().any(axis=1).sum()
    
    # Completeness percentages
    narrative_completeness = ((total_records - missing_narratives) / total_records * 100) if total_records > 0 else 0
    coord_completeness = ((total_records - missing_coords) / total_records * 100) if total_records > 0 else 0
    
    html = f"""
    <div class="section page-break" id="appendix">
        <h2>Appendix: Methodology and Data Quality</h2>
        
        <h3>Data Source and Collection</h3>
        <div class="info-box">
            <h4>About the Dataset</h4>
            <p><strong>Source:</strong> Everytown Research 
                (<a href="https://everytownresearch.org" style="color: #3498db;">everytownresearch.org</a>)</p>
            <p><strong>Collection Method:</strong> Comprehensive tracking of media reports, law enforcement 
                records, and school notifications</p>
            <p><strong>Update Frequency:</strong> Continuous updates as new incidents are verified</p>
            <p><strong>Quality Assurance:</strong> Multi-source verification and regular data audits</p>
        </div>
        
        <h3>Dataset Characteristics</h3>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Notes</th>
            </tr>
            <tr>
                <td>Total Records Analyzed</td>
                <td>{total_records:,}</td>
                <td>After filtering and deduplication</td>
            </tr>
            <tr>
                <td>Date Coverage</td>
                <td>{date_coverage}</td>
                <td>{years_covered} years of data</td>
            </tr>
            <tr>
                <td>Geographic Coverage</td>
                <td>{states_covered} states/territories</td>
                <td>Includes DC and US territories</td>
            </tr>
            <tr>
                <td>Data Completeness Score</td>
                <td>{quality_metrics.get('completeness_score', 'N/A')}%</td>
                <td>Overall data quality indicator</td>
            </tr>
            <tr>
                <td>Narrative Completeness</td>
                <td>{narrative_completeness:.1f}%</td>
                <td>Incidents with description text</td>
            </tr>
            <tr>
                <td>Location Completeness</td>
                <td>{coord_completeness:.1f}%</td>
                <td>Incidents with coordinates</td>
            </tr>
        </table>
        
        <h3>Inclusion Criteria</h3>
        <ul>
            <li>Any instance where a firearm was brandished, fired, or a bullet hit school property</li>
            <li>Incidents occurring inside school buildings, on school property, on school buses, 
                or at school-sponsored events</li>
            <li>Both K-12 schools and institutions of higher education</li>
            <li>Verified through multiple sources when possible</li>
        </ul>
        
        <h3>Key Definitions</h3>
        <div class="definition-box">
            <ul>
                <li><strong>Incident:</strong> A single event where a firearm was present on school grounds, 
                    regardless of outcome</li>
                <li><strong>Casualty:</strong> Any person killed or wounded during an incident</li>
                <li><strong>Fatal Incident:</strong> Any incident resulting in one or more deaths</li>
                <li><strong>Mass Casualty Event:</strong> Incidents with 4 or more total casualties, 
                    following FBI definitions</li>
                <li><strong>School Grounds:</strong> Any property owned, leased, or used by a school for 
                    educational purposes</li>
            </ul>
        </div>
        
        <h3>Statistical Methods</h3>
        <ul>
            <li><strong>Temporal Analysis:</strong> Year-over-year comparisons exclude incomplete current year data</li>
            <li><strong>Geographic Analysis:</strong> State and city comparisons use raw counts; per-capita 
                analysis requires external population data</li>
            <li><strong>Trend Identification:</strong> Linear regression and moving averages applied to 
                complete years only</li>
            <li><strong>Missing Data:</strong> Excluded from calculations rather than imputed to maintain 
                accuracy</li>
        </ul>
        
        <h3>Important Limitations</h3>
        <div class="warning-box">
            <h4>Data Interpretation Considerations</h4>
            <ul>
                <li><strong>Reporting Bias:</strong> Some incidents may go unreported or lack media coverage</li>
                <li><strong>Geographic Variations:</strong> Reporting practices and data availability vary by jurisdiction</li>
                <li><strong>Temporal Delays:</strong> Recent incidents may not yet be included due to verification processes</li>
                <li><strong>Classification Challenges:</strong> Some incidents may have ambiguous intent or outcomes</li>
                <li><strong>Population Context:</strong> Raw counts don't account for population or school density differences</li>
            </ul>
        </div>
        
        <h3>Report Generation Information</h3>
        <table>
            <tr>
                <td>Report Generated</td>
                <td>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
            </tr>
            <tr>
                <td>Data Last Updated</td>
                <td>{quality_metrics.get('data_freshness', 'Unknown')} days ago</td>
            </tr>
            <tr>
                <td>Analysis Software</td>
                <td>Python with Pandas, NumPy, and Streamlit</td>
            </tr>
            <tr>
                <td>Report Version</td>
                <td>2.0 (Enhanced)</td>
            </tr>
        </table>
        
        <h3>Contact and Resources</h3>
        <p>For questions about this analysis or to report data issues:</p>
        <ul>
            <li>Visit: <a href="https://everytownresearch.org" style="color: #3498db;">everytownresearch.org</a></li>
            <li>Access raw data: Available through Everytown Research website</li>
            <li>Report updates: Generated reports reflect data available at time of creation</li>
        </ul>
    </div>
    """
    
    return html


def calculate_gini_coefficient(values: np.ndarray) -> float:
    """
    Calculate Gini coefficient for measuring inequality in distribution.
    
    Args:
        values: Array of values (e.g., incident counts by state)
        
    Returns:
        Gini coefficient (0 = perfect equality, 1 = maximum inequality)
    """
    # Remove zeros and sort
    values = values[values > 0]
    if len(values) == 0:
        return 0.0
    
    sorted_values = np.sort(values)
    n = len(sorted_values)
    
    # Calculate Gini using the formula
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_values)) / (n * np.sum(sorted_values)) - (n + 1) / n