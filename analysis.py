import pandas as pd
from pathlib import Path

DATA = Path(__file__).with_name("Afficionado Coffee Roasters.xlsx")
OUT = Path(__file__).with_name("outputs")
OUT.mkdir(exist_ok=True)
df = pd.read_excel(DATA, sheet_name="Transactions")
df["revenue"] = df["transaction_qty"] * df["unit_price"]
df["transaction_time"] = pd.to_datetime(df["transaction_time"].astype(str), format="%H:%M:%S", errors="coerce")
df["hour"] = df["transaction_time"].dt.hour
df["time_period"] = pd.cut(df["hour"], bins=[5,10,14,17,21],
    labels=["Morning (6–10)","Late morning (11–14)","Afternoon (15–17)","Evening (18–21)"],
    right=True, include_lowest=True)
df.to_csv(OUT/"cleaned_transactions.csv", index=False)
for col, filename in [("product_category","category_summary.csv"),("store_location","store_summary.csv"),("time_period","time_period_summary.csv")]:
    summary = df.groupby(col, observed=False).agg(transactions=("transaction_id","count"),
        quantity=("transaction_qty","sum"), revenue=("revenue","sum")).sort_values("revenue",ascending=False)
    summary.to_csv(OUT/filename)
print(f"Rows: {len(df):,} | Revenue: {df.revenue.sum():,.2f} | Units: {df.transaction_qty.sum():,}")
print("No transaction date exists; weekday and monthly analyses cannot be calculated.")
