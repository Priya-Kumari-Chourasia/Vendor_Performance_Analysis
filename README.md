# Vendor-Performance-Analysis-Python-Powerbi

This report outlines the Vendor Performance Analysis project, detailing the automated integration of multiple SQL data sources, the execution of exploratory data analysis and vendor classification in Python, and the creation of interactive dashboards in Power BI to support procurement and vendor management decisions

## 📌 Objective

To automate and streamline the process of analyzing vendor data by:
- Integrating data from various relational tables
- Conducting exploratory data analysis (EDA) for deeper understanding
- Classifying vendors based on defined business logic
- Creating a visual Power BI dashboard to enable prompt decision-making

  ## 🛠️ Tools & Technologies

- **Python 3.x** – Utilized for automating data extraction, cleaning, and transformation
- **Pandas** – Data manipulation, aggregation, and analysis 
- **SQLite3** – Querying relational data tables
- **Power BI** – Interactive data visualization  
- **Matplotlib / Seaborn** – Optional EDA plotting 
- **Logging** – Enables debugging and records workflow for traceability

  ## 🧩 Project Workflow

### 1. 🧠 Data Ingestion & Transformation (Script: `ingestion_db.py`)

### 2. 📊 Exploratory Data Analysis (EDA)

Performed initial EDA using Python:
- Identified and handled null values, outliers, and duplicates records
- Aggregated vendors by category and computed relevant performance metrics
- Used summary statistics to understand data distribution and trends
- Optional visualizations: Bar charts, box plots, etc.

### 3. 📈 Vendor Performance Analysis
It answers following business questions:
- Identifying Brands that needs Promotional or Pricing Adjustments which exhibit lower sales performance but higher profit margins.
- Which vendors and brands demonstrate the highest sales performance?
- Which vendors contribute the most to toal purchase dollars?
- How much of total procurement is dependent on the top vendors?
- Does purchasing in bulk reduce the unit price, and what is the optimal purchase volume for cost savings?
- How much capital is locked in unsold inventory per vendor and which vendors contribute the most to it?

  ### 4. 📉 Power BI Dashboard

![image](https://github.com/user-attachments/assets/07a32b68-783a-4a5a-abd8-19811b13974a)

![image](https://github.com/user-attachments/assets/ed666aa2-e286-442e-93f3-b567e1f03bf8)
