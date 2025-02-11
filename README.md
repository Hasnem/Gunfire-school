# Gunfire on School Grounds Dashboard

This repository contains a **Streamlit** dashboard that visualizes data on gunfire incidents on school grounds in the United States. The data is fetched directly from [Everytown Research](https://everytownresearch.org/maps/gunfire-on-school-grounds/), which maintains a comprehensive record of such incidents.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Data Source](#data-source)
- [Project Structure](#project-structure)
- [Installation](#installation)

---

## Overview

This dashboard helps users explore trends and statistics about gun-related incidents on school grounds, including:

- **Yearly and monthly trends**: See how incidents have changed over time and across different months.  
- **Intent and outcomes**: Understand the nature (intent) and result (outcome) of these incidents.  
- **Geographic distribution**: View which states and cities are most affected, and explore an interactive density map.  
- **Dynamic Observations**: Bullet-point insights update automatically based on the filtered data.

---

## Features

1. **Interactive Filters**: Filter by State(s), Intent, and Date Range.  
2. **Key Metrics**: Instant overview of victims, incidents, kills, and injuries.  
3. **Latest Incident**: Quick details of the most recent recorded incident.  
4. **Yearly & Monthly Trend Analysis** with advanced reference lines and partial-year warnings.  
5. **Distribution Charts** (Intent, Outcome) + **Intent vs. Outcome Heatmap**.  
6. **Statewise Analysis** (Bar+Line chart + Interactive Density Map).  
7. **Top Cities**: Horizontal bar chart for quick comparison.

---

## Data Source

- **Everytown Research** – [Gunfire on School Grounds](https://everytownresearch.org/maps/gunfire-on-school-grounds/)

---


## Project Structure

- **app.py**: Main Streamlit app file.  
- **helpers.py**: Data loading, preprocessing, plotting, and dynamic observations.  
- **pages.py**: The "About" page content.  
- **requirements.txt** *(optional)*: Dependencies.  
- **README.md**: Project documentation.

## Installation

1. Clone this repository.
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
