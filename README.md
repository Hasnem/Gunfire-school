# School Gun Violence Dashboard

A comprehensive data analysis dashboard tracking gun-related incidents on school grounds across the United States. Built with Streamlit and powered by data from [Everytown Research](https://everytownresearch.org/maps/gunfire-on-school-grounds/).

**🔗 [Live Dashboard](https://gunfire-school.streamlit.app/)**

## Overview

This dashboard transforms raw incident data into actionable insights, helping policymakers, educators, researchers, and communities understand patterns and trends in school gun violence to inform prevention strategies.

## Features

### 📊 Real-Time Data Analysis
- Automatically fetches and processes the latest incident data
- Interactive filters by time period, location, and severity
- Dynamic visualizations that update based on selections

### 📈 Comprehensive Analytics
- **Temporal Trends**: Yearly, monthly, and weekly patterns
- **Geographic Insights**: State and city-level analysis with heat maps
- **Severity Assessment**: Casualty statistics and incident classifications
- **Narrative Analysis**: Text mining of incident descriptions

### 📑 Reporting Capabilities
- Generate executive reports in HTML format
- Export filtered data for further analysis
- Print-friendly layouts for presentations

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/school-gun-violence-dashboard.git
cd school-gun-violence-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## Project Structure

```
├── app.py                 # Main application entry point
├── about_page.py         # About page content
├── requirements.txt      # Python dependencies
├── utils/
│   ├── charts.py         # Visualization functions
│   ├── data_filters.py   # Data filtering logic
│   ├── data_loading.py   # Data fetching and preprocessing
│   ├── executive_report.py # Report generation
│   ├── narrative_analysis.py # Text analysis
│   ├── observations.py   # Insight generation
│   └── utils_common.py   # Shared utilities
└── README.md
```

## Usage Guide

### 1. Filtering Data
Use the sidebar to filter by:
- **Time Period**: Date ranges or specific years
- **Location**: Individual states or top N states
- **Severity**: All incidents, casualties only, or fatal incidents

### 2. Exploring Tabs
- **Trends**: Analyze patterns over time
- **Geography**: Explore spatial distributions
- **Severity**: Understand incident impacts
- **Narratives**: Extract insights from descriptions

### 3. Generating Reports
Click "Executive Report" in the navigation to create comprehensive PDF summaries with your selected data.

## Data Source

This dashboard uses publicly available data from [Everytown Research](https://everytownresearch.org/maps/gunfire-on-school-grounds/), which tracks incidents where a firearm was brandished, fired, or a bullet hit school property.

### Data Includes:
- Incident date and location
- School information
- Casualty counts
- Intent and outcome classifications
- Narrative descriptions

### Important Notes:
- Current year data is incomplete and continuously updated
- Some records may have missing geographic or narrative information
- Data reflects reported incidents only

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation
- **[Plotly](https://plotly.com/)**: Interactive visualizations
- **[NLTK](https://www.nltk.org/)**: Natural language processing
- **[WordCloud](https://github.com/amueller/word_cloud)**: Text visualization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Data Source**: [Everytown Research](https://everytownresearch.org/) for maintaining comprehensive incident data
- **Community**: All contributors and users working toward safer schools

## Contact

For questions, suggestions, or collaborations, please open an issue on GitHub.

---

**Disclaimer**: This is an independent analysis tool. For the most current information and research, please visit [Everytown Research](https://everytownresearch.org/).