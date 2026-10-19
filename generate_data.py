"""Generate a synthetic retail sales dataset (seeded, reproducible).

The data is intentionally messy (missing values, duplicates, inconsistent text)
so that the cleaning steps in analysis.py are meaningful.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000

catalog = {
    "Electronics": [("Wireless Earbuds", 1999), ("Smart Watch", 3499), ("Power Bank", 1299), ("Bluetooth Speaker", 2199)],
    "Clothing": [("T-Shirt", 499), ("Jeans", 1499), ("Jacket", 2999), ("Sneakers", 2499)],
    "Home & Kitchen": [("Mixer Grinder", 3299), ("Air Fryer", 5499), ("Water Bottle", 399), ("Bedsheet Set", 1199)],
    "Books": [("Python Handbook", 699), ("SQL Guide", 599), ("Data Science Basics", 899), ("Aptitude Prep", 349)],
}
regions = ["North", "South", "East", "West", "Central"]
payments = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"]

rows = []
for i in range(N):
    cat = rng.choice(list(catalog), p=[0.30, 0.30, 0.25, 0.15])
    product, price = catalog[cat][rng.integers(0, len(catalog[cat]))]
    rows.append({
        "order_id": f"ORD{100000 + i}",
        "order_date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(rng.integers(0, 730))),
        "customer_id": f"CUST{rng.integers(1, 1200):04d}",
        "region": rng.choice(regions, p=[0.22, 0.25, 0.15, 0.23, 0.15]),
        "category": cat,
        "product": product,
        "quantity": int(rng.integers(1, 6)),
        "unit_price": price,
        "discount": float(rng.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.4, 0.2, 0.2, 0.1, 0.1])),
        "payment_mode": rng.choice(payments, p=[0.38, 0.2, 0.17, 0.15, 0.10]),
    })

df = pd.DataFrame(rows)

# --- inject data-quality problems for cleaning practice ---
idx = rng.choice(df.index, 150, replace=False)
df.loc[idx, "region"] = None
idx = rng.choice(df.index, 120, replace=False)
df.loc[idx, "discount"] = None
idx = rng.choice(df.index, 80, replace=False)
df.loc[idx, "quantity"] = None
idx = rng.choice(df.index, 100, replace=False)
df.loc[idx, "category"] = df.loc[idx, "category"].str.upper()          # inconsistent case
idx = rng.choice(df.index, 100, replace=False)
df.loc[idx, "payment_mode"] = " " + df.loc[idx, "payment_mode"] + " "  # stray spaces
df = pd.concat([df, df.sample(60, random_state=1)], ignore_index=True)  # duplicate rows

df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
df.to_csv("data/raw_sales.csv", index=False)
print(f"Saved data/raw_sales.csv with {len(df)} rows")
