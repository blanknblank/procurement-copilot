import pandas as pd

print("Loading procurement dataset...")

df = pd.read_csv("data/procurement_transactions.csv")

df["order_date"] = pd.to_datetime(df["order_date"])