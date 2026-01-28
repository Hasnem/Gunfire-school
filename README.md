# School Gun Violence Analytics Dashboard

**A Business Intelligence & Analytics Solution for Public Safety Data**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gunfire-school.streamlit.app/)
![Methodology](https://img.shields.io/badge/Methodology-ETL%20%7C%20NLP%20%7C%20Visual%20Analytics-blue?style=flat-square)
![Data Source](https://img.shields.io/badge/Data-Everytown%20Research-green?style=flat-square)

---

## 📌 Problem Statement & Business Context
Gun violence on school grounds is a complex, multi-faceted issue that requires data-driven interventions. Policy makers, school administrators, and safety researchers often struggle to synthesize scattered incident reports into actionable patterns.

**This dashboard solves that data fragmentation problem.** 

It serves as a centralized **Decision Support System (DSS)** that:
1.  **Ingests** raw incident data from public research repositories.
2.  **Validates & Transforms** verifying geospatial coherence and temporal integrity.
3.  **Delivers Insights** through an interactive interface, enabling stakeholders to identify high-risk regions, time-based patterns, and severity trends affecting U.S. schools.

---

## 📊 Analytics Capabilities

### 1. Temporal & Trend Analysis
*Objective: Identify when incidents are most likely to occur to optimize resource allocation.*
-   **Yearly/Monthly Forecasting Views**: Visualizes the rise and fall of incident rates to correlate with policy changes or societal events.
-   **Cyclical Pattern Recognition**: Breakdowns by day-of-week and month to highlight "high-risk" windows (e.g., return to school periods).

### 2. Geospatial Intelligence
*Objective: Pinpoint regional hotspots for targeted intervention.*
-   **State-Level Chloropleths**: Heatmaps identifying states with disproportionate incident rates.
-   **City-Level Granularity**: "Top N" analysis to focus on specific metropolitan areas requiring immediate attention.

### 3. Severity & Classification Matrix
*Objective: Distinguish between minor incidents and mass casualty events for appropriate response planning.*
-   **Casualty Impact Analysis**: Quantifies the human cost (killed vs. wounded).
-   **Intent Classification**: Filters data by incident outcome (accidental, targeted, etc.).

### 4. Automated Executive Reporting
*Objective: Streamline communication with stakeholders.*
-   **Executive Summary Extraction**: Auto-generates high-level insights with "Data Quality Scores" (e.g., *Completeness: 100%*) to validate findings.
-   **Strategic Recommendations**: Delivers actionable advice alongside raw metrics.
-   **Professional Formatting**: Production-ready HTML output with custom CSS for board-level presentations.

**(Placeholder: Insert Screenshot of Report Executive Summary Here)**
*Example of the generated executive report showing data quality indicators and key metrics.*

---

## 🛠️ Data Pipeline & Technical Architecture

This project simulates a production-grade **ETL (Extract, Transform, Load)** pipeline:

### **E**xtract (Data Ingestion)
-   Automated fetching of live CSV data from the **Everytown Research** public repository.
-   Robust error handling for network resilience.

### **T**ransform (Data Engineering)
*Located in `utils/data_loading.py`*
-   **Data Cleaning**: Deduplication logic based on composite keys (Date + City + School) to ensure statistical accuracy.
-   **Geospatial Validation**: Coordinate verification to prevent mapping errors.
-   **Feature Engineering**: 
    -   Deriving "School Year" logic (Aug-July) for academic-relevant trending.
    -   Computing "Days Since Last Incident" to track safety streaks.
    -   Natural Language Processing (NLP) on narrative text to extract unstructured insights.

### **L**oad (Visualization Layer)
-   Optimized loading into **Streamlit's** in-memory cache for sub-second dashboard performance.
-   Serving processed data to **Plotly** for responsive, interactive charting.

---

## 💻 Tech Stack & Skills Demonstrated

| Domain | Technologies |
| :--- | :--- |
| **Orchestration & UI** | Python, Streamlit |
| **Data Engineering** | Pandas, NumPy, Request Handling |
| **Visualization** | Plotly Express, Plotly Graph Objects, Folium |
| **Data Science** | NLTK (Text Mining), Statistical Analysis |

---

## 🚀 Setup & Usage

### Prerequisites
-   Python 3.8+
-   pip

### local Installation
1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/school-gun-violence-dashboard.git
    cd school-gun-violence-dashboard
    ```

2.  **Environment Setup**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Launch Dashboard**
    ```bash
    streamlit run app.py
    ```

---

## 📸 Dashboard Preview

> *Note: Screenshots illustrate the dashboard's capabilities for prospective employers.*

**(Placeholder: Insert Main Dashboard View Here)**
*Real-time interface showing key metric cards and map visualization.*

**(Placeholder: Insert Trend Analysis View Here)**
*Interactive charts allowing users to drill down into specific time periods.*

---

## ⚖️ Disclaimer
*This project is an independent analytics tool developed for educational and portfolio purposes. Data is sourced from [Everytown Research](https://everytownresearch.org/maps/gunfire-on-school-grounds/).*