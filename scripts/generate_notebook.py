"""
Generate the Retail Sales EDA Jupyter Notebook programmatically.
This creates a complete .ipynb file with all cells.
"""
import nbformat as nbf
import os

nb = nbf.v4.new_notebook()
nb.metadata.kernelspec = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}
nb.metadata.language_info = {
    "name": "python",
    "version": "3.14.5"
}

cells = []

# ═══════════════════════════════════════════════════════════════
# TITLE & INTRODUCTION
# ═══════════════════════════════════════════════════════════════
cells.append(nbf.v4.new_markdown_cell("""# 🛒 Online Retail Sales — Exploratory Data Analysis

---

**Dataset**: [Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) (UCI Machine Learning Repository)  
**Period**: December 2009 — December 2011  
**Records**: ~1,067,371 transactions  
**Source**: A UK-based, registered non-store online retail company specializing in unique all-occasion gifts.

## 📋 Project Objectives

1. **Clean** the raw transactional data — handle missing values, duplicates, outliers (IQR method), type casting, and datetime parsing  
2. **Engineer features** — revenue, time components, customer segmentation  
3. **Explore** the data through 10 professional visualizations  
4. **Extract** 5 actionable business insights backed by data  

---"""))

# ═══════════════════════════════════════════════════════════════
# SECTION 1: SETUP & DATA LOADING
# ═══════════════════════════════════════════════════════════════
cells.append(nbf.v4.new_markdown_cell("""## 1. Setup & Data Loading

Import libraries, configure plotting styles, and load the raw dataset."""))

cells.append(nbf.v4.new_code_cell("""# ── Imports ──────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# ── Plotting Configuration ───────────────────────────────────────
sns.set_theme(style='whitegrid', font_scale=1.15)
plt.rcParams.update({
    'figure.figsize': (12, 6),
    'figure.dpi': 120,
    'axes.titleweight': 'bold',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'font.family': 'sans-serif',
})

# Custom color palette — vibrant but professional
PALETTE = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B',
           '#44BBA4', '#E94F37', '#393E41', '#D4B483', '#5C946E']
sns.set_palette(PALETTE)

print("✅ Libraries loaded and plot style configured.")"""))

cells.append(nbf.v4.new_code_cell("""# ── Load Raw Data ────────────────────────────────────────────────
# The dataset is split across two sheets (Year 2009-2010 and Year 2010-2011)
DATA_PATH = '../data/online_retail_II.xlsx'

print("Loading Sheet 1 (2009-2010)...")
df1 = pd.read_excel(DATA_PATH, sheet_name='Year 2009-2010', engine='openpyxl')
print(f"  → {df1.shape[0]:,} rows loaded.")

print("Loading Sheet 2 (2010-2011)...")
df2 = pd.read_excel(DATA_PATH, sheet_name='Year 2010-2011', engine='openpyxl')
print(f"  → {df2.shape[0]:,} rows loaded.")

# Combine into a single DataFrame
df_raw = pd.concat([df1, df2], ignore_index=True)
print(f"\\n📊 Combined dataset: {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")"""))

cells.append(nbf.v4.new_code_cell("""# ── Initial Inspection ───────────────────────────────────────────
print("=" * 60)
print("COLUMN TYPES & NON-NULL COUNTS")
print("=" * 60)
df_raw.info()

print("\\n")
print("=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
df_raw.head()"""))

cells.append(nbf.v4.new_code_cell("""# ── Descriptive Statistics ────────────────────────────────────────
df_raw.describe(include='all').round(2)"""))

# ═══════════════════════════════════════════════════════════════
# SECTION 2: DATA CLEANING
# ═══════════════════════════════════════════════════════════════
cells.append(nbf.v4.new_markdown_cell("""---

## 2. Data Cleaning (Deep)

A thorough, multi-step cleaning pipeline: missing values → duplicates → invalid records → type casting → datetime parsing → outlier removal → feature engineering."""))

cells.append(nbf.v4.new_code_cell("""# ── 2.1 Missing Values ───────────────────────────────────────────
missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing %', ascending=False)

print("🔍 Missing Values Summary")
print("=" * 45)
print(missing_df.to_string())
print(f"\\nTotal rows before cleaning: {len(df_raw):,}")"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.2 Create Working Copy & Drop Missing Descriptions ──────────
df = df_raw.copy()

# Drop rows where Description is missing (these are unidentifiable products)
df = df.dropna(subset=['Description'])

# Drop rows where Customer ID is missing (cannot attribute to a customer)
df = df.dropna(subset=['Customer ID'])

print(f"After dropping missing Description & Customer ID: {len(df):,} rows "
      f"({len(df_raw) - len(df):,} removed, {(len(df_raw) - len(df)) / len(df_raw) * 100:.1f}%)")"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.3 Remove Duplicates ────────────────────────────────────────
dup_count = df.duplicated().sum()
print(f"Duplicate rows found: {dup_count:,}")

df = df.drop_duplicates()
print(f"After removing duplicates: {len(df):,} rows")"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.4 Remove Cancelled / Invalid Orders ────────────────────────
# Cancelled invoices start with 'C'
df['Invoice'] = df['Invoice'].astype(str)
cancelled_mask = df['Invoice'].str.startswith('C')
cancelled_count = cancelled_mask.sum()
print(f"Cancelled orders (Invoice starts with 'C'): {cancelled_count:,}")

df = df[~cancelled_mask]

# Remove negative or zero quantities
invalid_qty = (df['Quantity'] <= 0).sum()
print(f"Rows with Quantity ≤ 0: {invalid_qty:,}")
df = df[df['Quantity'] > 0]

# Remove negative or zero prices
invalid_price = (df['Price'] <= 0).sum()
print(f"Rows with Price ≤ 0: {invalid_price:,}")
df = df[df['Price'] > 0]

print(f"\\nAfter removing invalid records: {len(df):,} rows")"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.5 Type Casting ─────────────────────────────────────────────
# Ensure proper data types
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Customer ID'] = df['Customer ID'].astype(int).astype(str)
df['Invoice'] = df['Invoice'].astype(str)
df['StockCode'] = df['StockCode'].astype(str)
df['Quantity'] = df['Quantity'].astype(int)
df['Price'] = df['Price'].astype(float)

print("✅ Type casting complete:")
print(df.dtypes)"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.6 Datetime Feature Extraction ──────────────────────────────
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
df['Hour'] = df['InvoiceDate'].dt.hour
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
df['Quarter'] = df['InvoiceDate'].dt.quarter
df['YearQuarter'] = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)

print("✅ Datetime features extracted:")
print(df[['InvoiceDate', 'Year', 'Month', 'DayOfWeek', 'Hour', 'Quarter']].head())"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.7 Feature Engineering: Revenue ─────────────────────────────
df['Revenue'] = df['Quantity'] * df['Price']

print(f"Revenue column created.")
print(f"  Total Revenue: £{df['Revenue'].sum():,.2f}")
print(f"  Avg Revenue per Transaction Line: £{df['Revenue'].mean():,.2f}")
print(f"  Median Revenue per Transaction Line: £{df['Revenue'].median():,.2f}")"""))

cells.append(nbf.v4.new_code_cell("""# ── 2.8 Outlier Detection & Removal (IQR Method) ────────────────
def remove_outliers_iqr(data, column, multiplier=1.5):
    \"\"\"Remove outliers using the IQR method and return cleaned data + stats.\"\"\"
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    cleaned = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    
    print(f"  {column}:")
    print(f"    Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
    print(f"    Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"    Outliers removed: {len(outliers):,} ({len(outliers)/len(data)*100:.1f}%)")
    
    return cleaned

print("🔍 Outlier Removal (IQR Method, multiplier=1.5)")
print("=" * 50)

rows_before = len(df)
df = remove_outliers_iqr(df, 'Quantity')
df = remove_outliers_iqr(df, 'Price')
df = remove_outliers_iqr(df, 'Revenue')

print(f"\\n📊 Final dataset: {len(df):,} rows (removed {rows_before - len(df):,} outliers total)")"""))

cells.append(nbf.v4.new_markdown_cell("""### 🧹 Cleaning Summary"""))

cells.append(nbf.v4.new_code_cell("""# ── Cleaning Summary ─────────────────────────────────────────────
print("=" * 55)
print("DATA CLEANING SUMMARY")
print("=" * 55)
print(f"  Raw records:           {len(df_raw):>10,}")
print(f"  After cleaning:        {len(df):>10,}")
print(f"  Records removed:       {len(df_raw) - len(df):>10,}")
print(f"  Retention rate:        {len(df)/len(df_raw)*100:>9.1f}%")
print(f"  Date range:            {df['InvoiceDate'].min().strftime('%Y-%m-%d')} → {df['InvoiceDate'].max().strftime('%Y-%m-%d')}")
print(f"  Unique customers:      {df['Customer ID'].nunique():>10,}")
print(f"  Unique products:       {df['StockCode'].nunique():>10,}")
print(f"  Unique countries:      {df['Country'].nunique():>10,}")
print(f"  Total revenue:         £{df['Revenue'].sum():>12,.2f}")
print("=" * 55)

df.head()"""))

# ═══════════════════════════════════════════════════════════════
# SECTION 3: EXPLORATORY DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════
cells.append(nbf.v4.new_markdown_cell("""---

## 3. Exploratory Data Analysis — 10 Visualizations

Professional, publication-ready charts exploring revenue trends, customer behavior, product performance, and geographic distribution."""))

# ── VIZ 1: Monthly Revenue Trend ──
cells.append(nbf.v4.new_markdown_cell("""### 📈 3.1 Monthly Revenue Trend"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 1: Monthly Revenue Trend (Line Chart) ───────────────────
monthly_rev = df.groupby('InvoiceMonth')['Revenue'].sum().reset_index()
monthly_rev['InvoiceMonth'] = monthly_rev['InvoiceMonth'].astype(str)

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly_rev['InvoiceMonth'], monthly_rev['Revenue'],
        color=PALETTE[0], linewidth=2.5, marker='o', markersize=7,
        markerfacecolor='white', markeredgewidth=2, markeredgecolor=PALETTE[0])

# Highlight peak month
peak_idx = monthly_rev['Revenue'].idxmax()
ax.annotate(f"Peak: £{monthly_rev.loc[peak_idx, 'Revenue']:,.0f}",
            xy=(peak_idx, monthly_rev.loc[peak_idx, 'Revenue']),
            xytext=(peak_idx - 2, monthly_rev.loc[peak_idx, 'Revenue'] * 1.08),
            fontsize=10, fontweight='bold', color=PALETTE[3],
            arrowprops=dict(arrowstyle='->', color=PALETTE[3], lw=1.5))

ax.fill_between(range(len(monthly_rev)), monthly_rev['Revenue'],
                alpha=0.08, color=PALETTE[0])
ax.set_title('Monthly Revenue Trend (2009–2011)', fontsize=16, pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue (£)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
plt.xticks(rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)
sns.despine()
plt.tight_layout()
plt.savefig('../outputs/01_monthly_revenue_trend.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 2: Top 10 Products by Revenue ──
cells.append(nbf.v4.new_markdown_cell("""### 🏆 3.2 Top 10 Products by Revenue"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 2: Top 10 Products by Revenue (Horizontal Bar) ──────────
product_rev = (df.groupby('Description')['Revenue']
               .sum()
               .sort_values(ascending=False)
               .head(10)
               .sort_values())

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(product_rev.index, product_rev.values, 
               color=PALETTE[:10][::-1], edgecolor='white', linewidth=0.5, height=0.7)

# Add value labels
for bar, val in zip(bars, product_rev.values):
    ax.text(val + product_rev.max() * 0.01, bar.get_y() + bar.get_height() / 2,
            f'£{val:,.0f}', va='center', fontsize=10, fontweight='bold', color='#333')

ax.set_title('Top 10 Products by Total Revenue', fontsize=16, pad=15)
ax.set_xlabel('Total Revenue (£)', fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
ax.set_xlim(0, product_rev.max() * 1.15)
sns.despine(left=True)
ax.tick_params(left=False)
ax.grid(axis='x', alpha=0.2)
plt.tight_layout()
plt.savefig('../outputs/02_top10_products_revenue.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 3: Sales by Country Heatmap ──
cells.append(nbf.v4.new_markdown_cell("""### 🌍 3.3 Sales by Country × Month Heatmap"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 3: Sales by Country Heatmap (Top 10 Countries × Months) ─
# Get top 10 countries by revenue (excluding UK for better contrast)
top_countries = (df.groupby('Country')['Revenue']
                 .sum()
                 .sort_values(ascending=False)
                 .head(10)
                 .index.tolist())

df_top_countries = df[df['Country'].isin(top_countries)]
heatmap_data = (df_top_countries.groupby(['Country', 'Month'])['Revenue']
                .sum()
                .unstack(fill_value=0))

# Reorder by total revenue
country_order = heatmap_data.sum(axis=1).sort_values(ascending=False).index
heatmap_data = heatmap_data.loc[country_order]

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(heatmap_data, annot=True, fmt=',.0f', cmap='YlOrRd',
            linewidths=0.5, linecolor='white',
            cbar_kws={'label': 'Revenue (£)', 'shrink': 0.8},
            ax=ax)
ax.set_title('Revenue Heatmap: Top 10 Countries × Month', fontsize=16, pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('')
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.savefig('../outputs/03_country_month_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 4: Order Quantity Distribution ──
cells.append(nbf.v4.new_markdown_cell("""### 📊 3.4 Order Quantity Distribution"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 4: Order Quantity Distribution (Histogram + KDE) ─────────
fig, ax = plt.subplots(figsize=(12, 6))

sns.histplot(df['Quantity'], bins=50, kde=True, color=PALETTE[0],
             edgecolor='white', linewidth=0.5, alpha=0.7,
             line_kws={'linewidth': 2.5}, ax=ax)

# Add statistical annotations
median_qty = df['Quantity'].median()
mean_qty = df['Quantity'].mean()
ax.axvline(median_qty, color=PALETTE[3], linestyle='--', linewidth=2, label=f'Median: {median_qty:.0f}')
ax.axvline(mean_qty, color=PALETTE[1], linestyle='--', linewidth=2, label=f'Mean: {mean_qty:.1f}')

ax.set_title('Distribution of Order Quantities', fontsize=16, pad=15)
ax.set_xlabel('Quantity per Transaction Line', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend(fontsize=11, framealpha=0.9)
sns.despine()
plt.tight_layout()
plt.savefig('../outputs/04_quantity_distribution.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"Quantity Stats — Mean: {mean_qty:.1f}, Median: {median_qty:.0f}, "
      f"Std: {df['Quantity'].std():.1f}, Skewness: {df['Quantity'].skew():.2f}")"""))

# ── VIZ 5: Correlation Matrix ──
cells.append(nbf.v4.new_markdown_cell("""### 🔗 3.5 Correlation Matrix"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 5: Correlation Matrix (Numeric Features) ────────────────
numeric_cols = ['Quantity', 'Price', 'Revenue', 'Month', 'Hour', 'Quarter']
corr_matrix = df[numeric_cols].corr()

# Create mask for upper triangle
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            square=True, linewidths=1, linecolor='white',
            cbar_kws={'shrink': 0.8, 'label': 'Correlation'},
            ax=ax)
ax.set_title('Correlation Matrix — Numeric Features', fontsize=16, pad=15)
plt.tight_layout()
plt.savefig('../outputs/05_correlation_matrix.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 6: Revenue by Day of Week ──
cells.append(nbf.v4.new_markdown_cell("""### 📅 3.6 Revenue by Day of Week"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 6: Revenue by Day of Week ────────────────────────────────
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
day_rev = (df.groupby('DayOfWeek')['Revenue']
           .sum()
           .reindex(day_order)
           .dropna())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(day_rev.index, day_rev.values, color=PALETTE[:len(day_rev)],
              edgecolor='white', linewidth=0.5, width=0.65)

# Highlight the peak day
peak_day = day_rev.idxmax()
peak_idx_bar = list(day_rev.index).index(peak_day)
bars[peak_idx_bar].set_edgecolor(PALETTE[3])
bars[peak_idx_bar].set_linewidth(3)

for bar, val in zip(bars, day_rev.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + day_rev.max() * 0.01,
            f'£{val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Total Revenue by Day of Week', fontsize=16, pad=15)
ax.set_ylabel('Revenue (£)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
ax.set_ylim(0, day_rev.max() * 1.12)
sns.despine()
ax.grid(axis='y', alpha=0.2)
plt.tight_layout()
plt.savefig('../outputs/06_revenue_by_day.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 7: Top 10 Customers ──
cells.append(nbf.v4.new_markdown_cell("""### 👥 3.7 Top 10 Customers by Revenue"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 7: Top 10 Customers by Revenue ───────────────────────────
customer_rev = (df.groupby('Customer ID')['Revenue']
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .sort_values())

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(customer_rev.index, customer_rev.values,
               color=PALETTE[:10][::-1], edgecolor='white', linewidth=0.5, height=0.65)

for bar, val in zip(bars, customer_rev.values):
    ax.text(val + customer_rev.max() * 0.01, bar.get_y() + bar.get_height() / 2,
            f'£{val:,.0f}', va='center', fontsize=10, fontweight='bold', color='#333')

# Pareto annotation
total_rev = df['Revenue'].sum()
top10_rev = customer_rev.sum()
ax.text(0.97, 0.05, f'Top 10 = {top10_rev/total_rev*100:.1f}% of total revenue',
        transform=ax.transAxes, ha='right', fontsize=11,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3E0', edgecolor='#F18F01', alpha=0.9))

ax.set_title('Top 10 Customers by Total Revenue', fontsize=16, pad=15)
ax.set_xlabel('Total Revenue (£)', fontsize=12)
ax.set_ylabel('Customer ID', fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
ax.set_xlim(0, customer_rev.max() * 1.18)
sns.despine(left=True)
ax.tick_params(left=False)
ax.grid(axis='x', alpha=0.2)
plt.tight_layout()
plt.savefig('../outputs/07_top10_customers.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 8: Hourly Order Volume ──
cells.append(nbf.v4.new_markdown_cell("""### ⏰ 3.8 Hourly Order Volume"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 8: Hourly Order Volume ───────────────────────────────────
hourly = df.groupby('Hour').agg(
    Orders=('Invoice', 'nunique'),
    Revenue=('Revenue', 'sum')
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar chart for order count
bars = ax1.bar(hourly['Hour'], hourly['Orders'], color=PALETTE[0],
               alpha=0.7, edgecolor='white', linewidth=0.5, width=0.7, label='Orders')
ax1.set_xlabel('Hour of Day', fontsize=12)
ax1.set_ylabel('Number of Orders', fontsize=12, color=PALETTE[0])
ax1.tick_params(axis='y', labelcolor=PALETTE[0])

# Line chart for revenue on secondary axis
ax2 = ax1.twinx()
ax2.plot(hourly['Hour'], hourly['Revenue'], color=PALETTE[3],
         linewidth=2.5, marker='D', markersize=6, label='Revenue')
ax2.set_ylabel('Revenue (£)', fontsize=12, color=PALETTE[3])
ax2.tick_params(axis='y', labelcolor=PALETTE[3])
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))

# Peak hour annotation
peak_hour = hourly.loc[hourly['Orders'].idxmax(), 'Hour']
ax1.annotate(f'Peak: {peak_hour}:00', xy=(peak_hour, hourly['Orders'].max()),
             xytext=(peak_hour + 1.5, hourly['Orders'].max() * 1.05),
             fontsize=10, fontweight='bold', color=PALETTE[3],
             arrowprops=dict(arrowstyle='->', color=PALETTE[3]))

ax1.set_xticks(range(int(hourly['Hour'].min()), int(hourly['Hour'].max()) + 1))
ax1.set_title('Hourly Order Volume & Revenue', fontsize=16, pad=15)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

sns.despine(right=False)
plt.tight_layout()
plt.savefig('../outputs/08_hourly_orders.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 9: Revenue Box Plot by Quarter ──
cells.append(nbf.v4.new_markdown_cell("""### 📦 3.9 Revenue Distribution by Quarter"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 9: Revenue Distribution by Quarter (Box Plot) ────────────
fig, ax = plt.subplots(figsize=(12, 6))

# Create quarter labels in order
quarter_order = sorted(df['YearQuarter'].unique())

bp = sns.boxplot(x='YearQuarter', y='Revenue', data=df,
                 order=quarter_order, palette='viridis',
                 fliersize=2, flierprops=dict(alpha=0.3),
                 linewidth=1.2, ax=ax)

ax.set_title('Revenue Distribution by Quarter', fontsize=16, pad=15)
ax.set_xlabel('Quarter', fontsize=12)
ax.set_ylabel('Revenue per Transaction (£)', fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
plt.xticks(rotation=45, ha='right')
sns.despine()
ax.grid(axis='y', alpha=0.2)
plt.tight_layout()
plt.savefig('../outputs/09_revenue_boxplot_quarter.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ── VIZ 10: Monthly Customer Count Trend ──
cells.append(nbf.v4.new_markdown_cell("""### 👤 3.10 Monthly Unique Customer Count Trend"""))

cells.append(nbf.v4.new_code_cell("""# ── Viz 10: Monthly Unique Customer Count ────────────────────────
monthly_cust = (df.groupby('InvoiceMonth')['Customer ID']
                .nunique()
                .reset_index()
                .rename(columns={'Customer ID': 'UniqueCustomers'}))
monthly_cust['InvoiceMonth'] = monthly_cust['InvoiceMonth'].astype(str)

fig, ax = plt.subplots(figsize=(14, 6))

ax.fill_between(range(len(monthly_cust)), monthly_cust['UniqueCustomers'],
                alpha=0.15, color=PALETTE[5])
ax.plot(monthly_cust['InvoiceMonth'], monthly_cust['UniqueCustomers'],
        color=PALETTE[5], linewidth=2.5, marker='s', markersize=7,
        markerfacecolor='white', markeredgewidth=2, markeredgecolor=PALETTE[5])

# Annotate max & min
max_idx = monthly_cust['UniqueCustomers'].idxmax()
min_idx = monthly_cust['UniqueCustomers'].idxmin()

ax.annotate(f"Peak: {monthly_cust.loc[max_idx, 'UniqueCustomers']:,}",
            xy=(max_idx, monthly_cust.loc[max_idx, 'UniqueCustomers']),
            xytext=(max_idx - 2, monthly_cust.loc[max_idx, 'UniqueCustomers'] * 1.08),
            fontsize=10, fontweight='bold', color=PALETTE[5],
            arrowprops=dict(arrowstyle='->', color=PALETTE[5]))

ax.set_title('Monthly Unique Customer Count', fontsize=16, pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Unique Customers', fontsize=12)
plt.xticks(rotation=45, ha='right')
sns.despine()
ax.grid(axis='y', alpha=0.2)
plt.tight_layout()
plt.savefig('../outputs/10_monthly_customers.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# ═══════════════════════════════════════════════════════════════
# SECTION 4: BUSINESS INSIGHTS
# ═══════════════════════════════════════════════════════════════
cells.append(nbf.v4.new_markdown_cell("""---

## 4. Business Insights

Data-driven conclusions derived from the exploratory analysis above."""))

cells.append(nbf.v4.new_code_cell("""# ── Insight Calculations ─────────────────────────────────────────

# 1. Q4 Revenue Concentration
q4_rev = df[df['Quarter'] == 4]['Revenue'].sum()
annual_rev = df['Revenue'].sum()
q4_pct = q4_rev / annual_rev * 100

# 2. Customer Concentration (Pareto)
cust_rev = df.groupby('Customer ID')['Revenue'].sum().sort_values(ascending=False)
total_customers = len(cust_rev)
top_20_pct_count = int(total_customers * 0.20)
top_20_pct_rev = cust_rev.head(top_20_pct_count).sum() / annual_rev * 100

# 3. Geographic Dependency
country_rev = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
uk_pct = country_rev.get('United Kingdom', 0) / annual_rev * 100
top3_countries = country_rev.head(3)

# 4. Peak Trading Time
peak_day_name = (df.groupby('DayOfWeek')['Revenue'].sum()
                 .reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
                 .dropna().idxmax())
peak_hour_val = df.groupby('Hour')['Revenue'].sum().idxmax()

# 5. Product Concentration
product_rev_all = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False)
top_10_products_pct = product_rev_all.head(10).sum() / annual_rev * 100
total_products = len(product_rev_all)

print("✅ Insight calculations complete — see markdown below.")"""))

cells.append(nbf.v4.new_code_cell("""# ── Print Business Insights ──────────────────────────────────────
print("=" * 65)
print("📊 BUSINESS INSIGHTS")
print("=" * 65)

print(f\"\"\"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 INSIGHT 1: Q4 Seasonality Drives Disproportionate Revenue
   Q4 accounts for {q4_pct:.1f}% of total revenue.
   November alone typically sees the highest monthly sales,
   driven by pre-Christmas gifting. 
   → Recommendation: Increase inventory and marketing spend
     by 40-50% in September to prepare for Q4 demand surge.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 INSIGHT 2: Severe Customer Concentration Risk
   Top 20% of customers generate {top_20_pct_rev:.1f}% of revenue.
   Total customer base: {total_customers:,} unique customers.
   → Recommendation: Implement a loyalty/retention program for 
     top-tier customers while diversifying the revenue base
     through acquisition campaigns.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 INSIGHT 3: Heavy Geographic Revenue Dependency
   United Kingdom: {uk_pct:.1f}% of total revenue.
   Top 3 markets outside UK: {', '.join(top3_countries.index[1:4]) if len(top3_countries) > 1 else 'N/A'}
   → Recommendation: Accelerate international expansion in 
     top-performing EU markets (DACH region, Netherlands, France)
     to reduce single-market risk.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 INSIGHT 4: Clear Peak Trading Windows
   Peak day: {peak_day_name}
   Peak hour: {peak_hour_val}:00
   → Recommendation: Schedule promotions, email campaigns, and 
     flash sales during peak windows to maximize conversion.
     Ensure customer support staffing aligns with peak hours.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 INSIGHT 5: Long-Tail Product Portfolio
   Top 10 products generate {top_10_products_pct:.1f}% of revenue
   out of {total_products:,} total products.
   → Recommendation: Focus marketing on proven bestsellers while
     evaluating low-performing SKUs for discontinuation to reduce
     warehousing costs and inventory complexity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
\"\"\")"""))

# ═══════════════════════════════════════════════════════════════
# SECTION 5: SUMMARY
# ═══════════════════════════════════════════════════════════════
cells.append(nbf.v4.new_markdown_cell("""---

## 5. Summary & Next Steps

### What We Accomplished
| Step | Detail |
|------|--------|
| **Data Cleaning** | Handled missing values, duplicates, cancelled orders, type casting, datetime parsing, and IQR-based outlier removal |
| **Feature Engineering** | Created Revenue, time-based features (Year, Month, Day, Hour, Quarter) |
| **Visualizations** | 10 publication-ready charts covering trends, distributions, correlations, and geographic patterns |
| **Business Insights** | 5 data-backed, actionable conclusions with strategic recommendations |

### Recommended Next Steps
1. **Customer Segmentation** — Apply RFM (Recency, Frequency, Monetary) analysis for targeted marketing
2. **Demand Forecasting** — Use time-series models (ARIMA/Prophet) to predict monthly revenue
3. **Market Basket Analysis** — Identify product bundles using association rules
4. **Churn Prediction** — Build a classification model to identify at-risk customers
5. **Interactive Dashboard** — Deploy a Plotly/Dash dashboard for real-time monitoring

---

*Notebook by [Your Name] | Data source: [UCI ML Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)*"""))

# ═══════════════════════════════════════════════════════════════
# ASSEMBLE & SAVE
# ═══════════════════════════════════════════════════════════════
nb.cells = cells

output_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'retail_sales_eda.ipynb')
output_path = os.path.abspath(output_path)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook saved to: {output_path}")
print(f"Cells: {len(nb.cells)} ({sum(1 for c in nb.cells if c.cell_type == 'code')} code, "
      f"{sum(1 for c in nb.cells if c.cell_type == 'markdown')} markdown)")
