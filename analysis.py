"""Retail Sales Analysis: cleaning, KPIs, charts and Power BI-ready export."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)


def load_and_clean(path="data/raw_sales.csv"):
    df = pd.read_csv(path)
    print(f"Raw rows: {len(df)}")

    # 1. Remove duplicate rows
    df = df.drop_duplicates()

    # 2. Standardise text columns
    df["category"] = df["category"].str.strip().str.title()
    df["payment_mode"] = df["payment_mode"].str.strip()

    # 3. Handle missing values
    df["region"] = df["region"].fillna("Unknown")
    df["discount"] = df["discount"].fillna(0)
    df["quantity"] = df["quantity"].fillna(df["quantity"].median()).astype(int)

    # 4. Fix data types and create features
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["year"] = df["order_date"].dt.year
    df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)

    print(f"Clean rows: {len(df)}  |  Missing values left: {int(df.isna().sum().sum())}")
    return df


def kpis(df):
    summary = {
        "Total Revenue": df["revenue"].sum(),
        "Total Orders": df["order_id"].nunique(),
        "Units Sold": int(df["quantity"].sum()),
        "Average Order Value": df["revenue"].mean(),
        "Unique Customers": df["customer_id"].nunique(),
    }
    print("\n--- KPIs ---")
    for k, v in summary.items():
        print(f"{k:22s}: {v:,.2f}")
    pd.Series(summary).to_csv(OUT / "kpi_summary.csv", header=["value"])
    return summary


def bar(series, title, fname, xlabel="", ylabel="Revenue (INR)", horizontal=False):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if horizontal:
        series.sort_values().plot.barh(ax=ax, color="#2a6f97")
    else:
        series.plot.bar(ax=ax, color="#2a6f97", rot=30)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(OUT / fname, dpi=150)
    plt.close(fig)


def main():
    df = load_and_clean()
    kpis(df)

    monthly = df.groupby("month")["revenue"].sum()
    by_category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    top_products = df.groupby("product")["revenue"].sum().nlargest(10)
    by_payment = df.groupby("payment_mode")["order_id"].count()

    # Monthly trend (line chart)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    monthly.plot(ax=ax, marker="o", color="#2a6f97")
    ax.set_title("Monthly Revenue Trend", fontweight="bold")
    ax.set_ylabel("Revenue (INR)")
    ax.set_xlabel("")
    plt.xticks(range(0, len(monthly), 2), monthly.index[::2], rotation=45)
    fig.tight_layout()
    fig.savefig(OUT / "monthly_revenue.png", dpi=150)
    plt.close(fig)

    bar(by_category, "Revenue by Category", "revenue_by_category.png")
    bar(by_region, "Revenue by Region", "revenue_by_region.png")
    bar(top_products, "Top 10 Products by Revenue", "top_products.png", horizontal=True)
    bar(by_payment, "Orders by Payment Mode", "payment_modes.png", ylabel="Orders")

    # Month-over-month growth
    mom = monthly.pct_change().mul(100).round(2).rename("mom_growth_pct")
    print("\nBest month :", monthly.idxmax(), f"({monthly.max():,.0f})")
    print("Worst month:", monthly.idxmin(), f"({monthly.min():,.0f})")
    print("Top category:", by_category.idxmax())
    print("Top region  :", by_region.idxmax())

    # Exports (Power BI / SQL ready)
    df.to_csv(OUT / "clean_sales.csv", index=False)
    pd.concat([monthly.rename("revenue"), mom], axis=1).to_csv(OUT / "monthly_summary.csv")
    print("\nSaved cleaned data and charts in the outputs/ folder")


if __name__ == "__main__":
    main()
