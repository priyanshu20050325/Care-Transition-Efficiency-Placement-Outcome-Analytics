# 📊 Child Processing Pipeline Dashboard

## 📌 Project Overview

The **Child Processing Pipeline Dashboard** is a data analysis and visualization project developed using **Python, Pandas, Plotly, and Streamlit**.

The project analyzes child movement through the **CBP (Customs and Border Protection)** and **HHS (Department of Health and Human Services)** processing pipeline.

The dashboard transforms raw daily operational data into meaningful **KPIs, trends, performance indicators, pressure metrics, bottleneck alerts, and analytical insights**.

The main objective is to understand how children move through different stages of the processing pipeline and identify periods of increased operational pressure.

---

## 🎯 Project Objectives

The main objectives of this project are:

- Analyze daily child processing data.
- Measure CBP apprehensions and transfers.
- Analyze HHS discharges.
- Monitor CBP custody and HHS care populations.
- Calculate important performance KPIs.
- Identify potential CBP and HHS bottlenecks.
- Analyze daily and monthly trends.
- Measure discharge stability.
- Identify highest and lowest activity periods.
- Provide an interactive dashboard for data-driven analysis.

---

## 🗂️ Dataset

The dataset contains daily observations covering the period:

**12 January 2023 – 21 December 2025**

### Main Variables

| Column | Description |
|---|---|
| Date | Date of observation |
| Children apprehended and placed in CBP custody* | Number of children apprehended and placed in CBP custody |
| Children in CBP custody | Number of children currently in CBP custody |
| Children transferred out of CBP custody | Number of children transferred from CBP custody |
| Children in HHS Care | Number of children currently in HHS care |
| Children discharged from HHS Care | Number of children discharged from HHS care |

---

# 🛠️ Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Plotly**
- **Streamlit**
- **Matplotlib**
- **Jupyter Notebook / VS Code**
- **Git & GitHub**

---

# 🔍 Exploratory Data Analysis

Before building the dashboard, extensive Exploratory Data Analysis (EDA) was performed.

The EDA included:

### 1. Data Cleaning

- Converted the `Date` column to datetime format.
- Converted numerical columns to appropriate numeric types.
- Removed formatting characters such as commas from numerical values.
- Checked missing values.
- Checked duplicate rows.
- Verified data types.
- Checked dataset dimensions.

Final cleaned dataset:

**720 rows × 6 columns**

---

### 2. Descriptive Statistics

Calculated:

- Mean
- Median
- Standard deviation
- Minimum
- Maximum
- First quartile (Q1)
- Third quartile (Q3)
- Interquartile range (IQR)

These statistics helped understand the distribution and variability of the operational data.

---

### 3. Outlier Analysis

Box plots and the IQR method were used to identify potential outliers.

The IQR method uses:

```text
IQR = Q3 - Q1