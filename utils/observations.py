import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from typing import Optional, Dict, List

def generate_yearly_trend_observations(df: pd.DataFrame) -> None:
    """
    Generate insightful observations about yearly trends with proper context.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No data available for yearly trend analysis.</em></p>"
            "</div>"
        )
        return

    # Calculate yearly statistics
    yearly_counts = df.groupby('Year').size().sort_index()
    if yearly_counts.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No valid yearly data found.</em></p>"
            "</div>"
        )
        return

    # Key metrics
    current_year = datetime.now().year
    current_month = datetime.now().strftime('%B')
    earliest_year = int(yearly_counts.index.min())
    latest_year = int(yearly_counts.index.max())
    total_years = latest_year - earliest_year + 1
    
    # Check for current year partial data
    is_current_year_partial = (latest_year == current_year)
    
    # Get complete years for accurate analysis
    complete_years = yearly_counts[yearly_counts.index < current_year]
    
    # Build observation HTML
    html_obs = '<div class="observation-section">'
    html_obs += '<h4>📊 What the Yearly Data Shows</h4>'
    
    # 1. Data completeness warning
    if is_current_year_partial:
        current_count = int(yearly_counts.loc[latest_year])
        html_obs += f'''
        <div class="warning-box">
            <strong>⚠️ Important:</strong> {latest_year} shows {current_count} incidents through {current_month}. 
            This number will increase as the year progresses. Year-over-year comparisons should exclude {latest_year}.
        </div>
        '''
    
    # 2. Overall time span
    html_obs += f'''
    <p><strong>📅 Data Coverage:</strong> {total_years} years ({earliest_year} to {latest_year})</p>
    '''
    
    # 3. Recent trend analysis (using complete years only)
    if len(complete_years) >= 2:
        recent_year = complete_years.index[-1]
        prev_year = complete_years.index[-2]
        recent_count = int(complete_years.loc[recent_year])
        prev_count = int(complete_years.loc[prev_year])
        
        if prev_count > 0:
            change_pct = ((recent_count - prev_count) / prev_count * 100)
            direction = "increased" if change_pct > 0 else "decreased"
            arrow = "↑" if change_pct > 0 else "↓"
            color = "#e74c3c" if change_pct > 0 else "#27ae60"
            
            html_obs += f'''
            <div class="metric-insight">
                <strong>Recent Change:</strong> 
                <span style="color: {color}; font-weight: bold;">
                    {arrow} {abs(change_pct):.1f}%
                </span>
                from {prev_year} ({prev_count} incidents) to {recent_year} ({recent_count} incidents)
            </div>
            '''
    
    # 4. Long-term trend
    if len(complete_years) >= 5:
        # Compare first 3 years to last 3 years
        early_period = complete_years.iloc[:3]
        recent_period = complete_years.iloc[-3:]
        early_avg = early_period.mean()
        recent_avg = recent_period.mean()
        
        long_term_change = ((recent_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0
        
        if abs(long_term_change) > 10:
            trend = "upward" if long_term_change > 0 else "downward"
            html_obs += f'''
            <div class="trend-insight">
                <strong>Long-term Pattern:</strong> The data shows an overall <strong>{trend} trend</strong> 
                when comparing early years (avg: {early_avg:.0f}) to recent years (avg: {recent_avg:.0f}).
            </div>
            '''
        else:
            html_obs += '''
            <div class="trend-insight">
                <strong>Long-term Pattern:</strong> Incident rates have remained <strong>relatively stable</strong> 
                over the observation period.
            </div>
            '''
    
    # 5. Peak year identification
    if len(complete_years) > 0:
        peak_year = int(complete_years.idxmax())
        peak_count = int(complete_years.max())
        years_since_peak = latest_year - peak_year
        
        html_obs += f'''
        <div class="peak-insight">
            <strong>Historical Peak:</strong> {peak_year} with {peak_count} incidents
            {f"({years_since_peak} years ago)" if years_since_peak > 0 else "(most recent complete year)"}
        </div>
        '''
    
    # 6. Volatility insight
    if len(complete_years) >= 3:
        volatility = complete_years.std() / complete_years.mean() * 100
        if volatility > 30:
            html_obs += '''
            <p><strong>⚡ Volatility:</strong> Year-to-year incident counts show 
            <strong>high variability</strong>, suggesting multiple factors influence occurrence rates.</p>
            '''
        elif volatility < 15:
            html_obs += '''
            <p><strong>📈 Consistency:</strong> Year-to-year incident counts are 
            <strong>relatively consistent</strong>, showing limited variation.</p>
            '''
    
    html_obs += '</div>'
    st.html(html_obs)


def generate_monthly_trend_observations(df: pd.DataFrame) -> None:
    """
    Generate clear observations about monthly patterns and school calendar impact.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No data available for monthly analysis.</em></p>"
            "</div>"
        )
        return

    # Calculate monthly statistics
    monthly_counts = df['Month'].value_counts()
    if monthly_counts.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No monthly patterns found.</em></p>"
            "</div>"
        )
        return

    # Define month order
    months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly_ordered = monthly_counts.reindex(months_order, fill_value=0)
    
    # Key statistics
    peak_month = monthly_ordered.idxmax()
    peak_count = monthly_ordered.max()
    lowest_month = monthly_ordered.idxmin()
    lowest_count = monthly_ordered.min()
    
    # School calendar groupings
    academic_months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
    summer_months = ['Jun', 'Jul', 'Aug']
    
    # Calculate school vs summer statistics
    academic_total = sum(monthly_ordered[month] for month in academic_months)
    summer_total = sum(monthly_ordered[month] for month in summer_months)
    total_incidents = monthly_ordered.sum()
    
    academic_pct = (academic_total / total_incidents * 100) if total_incidents > 0 else 0
    summer_pct = (summer_total / total_incidents * 100) if total_incidents > 0 else 0
    
    # Calculate expected percentages (9 months vs 3 months)
    expected_academic_pct = 75  # 9/12 months
    expected_summer_pct = 25    # 3/12 months
    
    # Build observations
    html_obs = '''
    <div class="observation-section">
        <h4>📅 Monthly Patterns & School Schedule Impact</h4>
    '''
    
    # 1. School calendar correlation
    html_obs += f'''
    <div class="calendar-insight">
        <strong>🏫 School Calendar Effect:</strong>
        <ul>
            <li>Academic months (Sep-May): <strong>{academic_total}</strong> incidents 
                ({academic_pct:.1f}% of total)</li>
            <li>Summer break (Jun-Aug): <strong>{summer_total}</strong> incidents 
                ({summer_pct:.1f}% of total)</li>
        </ul>
    '''
    
    # Interpretation of the pattern
    if summer_pct < expected_summer_pct - 5:
        reduction_pct = ((expected_summer_pct - summer_pct) / expected_summer_pct * 100)
        html_obs += f'''
        <p class="insight-highlight">
        💡 Summer incidents are <strong>{reduction_pct:.0f}% lower</strong> than expected, 
        demonstrating a clear correlation with school attendance.
        </p>
        '''
    
    html_obs += '</div>'
    
    # 2. Peak and low months
    html_obs += f'''
    <div class="peak-low-insight">
        <strong>📊 Monthly Extremes:</strong>
        <ul>
            <li>Highest: <strong>{peak_month}</strong> with {peak_count} incidents</li>
            <li>Lowest: <strong>{lowest_month}</strong> with {lowest_count} incidents</li>
            <li>Range: {peak_count - lowest_count} incidents 
                ({((peak_count - lowest_count) / peak_count * 100):.0f}% variation)</li>
        </ul>
    </div>
    '''
    
    # 3. Seasonal patterns
    # Calculate quarterly averages
    spring_avg = monthly_ordered[['Mar', 'Apr', 'May']].mean()
    summer_avg = monthly_ordered[['Jun', 'Jul', 'Aug']].mean()
    fall_avg = monthly_ordered[['Sep', 'Oct', 'Nov']].mean()
    winter_avg = monthly_ordered[['Dec', 'Jan', 'Feb']].mean()
    
    seasons = [
        ('Spring', spring_avg, '🌸'),
        ('Summer', summer_avg, '☀️'),
        ('Fall', fall_avg, '🍂'),
        ('Winter', winter_avg, '❄️')
    ]
    seasons_sorted = sorted(seasons, key=lambda x: x[1], reverse=True)
    
    html_obs += '''
    <div class="seasonal-insight">
        <strong>🌍 Seasonal Averages:</strong>
        <ol>
    '''
    
    for season, avg, emoji in seasons_sorted:
        html_obs += f'<li>{emoji} {season}: {avg:.1f} incidents/month</li>'
    
    html_obs += '''
        </ol>
    </div>
    '''
    
    # 4. Additional insights
    if peak_month in ['Sep', 'Oct']:
        html_obs += '''
        <p class="timing-insight">
        📌 The peak in early fall coincides with the start of the school year, 
        when security protocols may still be adjusting.
        </p>
        '''
    elif peak_month in ['Apr', 'May']:
        html_obs += '''
        <p class="timing-insight">
        📌 The peak in late spring may relate to end-of-year tensions and 
        approaching transitions.
        </p>
        '''
    
    html_obs += '</div>'
    st.html(html_obs)


def generate_day_of_week_observations(df: pd.DataFrame) -> None:
    """
    Generate insights about weekly patterns and school schedule correlation.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No data available for day-of-week analysis.</em></p>"
            "</div>"
        )
        return

    # Calculate day statistics
    day_counts = df['DayOfWeek'].value_counts()
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_counts_ordered = day_counts.reindex(day_order, fill_value=0)
    
    # Calculate weekday vs weekend
    weekday_total = sum(day_counts_ordered[day] for day in ["Mon", "Tue", "Wed", "Thu", "Fri"])
    weekend_total = sum(day_counts_ordered[day] for day in ["Sat", "Sun"])
    total = weekday_total + weekend_total
    
    if total == 0:
        st.html(
            "<div class='observation-section'>"
            "<p><em>Insufficient data for day-of-week analysis.</em></p>"
            "</div>"
        )
        return
    
    weekday_pct = (weekday_total / total * 100)
    weekend_pct = (weekend_total / total * 100)
    
    # Per-day averages
    weekday_avg = weekday_total / 5  # 5 weekdays
    weekend_avg = weekend_total / 2  # 2 weekend days
    
    # Build observations
    html_obs = '''
    <div class="observation-section">
        <h4>📆 Weekly Pattern Analysis</h4>
    '''
    
    # 1. Overall distribution
    html_obs += f'''
    <div class="weekday-weekend-split">
        <strong>🏫 School Days vs Weekends:</strong>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
            <div class="stat-box" style="background: #e8f4f8; padding: 1rem; border-radius: 0.5rem;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #2c3e50;">
                    {weekday_pct:.1f}%
                </div>
                <div style="color: #7f8c8d;">Weekdays (Mon-Fri)</div>
                <div style="color: #3498db; margin-top: 0.5rem;">
                    {weekday_avg:.1f} incidents/day
                </div>
            </div>
            <div class="stat-box" style="background: #fef5e7; padding: 1rem; border-radius: 0.5rem;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #2c3e50;">
                    {weekend_pct:.1f}%
                </div>
                <div style="color: #7f8c8d;">Weekends (Sat-Sun)</div>
                <div style="color: #f39c12; margin-top: 0.5rem;">
                    {weekend_avg:.1f} incidents/day
                </div>
            </div>
        </div>
    </div>
    '''
    
    # 2. Risk ratio
    if weekend_avg > 0:
        risk_ratio = weekday_avg / weekend_avg
        html_obs += f'''
        <div class="risk-insight">
            <strong>⚖️ Relative Risk:</strong> Weekdays have 
            <span style="color: #e74c3c; font-weight: bold;">{risk_ratio:.1f}x higher</span> 
            incident rate per day compared to weekends.
        </div>
        '''
    
    # 3. Peak day analysis
    peak_day = day_counts_ordered.idxmax()
    peak_count = day_counts_ordered.max()
    lowest_day = day_counts_ordered.idxmin()
    lowest_count = day_counts_ordered.min()
    
    html_obs += f'''
    <div class="daily-pattern">
        <strong>📊 Daily Breakdown:</strong>
        <ul>
            <li>Highest risk: <strong>{peak_day}</strong> ({peak_count} incidents)</li>
            <li>Lowest risk: <strong>{lowest_day}</strong> ({lowest_count} incidents)</li>
    '''
    
    # Specific day insights
    if peak_day == "Mon":
        html_obs += '''
            <li>📌 Monday peak may reflect weekend tensions carrying over or 
                adjustment stress after breaks</li>
        '''
    elif peak_day == "Fri":
        html_obs += '''
            <li>📌 Friday peak might indicate end-of-week tensions or 
                reduced supervision</li>
        '''
    elif peak_day in ["Tue", "Wed", "Thu"]:
        html_obs += '''
            <li>📌 Mid-week peak suggests incidents aren't limited to 
                transition periods</li>
        '''
    
    html_obs += '''
        </ul>
    </div>
    '''
    
    # 4. Weekend patterns
    if weekend_total > 0:
        sat_count = day_counts_ordered.get('Sat', 0)
        sun_count = day_counts_ordered.get('Sun', 0)
        
        html_obs += f'''
        <div class="weekend-detail">
            <strong>🏃 Weekend Activity:</strong> Despite schools being closed, 
            {weekend_total} incidents ({weekend_pct:.1f}%) still occur on weekends, 
            often related to:
            <ul>
                <li>Sports events and extracurricular activities</li>
                <li>Community use of school facilities</li>
                <li>Off-hours incidents on school property</li>
            </ul>
        </div>
        '''
    
    html_obs += '</div>'
    st.html(html_obs)


def generate_distribution_observations(df: pd.DataFrame) -> None:
    """
    Generate observations about incident severity and characteristics.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No data available for distribution analysis.</em></p>"
            "</div>"
        )
        return

    html_obs = '<div class="observation-section">'
    html_obs += '<h4>⚠️ Understanding Incident Severity</h4>'
    
    # 1. Severity analysis
    if 'Severity' in df.columns:
        severity_counts = df['Severity'].value_counts()
        total_incidents = len(df)
        
        # Calculate key percentages
        no_casualty_count = severity_counts.get('No Casualties', 0)
        no_casualty_pct = (no_casualty_count / total_incidents * 100) if total_incidents > 0 else 0
        
        fatal_categories = ['Single Fatality', 'Multiple Casualties', 'Mass Casualty']
        fatal_count = sum(severity_counts.get(cat, 0) for cat in fatal_categories)
        fatal_pct = (fatal_count / total_incidents * 100) if total_incidents > 0 else 0
        
        mass_casualty_count = severity_counts.get('Mass Casualty', 0)
        mass_casualty_pct = (mass_casualty_count / total_incidents * 100) if total_incidents > 0 else 0
        
        html_obs += f'''
        <div class="severity-overview">
            <strong>📊 Severity Breakdown:</strong>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0;">
                <div style="text-align: center; padding: 1rem; background: #eafaf1; border-radius: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold; color: #27ae60;">
                        {no_casualty_pct:.1f}%
                    </div>
                    <div style="color: #27ae60; font-weight: 600;">No Casualties</div>
                    <div style="font-size: 0.875rem; color: #7f8c8d;">
                        {no_casualty_count} incidents
                    </div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #fadbd8; border-radius: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;">
                        {fatal_pct:.1f}%
                    </div>
                    <div style="color: #e74c3c; font-weight: 600;">Fatal</div>
                    <div style="font-size: 0.875rem; color: #7f8c8d;">
                        {fatal_count} incidents
                    </div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8d7da; border-radius: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold; color: #8b0000;">
                        {mass_casualty_pct:.1f}%
                    </div>
                    <div style="color: #8b0000; font-weight: 600;">Mass Casualty</div>
                    <div style="font-size: 0.875rem; color: #7f8c8d;">
                        {mass_casualty_count} incidents
                    </div>
                </div>
            </div>
        </div>
        '''
        
        # Key insight about severity
        html_obs += f'''
        <div class="severity-insight">
            <strong>💡 Key Finding:</strong> While the majority of incidents 
            ({no_casualty_pct:.1f}%) result in no physical casualties, every incident 
            represents a serious safety breach requiring immediate attention and response.
        </div>
        '''
    
    # 2. Intent analysis
    if 'Intent' in df.columns:
        intent_counts = df['Intent'].value_counts()
        if not intent_counts.empty:
            top_3_intents = intent_counts.head(3)
            
            html_obs += '''
            <div class="intent-analysis">
                <strong>🎯 Common Intent Patterns:</strong>
                <ol style="margin: 0.5rem 0;">
            '''
            
            for intent, count in top_3_intents.items():
                pct = (count / total_incidents * 100)
                html_obs += f'''
                <li><strong>{intent}:</strong> {count} incidents ({pct:.1f}%)</li>
                '''
            
            html_obs += '''
                </ol>
                <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                    Understanding intent patterns helps target prevention strategies 
                    to address root causes.
                </p>
            </div>
            '''
    
    # 3. Casualty statistics
    if 'Total_Casualties' in df.columns:
        total_casualties = df['Total_Casualties'].sum()
        avg_casualties_when_present = df[df['Total_Casualties'] > 0]['Total_Casualties'].mean()
        
        if total_casualties > 0:
            html_obs += f'''
            <div class="casualty-stats">
                <strong>📈 Casualty Statistics:</strong>
                <ul>
                    <li>Total casualties across all incidents: <strong>{int(total_casualties)}</strong></li>
                    <li>When casualties occur, average per incident: 
                        <strong>{avg_casualties_when_present:.1f}</strong></li>
                </ul>
            </div>
            '''
    
    html_obs += '</div>'
    st.html(html_obs)


def generate_heatmap_observations(df: pd.DataFrame) -> None:
    """
    Generate insights from intent vs outcome patterns.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty or 'Intent' not in df.columns or 'Outcome' not in df.columns:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No data available for intent-outcome analysis.</em></p>"
            "</div>"
        )
        return

    # Create pivot table for analysis
    pivot_table = pd.pivot_table(
        df, 
        values='ID', 
        index='Intent', 
        columns='Outcome', 
        aggfunc='count'
    ).fillna(0)
    
    if pivot_table.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>Insufficient data for pattern analysis.</em></p>"
            "</div>"
        )
        return

    html_obs = '''
    <div class="observation-section">
        <h4>🔍 Intent vs Outcome Patterns</h4>
        
        <p>This analysis reveals how different incident intents correlate with 
        outcomes, helping identify which situations are most likely to escalate.</p>
    '''
    
    # Find strongest correlations
    melted = pivot_table.reset_index().melt(
        id_vars='Intent', 
        var_name='Outcome', 
        value_name='Count'
    )
    melted = melted[melted['Count'] > 0].sort_values('Count', ascending=False)
    
    if not melted.empty:
        # Top patterns
        top_patterns = melted.head(5)
        total_in_top = top_patterns['Count'].sum()
        total_overall = melted['Count'].sum()
        concentration_pct = (total_in_top / total_overall * 100) if total_overall > 0 else 0
        
        html_obs += f'''
        <div class="pattern-concentration">
            <strong>📊 Pattern Concentration:</strong> The top 5 intent-outcome 
            combinations account for <strong>{concentration_pct:.1f}%</strong> of 
            all incidents, indicating predictable patterns.
        </div>
        
        <div class="top-patterns">
            <strong>🔝 Most Common Patterns:</strong>
            <ol style="margin: 0.5rem 0;">
        '''
        
        for idx, row in top_patterns.iterrows():
            pct = (row['Count'] / total_overall * 100)
            html_obs += f'''
            <li>
                <strong>{row["Intent"]}</strong> → {row["Outcome"]} 
                <span style="color: #7f8c8d;">
                    ({int(row["Count"])} incidents, {pct:.1f}%)
                </span>
            </li>
            '''
        
        html_obs += '''
            </ol>
        </div>
        '''
        
        # Risk insights
        if 'Fatal' in str(melted['Outcome'].values) or 'Death' in str(melted['Outcome'].values):
            fatal_intents = melted[melted['Outcome'].str.contains('Fatal|Death', case=False, na=False)]
            if not fatal_intents.empty:
                top_fatal_intent = fatal_intents.iloc[0]['Intent']
                html_obs += f'''
                <div class="risk-alert">
                    <strong>⚠️ High-Risk Pattern:</strong> Incidents with intent 
                    "<strong>{top_fatal_intent}</strong>" show the highest correlation 
                    with fatal outcomes, requiring immediate intervention protocols.
                </div>
                '''
    
    html_obs += '''
        <p style="margin-top: 1rem; font-size: 0.9rem; color: #7f8c8d;">
            💡 <em>Understanding these patterns helps schools and law enforcement 
            develop targeted response protocols for different incident types.</em>
        </p>
    </div>
    '''
    
    st.html(html_obs)


def generate_statewise_observations(df: pd.DataFrame) -> None:
    """
    Generate geographic insights with context about concentration and spread.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No state data available.</em></p>"
            "</div>"
        )
        return

    # Calculate state statistics
    state_counts = df['State_name'].value_counts()
    total_incidents = len(df)
    states_affected = len(state_counts)
    total_possible_states = 50  # Continental US states
    
    html_obs = '''
    <div class="observation-section">
        <h4>📍 Geographic Distribution Insights</h4>
    '''
    
    # 1. Coverage statistics
    coverage_pct = (states_affected / total_possible_states * 100)
    html_obs += f'''
    <div class="coverage-stat">
        <strong>🗺️ Geographic Reach:</strong> Incidents have been recorded in 
        <strong>{states_affected} states</strong> ({coverage_pct:.0f}% of the US), 
        demonstrating this is a nationwide concern.
    </div>
    '''
    
    # 2. Concentration analysis
    top_5_states = state_counts.head(5)
    top_5_total = top_5_states.sum()
    top_5_pct = (top_5_total / total_incidents * 100) if total_incidents > 0 else 0
    
    # Calculate if this follows Pareto principle
    top_20_pct_states = int(states_affected * 0.2)
    top_20_pct_total = state_counts.head(top_20_pct_states).sum()
    top_20_pct_incidents = (top_20_pct_total / total_incidents * 100) if total_incidents > 0 else 0
    
    html_obs += f'''
    <div class="concentration-analysis">
        <strong>📊 Geographic Concentration:</strong>
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;">
            <div style="margin-bottom: 0.5rem;">
                Top 5 states account for <strong>{top_5_pct:.1f}%</strong> of all incidents:
            </div>
            <ol style="margin: 0.5rem 0 0.5rem 1.5rem;">
    '''
    
    for state, count in top_5_states.items():
        state_pct = (count / total_incidents * 100)
        html_obs += f'''
        <li>{state}: <strong>{count}</strong> incidents ({state_pct:.1f}%)</li>
        '''
    
    html_obs += f'''
            </ol>
            <div style="margin-top: 0.5rem; color: #7f8c8d; font-size: 0.9rem;">
                📐 The top 20% of states ({top_20_pct_states}) contain {top_20_pct_incidents:.1f}% 
                of incidents, {"closely following" if 70 <= top_20_pct_incidents <= 85 else "deviating from"} 
                the Pareto principle.
            </div>
        </div>
    </div>
    '''
    
    # 3. Per capita insight (if population data were available)
    html_obs += '''
    <div class="context-note">
        <strong>📝 Important Context:</strong> Raw incident counts should be 
        interpreted alongside:
        <ul style="margin: 0.5rem 0;">
            <li>State population sizes</li>
            <li>Number of schools per state</li>
            <li>Reporting practices and data collection methods</li>
            <li>State-specific policies and interventions</li>
        </ul>
    </div>
    '''
    
    # 4. Regional patterns (if identifiable)
    if len(top_5_states) >= 3:
        # Simple regional grouping
        south_states = ['Texas', 'Florida', 'Georgia', 'North Carolina', 'Virginia']
        west_states = ['California', 'Arizona', 'Colorado', 'Washington', 'Oregon']
        midwest_states = ['Illinois', 'Ohio', 'Michigan', 'Indiana', 'Wisconsin']
        northeast_states = ['New York', 'Pennsylvania', 'Massachusetts', 'New Jersey', 'Connecticut']
        
        regions_represented = []
        if any(state in south_states for state in top_5_states.index):
            regions_represented.append("South")
        if any(state in west_states for state in top_5_states.index):
            regions_represented.append("West")
        if any(state in midwest_states for state in top_5_states.index):
            regions_represented.append("Midwest")
        if any(state in northeast_states for state in top_5_states.index):
            regions_represented.append("Northeast")
        
        if len(regions_represented) >= 3:
            html_obs += '''
            <p><strong>🌎 Regional Distribution:</strong> The top states span multiple 
            regions, confirming this is not a regionally isolated issue.</p>
            '''
    
    html_obs += '</div>'
    st.html(html_obs)


def generate_top_cities_observations(df: pd.DataFrame) -> None:
    """
    Generate insights about city-level incident patterns.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No city data available.</em></p>"
            "</div>"
        )
        return

    # Calculate city statistics
    city_counts = df.groupby(['City', 'State_name']).size().reset_index(name='count')
    city_counts['City_State'] = city_counts['City'] + ', ' + city_counts['State_name']
    city_counts = city_counts.sort_values('count', ascending=False)
    
    total_cities = len(city_counts)
    total_incidents = city_counts['count'].sum()
    
    html_obs = '''
    <div class="observation-section">
        <h4>🏙️ City-Level Analysis</h4>
    '''
    
    if len(city_counts) > 0:
        # 1. Top city information
        top_city = city_counts.iloc[0]
        top_city_pct = (top_city['count'] / total_incidents * 100) if total_incidents > 0 else 0
        
        html_obs += f'''
        <div class="top-city-stat">
            <strong>📍 Highest Concentration:</strong> {top_city["City_State"]} 
            leads with <strong>{top_city["count"]} incidents</strong> 
            ({top_city_pct:.1f}% of total).
        </div>
        '''
        
        # 2. Distribution pattern
        single_incident_cities = len(city_counts[city_counts['count'] == 1])
        multiple_incident_cities = len(city_counts[city_counts['count'] > 1])
        repeat_incident_pct = (multiple_incident_cities / total_cities * 100) if total_cities > 0 else 0
        
        html_obs += f'''
        <div class="distribution-pattern">
            <strong>📊 Distribution Pattern:</strong>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 0.5rem 0;">
                <div style="background: #e8f8f5; padding: 1rem; border-radius: 0.5rem;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #27ae60;">
                        {single_incident_cities}
                    </div>
                    <div style="color: #7f8c8d;">Cities with single incident</div>
                </div>
                <div style="background: #fef5e7; padding: 1rem; border-radius: 0.5rem;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #f39c12;">
                        {multiple_incident_cities}
                    </div>
                    <div style="color: #7f8c8d;">Cities with multiple incidents</div>
                </div>
            </div>
        </div>
        '''
        
        # 3. Concentration insight
        top_10_cities = city_counts.head(10)
        top_10_total = top_10_cities['count'].sum()
        top_10_pct = (top_10_total / total_incidents * 100) if total_incidents > 0 else 0
        
        html_obs += f'''
        <div class="concentration-insight">
            <strong>🎯 Urban Concentration:</strong> The top 10 cities account for 
            <strong>{top_10_pct:.1f}%</strong> of all incidents, while representing 
            less than 1% of all affected cities ({total_cities} total).
        </div>
        '''
        
        # 4. Pattern implications
        if repeat_incident_pct > 20:
            html_obs += '''
            <div class="pattern-implication">
                <strong>💡 Key Finding:</strong> With {repeat_incident_pct:.0f}% of 
                cities experiencing multiple incidents, targeted interventions in 
                high-frequency locations could significantly reduce overall numbers.
            </div>
            '''.format(repeat_incident_pct=repeat_incident_pct)
        else:
            html_obs += '''
            <div class="pattern-implication">
                <strong>💡 Key Finding:</strong> The wide geographic spread with most 
                cities experiencing single incidents suggests the need for broad-based 
                prevention strategies rather than location-specific interventions.
            </div>
            '''
    
    html_obs += '</div>'
    st.html(html_obs)


def generate_top_tragic_incidents_observation(df: pd.DataFrame) -> None:
    """
    Generate sensitive observations about severe incidents with focus on prevention.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No data available for severity analysis.</em></p>"
            "</div>"
        )
        return
    
    html_obs = '''
    <div class="observation-section">
        <h4>🔴 Understanding High-Impact Incidents</h4>
        
        <div class="context-box">
            <strong>📋 Context:</strong> This analysis examines the most severe incidents 
            to identify patterns that can inform prevention and response strategies. 
            Each data point represents a tragedy that impacted communities deeply.
        </div>
    '''
    
    if 'Total_Casualties' in df.columns:
        # Calculate severity statistics
        mass_casualties = df[df['Total_Casualties'] >= 4]
        mass_count = len(mass_casualties)
        total_incidents = len(df)
        
        if mass_count > 0:
            mass_pct = (mass_count / total_incidents * 100)
            
            # Calculate casualty concentration
            total_casualties_all = df['Total_Casualties'].sum()
            total_casualties_mass = mass_casualties['Total_Casualties'].sum()
            casualty_concentration = (total_casualties_mass / total_casualties_all * 100) if total_casualties_all > 0 else 0
            
            # Time pattern for mass casualties
            if 'Year' in mass_casualties.columns:
                years_with_mass = mass_casualties['Year'].nunique()
                total_years = df['Year'].nunique()
                
            html_obs += f'''
            <div class="severity-statistics">
                <strong>📊 Mass Casualty Events (4+ casualties):</strong>
                <ul style="margin: 0.5rem 0;">
                    <li><strong>{mass_count}</strong> incidents 
                        ({mass_pct:.1f}% of all incidents)</li>
                    <li>Account for <strong>{casualty_concentration:.1f}%</strong> 
                        of all casualties despite being rare</li>
                    <li>Occurred in <strong>{years_with_mass}</strong> of 
                        {total_years} years analyzed</li>
                </ul>
            </div>
            '''
            
            # Prevention focus
            html_obs += '''
            <div class="prevention-focus">
                <strong>🛡️ Prevention Implications:</strong>
                <p>The concentration of casualties in a small percentage of incidents 
                suggests that:</p>
                <ul style="margin: 0.5rem 0;">
                    <li>Early intervention and threat assessment are critical</li>
                    <li>Rapid response protocols can significantly reduce casualties</li>
                    <li>Most incidents can be prevented from escalating to mass casualty events</li>
                </ul>
            </div>
            '''
            
            # Response time insight
            avg_casualties_regular = df[df['Total_Casualties'] < 4]['Total_Casualties'].mean()
            avg_casualties_mass = mass_casualties['Total_Casualties'].mean()
            
            if avg_casualties_regular > 0:
                escalation_factor = avg_casualties_mass / avg_casualties_regular
                html_obs += f'''
                <div class="escalation-insight">
                    <strong>⏱️ Escalation Factor:</strong> Mass casualty events result in 
                    <strong>{escalation_factor:.0f}x more casualties</strong> on average, 
                    emphasizing the critical importance of rapid response and intervention.
                </div>
                '''
        else:
            html_obs += '''
            <div class="positive-note">
                <strong>✅ Positive Finding:</strong> No mass casualty events 
                (4+ casualties) found in the current data selection. However, 
                continued vigilance and prevention efforts remain essential.
            </div>
            '''
    
    html_obs += '''
        <div class="closing-note">
            <p style="margin-top: 1rem; padding: 0.75rem; background: #e8f4f8; 
                      border-radius: 0.5rem; font-size: 0.9rem;">
                💙 <em>Every incident, regardless of severity, represents an opportunity 
                to learn and improve our prevention and response strategies. The goal 
                is zero incidents through comprehensive, evidence-based interventions.</em>
            </p>
        </div>
    </div>
    '''
    
    st.html(html_obs)


def generate_choropleth_observations(df: pd.DataFrame) -> None:
    """
    Generate insights about the geographic visualization.
    
    Args:
        df: Filtered dataframe with incident data
    """
    if df.empty:
        st.html(
            "<div class='observation-section'>"
            "<p><em>No geographic data available.</em></p>"
            "</div>"
        )
        return

    html_obs = '''
    <div class="observation-section">
        <h4>🗺️ Reading the Geographic Heat Map</h4>
        
        <div class="map-guide">
            <strong>📖 How to Interpret This Map:</strong>
            <ul style="margin: 0.5rem 0;">
                <li><strong>Color Intensity:</strong> Darker shades indicate higher 
                    incident counts</li>
                <li><strong>White/Light Areas:</strong> States with few or no 
                    recorded incidents</li>
                <li><strong>Interactive:</strong> Hover over any state for detailed 
                    statistics</li>
            </ul>
        </div>
        
        <div class="interpretation-note">
            <strong>⚠️ Important Considerations:</strong>
            <p>When interpreting geographic patterns, consider that incident counts 
            are influenced by:</p>
            <ul style="margin: 0.5rem 0;">
                <li><strong>Population density:</strong> More populated states naturally 
                    have more schools and potential incidents</li>
                <li><strong>Reporting practices:</strong> Some states may have more 
                    comprehensive reporting systems</li>
                <li><strong>Policy differences:</strong> State-level gun laws and school 
                    safety policies vary significantly</li>
                <li><strong>Data collection:</strong> Variations in how incidents are 
                    tracked and reported across jurisdictions</li>
            </ul>
        </div>
        
        <div class="action-prompt">
            <strong>💡 For Deeper Analysis:</strong> Compare states with similar 
            populations or school counts to identify meaningful differences in 
            incident rates and successful prevention strategies.
        </div>
    </div>
    '''
    
    st.html(html_obs)


# CSS styling for observation sections
def get_observation_styles():
    """Return comprehensive CSS styles for observation sections."""
    return """
    <style>
    /* Main observation container */
    .observation-section {
        background-color: #f8f9fa;
        border-left: 4px solid #4a5568;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .observation-section h4 {
        color: #2d3748;
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Different box types */
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-left: 4px solid #f39c12;
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 0.25rem;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 0.25rem;
    }
    
    .context-box {
        background-color: #e8f4f8;
        border: 1px solid #3498db;
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 0.25rem;
    }
    
    /* Insight highlights */
    .metric-insight, .trend-insight, .peak-insight {
        background-color: white;
        padding: 0.75rem;
        margin: 0.75rem 0;
        border-radius: 0.25rem;
        border: 1px solid #e2e8f0;
    }
    
    .insight-highlight {
        background-color: #fffbeb;
        padding: 0.75rem;
        margin: 0.75rem 0;
        border-radius: 0.25rem;
        border-left: 3px solid #f59e0b;
    }
    
    /* Lists and structure */
    .observation-section ul, .observation-section ol {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .observation-section li {
        margin: 0.35rem 0;
    }
    
    .observation-section p {
        margin: 0.75rem 0;
    }
    
    /* Stat boxes */
    .stat-box {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        transition: transform 0.2s;
    }
    
    .stat-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Strong emphasis */
    .observation-section strong {
        color: #2d3748;
        font-weight: 600;
    }
    
    /* Links */
    .observation-section a {
        color: #3498db;
        text-decoration: none;
    }
    
    .observation-section a:hover {
        text-decoration: underline;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .observation-section {
            padding: 1rem;
            font-size: 0.9rem;
        }
        
        .observation-section h4 {
            font-size: 1.1rem;
        }
    }
    </style>
    """