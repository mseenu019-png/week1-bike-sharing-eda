# Data Acquisition, Cleaning and Exploratory Data Analysis of Bike Sharing Demand
## A Python-Based Data Preparation and Exploratory Analysis Project

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Dataset](https://img.shields.io/badge/UCI-Bike%20Sharing%20Dataset-orange.svg)](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)

---

## 📖 Executive Project Overview
This repository contains the complete academic and industry-standard **Week 1 Data Science Portfolio Project** focusing on the foundational stages of the Data Science Lifecycle:
### Data Science Workflow

**Data Acquisition**  
↓  
**Data Quality Audit**  
↓  
**Data Cleaning & Validation**  
↓  
**Feature Engineering**  
↓  
**Exploratory Data Analysis**  
↓  
**Statistical Analysis**  
↓  
**Visualization & Insights**  
↓  
**Final Report**

The study investigates urban micromobility patterns and environmental responsiveness using the **UCI Machine Learning Repository Bike Sharing Dataset** (`hour.csv`), capturing **17,379 hourly observation records** from the Capital Bikeshare system in Washington, D.C., across 2011–2012.

---

## 🎯 Project Objectives
1. **Automated Data Acquisition**: Programmatically acquire the official raw UCI archive, validating checksums and preserving raw records untouched.
2. **Comprehensive Data Understanding**: Map schema definitions, dimensional scale ($17,379 \times 17$), feature types, and statistical properties.
3. **Rigorous Data Quality Audit**: Verify zero missing values, zero duplicate entries, schema alignment, and logical range bounds.
4. **Data Validation & Assertions**: Apply 11 domain-specific assertions enforcing physical boundaries and additive constraints ($cnt = casual + registered$).
5. **Feature Engineering**: Derive calendar features (`year`, `month_name`, `day_of_week`, `season_name`, `weather_description`, `hour_group`) and reconstruct un-normalized physical units (°C, %, km/h).
6. **Statistical Analysis**: Calculate parametric (mean, standard deviation, skewness) and non-parametric (median, IQR, percentiles) metrics.
7. **Publication-Grade Visualizations**: Generate 8 high-resolution 300 DPI visualizations exploring demand distributions, diurnal rush-hour dynamics, seasonality, weather effects, and correlation matrices.
8. **Academic Report Production**: Deliver an academic Word document (`.docx`) report complete with embedded charts, formatted tables, and quantified insights.

---

## 📁 Repository Structure
```text
Week1_Bike_Sharing_EDA/
├── data/
│   ├── raw/
│   │   ├── hour.csv                     # Raw, untouched UCI hourly dataset (17,379 rows)
│   │   ├── day.csv                      # Raw daily dataset (reference)
│   │   └── Readme.txt                   # Original UCI dataset documentation
│   └── processed/
│       └── bike_sharing_cleaned.csv     # Cleaned, validated, and feature-engineered dataset
│
├── notebooks/
│   └── Week1_Bike_Sharing_EDA.ipynb     # Fully executed, reproducible Jupyter Notebook
│
├── src/
│   ├── data_acquisition.py              # Phase 1: Automated acquisition and raw archive extraction
│   ├── data_cleaning.py                 # Phases 2-6: Quality audit, validation, cleaning & feature engineering
│   ├── exploratory_analysis.py          # Phases 7, 11, 12: Statistical summaries & insight extraction
│   ├── visualization.py                 # Phase 10: High-resolution (300 DPI) chart generation
│   ├── build_notebook.py                # Programmatic notebook generation script
│   └── generate_docx_report.py          # Phase 17: Academic DOCX report compilation
│
├── visualizations/                      # 300 DPI Publication Visualizations
│   ├── missing_values.png               # Figure 1: Data Completeness & Quality Audit
│   ├── demand_distribution.png          # Figure 2: Hourly Demand Distribution & Skewness
│   ├── hourly_demand.png                # Figure 3: Diurnal Commute Patterns (Work vs Non-Work)
│   ├── monthly_demand.png               # Figure 4: Monthly Seasonality & Year-over-Year Growth
│   ├── seasonal_demand.png              # Figure 5: Seasonal Rental Distribution (Boxplot with Means)
│   ├── weather_demand.png               # Figure 6: Temperature & Weather Severity Impact
│   ├── workingday_demand.png            # Figure 7: User Segmentation (Casual vs Registered)
│   └── correlation_heatmap.png          # Figure 8: Pearson Correlation Matrix Heatmap
│
├── outputs/                             # Tabular & Textual Analytical Outputs
│   ├── summary_statistics.csv           # Parametric and non-parametric summary statistics
│   ├── data_quality_report.csv          # Feature-by-feature quality and transformation matrix
│   └── key_insights.txt                 # Quantified evidence-based findings
│
├── report/
│   └── Week1_Bike_Sharing_EDA_Report.docx # Complete Academic Project Report (Word Document)
│
├── requirements.txt                     # Project dependencies
└── README.md                            # Comprehensive project documentation
```

---

## ⚙️ Installation & Quickstart

### 1. Clone or Open the Repository
```bash
cd "Week1_Bike_Sharing_EDA"
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Complete Pipeline End-to-End
You can run the modular Python scripts sequentially:
```bash
# Step 1: Download and extract raw UCI dataset
python src/data_acquisition.py

# Step 2: Perform data quality audit, validation, and feature engineering
python src/data_cleaning.py

# Step 3: Compute summary statistics, aggregations, and insights
python src/exploratory_analysis.py

# Step 4: Generate all 8 high-resolution visualizations
python src/visualization.py

# Step 5: Build and execute the interactive Jupyter Notebook
python src/build_notebook.py
python -m nbconvert --to notebook --execute notebooks/Week1_Bike_Sharing_EDA.ipynb --inplace

# Step 6: Compile the academic DOCX report
python src/generate_docx_report.py
```

---

## 📊 Summary of Key Empirical Findings

| # | Domain Finding | Quantitative Metric / Evidence | Strategic Takeaway |
|---|----------------|--------------------------------|-------------------|
| **1** | **Fleet Volume & Backbone** | 3,292,679 total rides; **81.17%** registered subscribers vs. **18.83%** casual | Registered commuters form the predictable baseline revenue. |
| **2** | **Adoption Growth** | **+64.88%** year-over-year surge (1.24M in 2011 $\rightarrow$ 2.05M in 2012) | Demonstrates rapid municipal transit network maturation. |
| **3** | **Diurnal Commute Rhythm** | Dual peaks at **08:00** (368.6/hr) and **17:00** (461.5/hr); low at **04:00** (6.4/hr) | Direct driver of morning/evening dock rebalancing demands. |
| **4** | **Day-Type Segmentation** | Weekdays: 86.7% registered; Weekends: Casual demand doubles to **57.4/hr** | Distinct weekday commuter vs weekend recreational schedules. |
| **5** | **Seasonal Trajectory** | Peak in Fall (**236.0/hr**) and Summer (**208.4/hr**); lowest in Spring (**111.1/hr**) | Winter/early spring cold depresses usage by over 50%. |
| **6** | **Monthly Expansion** | June/Sept peak (**~241/hr**) vs. January trough (**94.4/hr**) | 2.55x seasonal variance requires dynamic winter fleet maintenance. |
| **7** | **Thermal Catalyst** | Temperature Pearson correlation **$r = +0.404$** ($r = +0.401$ for feeling temp) | Ambient temperature is the primary positive environmental driver. |
| **8** | **Adverse Weather Deterrence** | Humidity $r = -0.323$; rain/snow reduces demand by **62.4%** (to 111.6/hr) | Extreme precipitation halts recreational trips almost entirely. |

---

## 📈 Visualizations Overview

1. **Figure 1: Missing Values Audit (`visualizations/missing_values.png`)**: Confirms 100.0% completeness across all 17 attributes.
2. **Figure 2: Demand Distribution (`visualizations/demand_distribution.png`)**: Visualizes right-skewed (+1.19) distribution with mean (189.5) and median (142.0) markers.
3. **Figure 3: Hourly Commute Dynamics (`visualizations/hourly_demand.png`)**: Compares bimodal working-day commuter peaks against unimodal weekend leisure curves.
4. **Figure 4: Monthly Demand Growth (`visualizations/monthly_demand.png`)**: Quantifies month-by-month ridership and +64.88% annual system expansion.
5. **Figure 5: Seasonal Distribution (`visualizations/seasonal_demand.png`)**: Boxplot comparing quartile spreads and red mean indicators across Spring, Summer, Fall, Winter.
6. **Figure 6: Weather & Temperature Impact (`visualizations/weather_demand.png`)**: Scatter plot and regression trendline segmenting ridership by weather condition categories.
7. **Figure 7: User-Type Segmentation (`visualizations/workingday_demand.png`)**: Grouped bar chart decomposing casual, registered, and total demand across day types.
8. **Figure 8: Correlation Matrix Heatmap (`visualizations/correlation_heatmap.png`)**: Pearson correlation matrix of environmental variables and user demand tiers.

---

## 🔬 Limitations & Future Work

### Limitations
- **Geographic Boundary**: Constrained to Washington, D.C. (Capital Bikeshare).
- **Temporal Epoch**: 2011–2012 data precedes modern dockless e-bike deployments.
- **Descriptive Nature**: Correlation reflects empirical association rather than causation.
- **Spatial Aggregation**: Lacks station-level GPS telemetry and route elevation profiles.

### Future Scope
- **Supervised Regression Modeling**: XGBoost, LightGBM, Random Forest for hourly demand prediction.
- **Time-Series Forecasting**: SARIMAX and Prophet models for multi-horizon planning.
- **Fleet Rebalancing Optimization**: Mixed-integer linear programming (MILP) for truck dispatching.

---

## 📚 Dataset References & Citation
- **Primary Source**: UCI Machine Learning Repository — [Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)
- **DOI**: [10.24432/C5W894](https://doi.org/10.24432/C5W894)
- **Paper**: Fanaee-T, H., & Gama, J. (2014). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence, 2(2), 113-127.
