# Google Fiber Customer Service Analytics

## 🎯 Objective
To provide Google Fiber customer support leadership with data-driven visibility into repeat customer call patterns and first-contact resolution effectiveness, enabling targeted service improvements and reduced call volumes.

## 📁 Repository Structure

google-fiber-analytics/

├── business-planning/

│   ├── Google-Fiber_project-requirements.docx

│   ├── Google-Fiber_stakeholder-requirements.docx

│   └── Google-Fiber_strategy-document.docx

├── Data preparation/

│   ├── Google-Fiber_Preprocessing_Analytics.py

│   ├── Google-Fiber_Analysis.sql

│   ├── Google-Fiber.csv

│   ├── fcr_by_issue_type.csv

|   ├── fcr_by_market.csv

|   └── fcr_overall_metrics.csv

├── Google-Fiber-Customer-Service.pbix

└── README.md


## 📓 Notebooks Overview
**1. Data Cleaning & Preparation**
- Handled missing values in contact sequence data

- Unpivoted contact columns for analysis

- Created temporal features from date stamps

- Standardized categorical variables (issue types, markets)

**2. Exploratory Data Analysis**
- Statistical summary of key metrics

- Distribution analysis of contact patterns

- Correlation analysis between variables

- Initial identification of trends and outliers

**3. Repeat Caller Analysis**
- FCR rate calculations by multiple definitions

- Repeat caller segmentation and profiling

- Escalation pattern identification

- Root cause analysis for repeat contacts

**4. Feature Engineering**
- Created smart metrics for dashboard optimization

- Developed aggregated summary tables

- Built time intelligence features

- Prepared data for Power BI consumption

## 📊 Power BI Dashboard Overview

<img width="1422" height="792" alt="image" src="https://github.com/user-attachments/assets/c9e4a88f-ec57-4839-bfc2-a2b598e8791e" />
<img width="1417" height="792" alt="image" src="https://github.com/user-attachments/assets/b8d04114-5624-49bf-b804-abf6415c296e" />

## 🔍 Key Insights

**Critical Findings**
1. **Extremely Low FCR Rate**: Only 7.63% of cases resolved on first contact

2. **High Repeat Rate**: 81.19% of cases require multiple contacts

3. **Market Concentration**: 68% of cases from market_3

4. **Issue Type Prevalence**: Type_5 represents majority of cases and repeat calls

**Performance Patterns**
1. **Market_2**: Highest repeat call rate (~70%)

2. **Market_3**: Highest volume (68% of cases) with 60% repeat rate

3. **Type_5 Issues**: Most prevalent and highest repeat contact driver

4. **Type_4 Issues**: Highest escalation probability despite lower volume

## 🎯 Recommendations

**Immediate Actions**
1. **Prioritize Type_5 Resolution**: Address root causes of most common issue type

2. **Market_3 Intervention**: Deploy additional resources to highest-volume market

3. **FCR Training**: Implement specialized first-contact resolution training

**Strategic Initiatives**
1. **Root Cause Analysis**: Investigate why Type_5 issues generate disproportionate repeats

2. **Process Optimization**: Streamline resolution pathways for common issue types

3. **Preventative Measures**: Develop solutions to reduce Type_2 and Type_5 occurrences

**Monitoring Framework**
1. **Weekly FTR Tracking**: Implement strict first-time resolution monitoring

2. **Market-Specific Goals**: Set differentiated performance targets

3. **Issue-Type KPIs**: Establish improvement targets for each problem category


## 🛠️ Tech Stack
**Data Processing & Analysis**
- Python 3.8+: Primary analysis language

- Pandas: Data manipulation and cleaning

- NumPy: Numerical computations

- Matplotlib/Seaborn: Data visualization

- Jupyter Notebooks: Interactive analysis

**Business Intelligence**
- Power BI: Dashboard development and deployment

- DAX: Advanced measures and calculations

- Power Query: Data transformation and modeling

**Data Management**
- CSV: Data storage and exchange format

- Git: Version control and collaboration

- Windows OS: Development environment

