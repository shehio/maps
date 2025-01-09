# NYC CitiBikes Data Analysis

A comprehensive data analysis project for NYC CitiBikes trip data, featuring interactive visualizations and detailed analytics.

## Features

- **Interactive Visualizations**: Dynamic charts and maps showing bike usage patterns
- **Usage Analytics**: Detailed analysis of trip durations, station popularity, and user demographics
- **Geographic Insights**: Heat maps and route analysis for bike movement patterns
- **Time-based Analysis**: Peak usage times and seasonal trends
- **User Demographics**: Analysis of user types and subscription patterns

## Installation
1. Clone the repository:
```bash
git clone https://github.com/shehio/maps.git
```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the data:
   - Place the NYC CitiBikes trip data CSV file in the `data` directory
   - The data file should be named `JC-202501-citibike-tripdata.csv`

## Usage

1. Run the main analysis script:
   ```bash
   python src/main.py
   ```

2. View the generated visualizations in the `output` directory:
   - `output/station_heatmap.html`: Interactive map of station usage
   - `output/trip_duration_distribution.html`: Distribution of trip durations
   - `output/peak_usage_times.html`: Peak usage times analysis
   - `output/user_demographics.html`: User type distribution

## Project Structure

```
nyc-citibikes-analysis/
├── data/                      # Data files
│   └── JC-202501-citibike-tripdata.csv
├── output/                    # Generated visualizations
│   ├── station_heatmap.html
│   ├── trip_duration_distribution.html
│   ├── peak_usage_times.html
│   └── user_demographics.html
├── src/                       # Source code
│   ├── analyzers/            # Analysis modules
│   │   ├── base.py
│   │   ├── station_analyzer.py
│   │   ├── trip_analyzer.py
│   │   └── user_analyzer.py
│   ├── visualizers/          # Visualization modules
│   │   ├── base.py
│   │   ├── heatmap.py
│   │   ├── histogram.py
│   │   └── pie_chart.py
│   └── main.py              # Main script
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 