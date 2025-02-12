# Gunfire on School Grounds Dashboard

This repository contains a **Streamlit** dashboard for analyzing gunfire incidents on school grounds in the United States. It automatically fetches data from [Everytown Research](https://everytownresearch.org/maps/gunfire-on-school-grounds/) to give users real-time insights into the frequency, geographic spread, and outcomes of these tragic events.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Data Source & Scope](#data-source--scope)
- [Project Structure](#project-structure)
---

## Overview

Gun-related violence on school grounds is a critical issue that affects students, educators, and communities. This dashboard aims to:
- Present **yearly and monthly trends** to illustrate how incidents have evolved over time.
- Provide **interactive filtering** for deeper insights into specific states, time frames, or types of incidents (intent).
- Highlight **key metrics**, including total incidents, lives lost, and injuries.
- Offer **visual context** via maps and charts, illuminating where and how these incidents occur most frequently.

By converting raw data into easily interpretable visuals, this project aspires to inform researchers, policymakers, educators, and the general public, guiding meaningful conversations and potential preventative measures.

---

## Key Features

1. **Interactive Filters**  
   - Select specific states, adjust date ranges, and filter by intent type.  
   - All charts and metrics update on the fly to reflect the filtered dataset.

2. **Dynamic Metrics**  
   - At-a-glance figures for total victims, incidents, killed, and injured.  
   - Quickly gauge the scope of impact under your chosen filters.

3. **Latest Incident Highlights**  
   - A concise summary in the sidebar that pinpoints the most recent recorded incident.

4. **Trend Analysis**  
   - **Yearly Trends**: Track how incident counts and casualties change over time.  
   - **Monthly Trends**: Identify seasonal peaks or slow periods and explore possible contributing factors (e.g., holidays or academic schedules).

5. **Distribution & Heatmap**  
   - **Bar Charts**: Reveal the breakdown of Intent and Outcome across incidents.  
   - **Intent vs. Outcome Heatmap**: Spot the most frequent combinations of motives and results, guiding discussions on risk factors.

6. **Geographic Visualization**  
   - **Statewise Overview**: A dual-axis bar+line chart highlights incident counts and cumulative impact.  
   - **Interactive US Map**: Pinpoint hotspots and compare geographic densities.

7. **Top Cities**  
   - A quick glance at which cities have the highest reported incidents, aiding localized policy or research.

---

## Data Source & Scope

- **Primary Data Source**:  
  [Everytown Research – Gunfire on School Grounds](https://everytownresearch.org/maps/gunfire-on-school-grounds/)  
  Everytown updates this dataset regularly, capturing details such as date, location, intent, and casualties.

- **Scope & Limitations**:  
  - Data may be **partial** for recent years (e.g., 2025) as incidents may still be under investigation or unreported.  
  - **Geographic coordinates** may be missing or approximate for certain records.  
  - The data reflects **reported incidents** only and may not include every event that goes unreported or undiscovered.  

---

## Project Structure

1. **app.py**: Orchestrates the Streamlit dashboard, including the layout, page config, and overall UI flow.  
2. **helpers.py**: Contains functions for data fetching, cleaning, chart creation, and dynamic text observations.  
3. **pages.py**: Offers additional narrative and background context for the dashboard, displayed under an “About” tab.

---