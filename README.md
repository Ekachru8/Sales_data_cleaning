# 🛒 Online Retail Sales — Exploratory Data Analysis

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Website](https://img.shields.io/badge/🌐_Live_Website-Portfolio-2e86ab?style=for-the-badge)](https://ekachru8.github.io/Sales_data_cleaning/website/index.html)

> **🔗 Live Portfolio Website:** [https://ekachru8.github.io/Sales_data_cleaning/website/index.html](https://ekachru8.github.io/Sales_data_cleaning/website/index.html)
>
> **📂 GitHub Repository:** [https://github.com/Ekachru8/Sales_data_cleaning](https://github.com/Ekachru8/Sales_data_cleaning)

A comprehensive exploratory data analysis of **1M+ retail transactions** from a UK-based online gift store. This project demonstrates professional data cleaning, feature engineering, 10 publication-ready visualizations, and actionable business insights.

---

## 📊 Dataset

| Attribute | Detail |
|-----------|--------|
| **Source** | [UCI ML Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) |
| **Period** | December 2009 — December 2011 |
| **Records** | ~1,067,371 transactions |
| **Features** | Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country |
| **Business** | UK-based, non-store online retailer specializing in all-occasion gifts |

---

## 🔑 Key Findings

1. **Q4 Seasonality** — Q4 drives a disproportionate share of annual revenue, with November being the peak month driven by pre-Christmas demand
2. **Customer Concentration** — Top 20% of customers generate the vast majority of revenue, indicating significant Pareto concentration
3. **Geographic Dependency** — The UK dominates revenue, creating single-market risk; EU expansion is a clear growth lever
4. **Peak Trading Windows** — Clear daily and hourly patterns exist, enabling optimized promotional scheduling
5. **Product Portfolio** — A small number of bestselling products contribute outsized revenue, suggesting opportunities for SKU rationalization

---

## 📈 Visualizations

The notebook includes 10 professional charts:

| # | Visualization | Type |
|---|---------------|------|
| 1 | Monthly Revenue Trend | Line chart with peak annotation |
| 2 | Top 10 Products by Revenue | Horizontal bar chart |
| 3 | Sales by Country × Month | Seaborn heatmap |
| 4 | Order Quantity Distribution | Histogram + KDE |
| 5 | Correlation Matrix | Triangular heatmap |
| 6 | Revenue by Day of Week | Bar chart |
| 7 | Top 10 Customers by Revenue | Horizontal bar chart |
| 8 | Hourly Order Volume & Revenue | Dual-axis bar + line |
| 9 | Revenue Distribution by Quarter | Box plot |
| 10 | Monthly Unique Customer Count | Area line chart |

---

## 🧹 Data Cleaning Pipeline

- **Missing values** — Dropped rows with missing Customer ID and Description
- **Duplicates** — Identified and removed exact duplicate records
- **Invalid records** — Removed cancelled orders (Invoice prefix 'C'), negative quantities/prices
- **Type casting** — Enforced proper dtypes (datetime, int, float, string)
- **Datetime parsing** — Extracted Year, Month, DayOfWeek, Hour, Quarter features
- **Outlier removal** — IQR method (1.5× multiplier) on Quantity, Price, and Revenue
- **Feature engineering** — Created Revenue column (Quantity × Price)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Ekachru8/Sales_data_cleaning.git
cd Sales_data_cleaning

# Install dependencies
pip install -r requirements.txt
```

### Download the Dataset

Download the **Online Retail II** dataset from [UCI ML Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii) and place the `.xlsx` file in the `data/` directory:

```
Sales_data_cleaning/
└── data/
    └── online_retail_II.xlsx
```

### Run the Notebook

```bash
jupyter notebook notebooks/retail_sales_eda.ipynb
```

---

## 📁 Project Structure

```
Sales_data_cleaning/
├── data/                          # Raw dataset (not tracked in git)
│   └── online_retail_II.xlsx
├── notebooks/
│   └── retail_sales_eda.ipynb     # Main EDA notebook
├── outputs/                       # Exported chart PNGs
├── scripts/
│   └── generate_notebook.py       # Notebook generator script
├── website/                       # Portfolio website (GitHub Pages)
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠 Tech Stack

- **Python 3.10+** — Core language
- **Pandas** — Data manipulation and analysis
- **Matplotlib** — Base plotting library
- **Seaborn** — Statistical visualization
- **SciPy** — Statistical computations (IQR outlier detection)
- **OpenPyXL** — Excel file parsing
- **Jupyter** — Interactive notebook environment

---

## 📄 License

This project is licensed under the MIT License. The dataset is provided by the UCI Machine Learning Repository under its own terms.

---

*Built as a portfolio project demonstrating data cleaning and exploratory data analysis skills.*
