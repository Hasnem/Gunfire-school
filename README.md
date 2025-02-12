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
   - All charts and metrics update instantly to reflect your filter selections.

2. **Dynamic Metrics**  
   - At-a-glance figures for total incidents, casualties, killed, and wounded.  
   - Quickly gauge the scope of impact based on chosen filters.

3. **Latest Incident Highlights**  
   - A concise summary pinpoints the most recent recorded incident in the sidebar.

4. **Trend Analysis**  
   - **Yearly Trends**: Track how incident counts and casualties shift over time.  
   - **Monthly Trends**: Identify potential seasonal or academic factors.

5. **Distribution & Heatmap**  
   - **Bar Charts**: Reveal the breakdown of outcomes (killed vs. wounded) and intent.  
   - **Heatmap**: Visualize the intersection of intent vs. outcome.

6. **Geographic Visualization**  
   - **Statewise Bar Chart**: Compare incident counts across states.  
   - **US Map**: Choose between a bubble scatter map or a choropleth to see incident hotspots.

7. **Top Cities & Tragic Incidents**  
   - Identify which cities have the highest reported incidents.
   - A quick rundown of the most tragic incidents for deeper context.

---

## Data Source & Scope

- **Primary Data Source**:  
  [Everytown Research – Gunfire on School Grounds](https://everytownresearch.org/maps/gunfire-on-school-grounds/)  
  The data includes incident date, location, intent, and casualties, updated by Everytown on a rolling basis.

- **Scope & Limitations**:  
  - Data may be **partial** for recent years (e.g., 2025) as incidents might be newly reported or under investigation.  
  - **Geographic coordinates** can be missing or approximate for select records.  
  - Reflects **reported incidents** only; actual events may be underreported.

---

## Project Structure


- **app.py**  
  Main Streamlit application. Configures the layout, sidebar, and selects between the **Dashboard** and **About** page.
- **about_page.py**  
  A simple page that provides additional background or context about the project.
- **utils/**  
  - **data_loading.py**: Functions to fetch and preprocess the dataset.  
  - **data_filters.py**: Sidebar-based filtering logic.  
  - **utils_common.py**: Common functions, such as displaying headers or metric cards.  
  - **charts.py**: Various Plotly chart functions.  
  - **observations.py**: Dynamically generated text or insights based on the filtered data.

---