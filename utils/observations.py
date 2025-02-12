import pandas as pd

def generate_yearly_trend_observations(df: pd.DataFrame) -> str:
    # (same as before or improved)
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
    if 2025 in yearly_counts.index:
        notes.append(
            "<div><b style='font-size:80%; color:#f44336;'>Partial Data Disclaimer:</b> "
            "<span style='font-size:70%;'>Some 2025 incidents may not yet be reported.</span></div>"
        )

    if {2019, 2020, 2021}.issubset(yearly_counts.index):
        avg_around = (yearly_counts.loc[2019] + yearly_counts.loc[2021]) / 2
        if avg_around and yearly_counts.loc[2020] < (avg_around * 0.8):
            notes.append(
                "<div><b style='font-size:80%; color:#f44336;'>Pandemic Impact:</b> "
                "<span style='font-size:70%;'>A noticeable dip in 2020 may reflect school closures or underreporting.</span></div>"
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
        Rising trends may indicate worsening circumstances or better reporting, 
        while decreases might reflect interventions or external factors.
    </p>
    """
    return html_obs

def generate_monthly_trend_observations(df: pd.DataFrame) -> str:
    # (same as before)
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
                {top_month} logged {top_count} incidents, possibly reflecting school schedules or local events.
            </span>
        </li>
        <li><b style="font-size: 80%; color: #f44336;">Lowest Activity:</b>
            <span style="font-size:70%;">
                {bottom_month} had {bottom_count} incidents, which could coincide with breaks or seasonal slowdowns.
            </span>
        </li>
        <li><b style="font-size: 80%; color: #f44336;">Total Records Analyzed:</b>
            <span style="font-size:70%;">{total_incidents} incidents across all months.</span>
        </li>
    </ul>
    """
    return html_obs

def generate_distribution_observations(df: pd.DataFrame) -> str:
    # (same as before)
    if df.empty:
        return "<p><em>No distribution data available to reflect upon.</em></p>"

    intent_counts = df['Intent'].value_counts()
    outcome_counts = df['Outcome'].value_counts()

    intent_line = ""
    if not intent_counts.empty:
        top_intent = intent_counts.idxmax()
        intent_pct = (intent_counts[top_intent] / intent_counts.sum() * 100)
        intent_line = (
            f"<li><b style='font-size:80%; color:#f44336;'>Most Common Intent:</b> "
            f"<span style='font-size:70%;'>{top_intent}</span> (~{intent_pct:.1f}% of all cases)</li>"
        )

    outcome_line = ""
    if not outcome_counts.empty:
        top_outcome = outcome_counts.idxmax()
        outcome_pct = (outcome_counts[top_outcome] / outcome_counts.sum() * 100)
        outcome_line = (
            f"<li><b style='font-size:80%; color:#f44336;'>Most Common Outcome:</b> "
            f"<span style='font-size:70%;'>{top_outcome}</span> (~{outcome_pct:.1f}% of outcomes)</li>"
        )

    if not intent_line and not outcome_line:
        return "<p><em>No distribution observations can be drawn.</em></p>"

    html_obs = f"""
    <p style="font-size: 90%;"><b>Distribution Insights: Intent & Outcome</b></p>
    <ul style="font-size: 90%;">
        {intent_line}
        {outcome_line}
    </ul>
    """
    return html_obs

def generate_heatmap_observations(df: pd.DataFrame) -> str:
    # (same as before)
    if df.empty:
        return "<p><em>No data available to extract heatmap insights.</em></p>"

    pivot_table = pd.pivot_table(df, values='ID', index='Intent', columns='Outcome', aggfunc='count').fillna(0)
    if pivot_table.empty:
        return "<p><em>No valid data found in the heatmap.</em></p>"

    melted = pivot_table.reset_index().melt(id_vars='Intent', var_name='Outcome', value_name='Count')
    melted.sort_values(by='Count', ascending=False, inplace=True)
    if melted.empty or melted['Count'].max() == 0:
        return "<p><em>No significant patterns to report in the heatmap.</em></p>"

    top_combo = melted.iloc[0]
    html_obs = f"""
    <p style="font-size: 90%;"><b>Heatmap Interpretation: Intent vs. Outcome</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size:80%; color:#f44336;">Dominant Pattern:</b>
            <span style="font-size:70%;">
                Intent: <i>{top_combo['Intent']}</i> and Outcome: <i>{top_combo['Outcome']}</i> 
                appear most frequently with {int(top_combo['Count'])} incidents.
            </span>
        </li>
    </ul>
    """
    return html_obs

def generate_day_of_week_observations(df: pd.DataFrame) -> str:
    """
    Observations about the day-of-week chart, explaining possible weekday vs. weekend patterns.
    """
    if df.empty:
        return "<p><em>No data available for day-of-week observations.</em></p>"

    # We can highlight the busiest or quietest day
    df['Total_Casualties'] = df['Number Killed'] + df['Number Wounded']
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # For a quick snippet, let's get the top day for incidents
    incidents_by_day = df.groupby("DayOfWeek").size()
    incidents_by_day = incidents_by_day.reindex(day_order, fill_value=0)
    top_day_inc = incidents_by_day.idxmax()
    top_val_inc = incidents_by_day.max()

    # Similarly for casualties
    casualties_by_day = df.groupby("DayOfWeek")["Total_Casualties"].sum().reindex(day_order, fill_value=0)
    top_day_cas = casualties_by_day.idxmax()
    top_val_cas = casualties_by_day.max()

    html_obs = f"""
    <p style="font-size: 90%;"><b>Day-of-Week Observations:</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size:80%; color:#f44336;">Highest Incident Day:</b>
            <span style="font-size:70%;">
                {top_day_inc} stands out with {top_val_inc} recorded incidents.
            </span>
        </li>
        <li><b style="font-size:80%; color:#f44336;">Most Casualties Day:</b>
            <span style="font-size:70%;">
                {top_day_cas} reports the highest total casualties at {top_val_cas}.
            </span>
        </li>
    </ul>
    <p style="font-size:90%;">
        Weekday vs. weekend differences can help highlight when campuses might need 
        heightened safety measures or if after-school activities play a role.
    </p>
    """
    return html_obs

def generate_statewise_observations(df: pd.DataFrame) -> str:
    # (same as before)
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
                ~{top3_pct:.1f}% of all incidents.
            </span>
        </li>
        <li><b style="font-size:80%; color:#f44336;">Highest Concentration:</b>
            <span style="font-size:70%;">
                {top_state} alone contributes ~{top_state_pct:.1f}% ({top_state_count} incidents).
            </span>
        </li>
    </ul>
    """
    return html_obs

def generate_top_cities_observations(df: pd.DataFrame) -> str:
    # (same as before)
    if df.empty:
        return "<p><em>No data available on top cities.</em></p>"

    city_counts = df['City'].value_counts()
    if city_counts.empty:
        return "<p><em>No city data to report.</em></p>"

    top_city = city_counts.index[0]
    top_city_count = city_counts.iloc[0]
    next_cities = city_counts.index[1:4]
    next_cities_str = ", ".join(next_cities) if len(next_cities) > 0 else "None listed"

    html_obs = f"""
    <p style="font-size: 90%;"><b>City-Level Observations:</b></p>
    <ul style="font-size: 90%;">
        <li><b style="font-size:80%; color:#f44336;">Highest Incidence City:</b>
            <span style="font-size:70%;">{top_city} leads with {top_city_count} recorded incidents.</span>
        </li>
        <li><b style="font-size:80%; color:#f44336;">Other Noteworthy Hubs:</b>
            <span style="font-size:70%;">{next_cities_str}</span>
        </li>
    </ul>
    """
    return html_obs

def generate_top_tragic_incidents_observation(df: pd.DataFrame) -> str:
    if df.empty:
        return "<p><em>No data available to reflect upon top tragic incidents.</em></p>"
    html_obs = f"""
    <p style="font-size:90%;">
        The table above highlights incidents with the highest total casualties, offering 
        a stark look at events that had particularly severe outcomes. Examining these cases 
        may reveal shared risk factors—like campus size, location type, or response times—
        guiding targeted policies or practices to help prevent future tragedies.
    </p>
    """
    return html_obs

def generate_choropleth_observations(df: pd.DataFrame) -> str:
    if df.empty:
        return "<p><em>No data to display in choropleth observation.</em></p>"

    state_counts = df['State_name'].value_counts()
    if state_counts.empty:
        return "<p><em>No data to reflect upon in choropleth view.</em></p>"

    top_state = state_counts.index[0]
    top_val = state_counts.iloc[0]
    html_obs = f"""
    <p style="font-size:90%;"><b>Choropleth Insights:</b></p>
    <p style="font-size:90%;">
        This map colors each state by the total number of incidents, with deeper hues
        indicating higher counts. For instance, <b style="color:#f44336;">{top_state}</b>
        has the highest count at <b>{top_val}</b> incidents. Hover over a state for its
        specific data or compare patterns across regions. 
    </p>
    """
    return html_obs
