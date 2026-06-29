import pandas as pd

df = pd.read_csv("data/procurement_transactions.csv")

def get_summary():

    return {

        "total_spend": float(df["spend"].sum()),

        "total_suppliers": int(df["supplier"].nunique()),

        "total_categories": int(df["category"].nunique()),

        "total_orders": int(len(df))

    }