# Retail Sales Analysis (Python + SQL + Power BI)

An end-to-end data analysis project: generate a messy retail sales dataset, clean it with **Pandas**, calculate business KPIs, create charts, and export a Power BI / MySQL-ready file.

> **Note:** The dataset is **synthetic** (created by `generate_data.py` with a fixed random seed), so results are fully reproducible. No real customer data is used.

## Business Questions Answered
- What are the total revenue, orders, units sold and average order value?
- How does revenue change month by month? Which months are best and worst?
- Which categories, regions and products drive the most revenue?
- Which payment modes do customers prefer?
- Does giving a discount change the average order value?

## Tech Stack
Python (Pandas, NumPy, Matplotlib) | SQL (MySQL 8 window functions, CTEs) | Power BI (optional dashboard)

## Project Structure
```
retail-sales-analysis/
├── data/raw_sales.csv         # messy synthetic dataset (5,060 rows)
├── sql/queries.sql            # 7 analytical SQL queries
├── outputs/                   # cleaned data, KPI tables, charts
├── generate_data.py           # creates the raw dataset
├── analysis.py                # cleaning + KPIs + charts + export
└── requirements.txt
```

## Data Cleaning Steps
| Problem in raw data | Fix |
|---|---|
| 60 duplicate rows | `drop_duplicates()` |
| Inconsistent category text (e.g. `ELECTRONICS`) | strip spaces + title case |
| Extra spaces in payment mode | `str.strip()` |
| Missing region (150) | filled with `Unknown` |
| Missing discount (120) | filled with `0` |
| Missing quantity (80) | filled with median |
| Date stored as text | converted to datetime, month/year features added |

Revenue is calculated as `quantity x unit_price x (1 - discount)`.

## How to Run
```bash
git clone https://github.com/<your-username>/retail-sales-analysis.git
cd retail-sales-analysis
pip install -r requirements.txt

python generate_data.py   # creates data/raw_sales.csv
python analysis.py        # cleans data, prints KPIs, saves charts to outputs/
```

## Sample Output (seed = 42)
| KPI | Value |
|---|---|
| Total Revenue | INR 2.79 crore (27,902,681) |
| Total Orders | 5,000 |
| Units Sold | 15,035 |
| Average Order Value | INR 5,581 |
| Unique Customers | 1,185 |

- Top category: **Electronics** | Top region: **South**
- Best month: **Aug 2025** | Weakest month: **Sep 2024**

Charts are saved in `outputs/` (monthly trend, category, region, top products, payment modes).

## Using SQL
1. Import `outputs/clean_sales.csv` into a MySQL table named `sales`.
2. Run the queries in `sql/queries.sql` (covers `RANK`, `LAG`, `ROW_NUMBER`, CTEs and share-of-total calculations).

## Power BI Dashboard (Optional)
Load `outputs/clean_sales.csv` into Power BI and build: KPI cards, monthly revenue line chart, category/region bar charts, and slicers for year, region and category. Add a screenshot to this README (`![Dashboard](dashboard.png)`).

## Key Learnings
- Practical data cleaning: duplicates, missing values, inconsistent text, data types
- Feature engineering for time-series reporting
- Translating business questions into Pandas and SQL
- Preparing a clean dataset for BI tools

## Author
**Kaustubh Parashar** - B.Tech CSE | Aspiring Data Analyst
[LinkedIn](#) | [GitHub](#)
