import pandas as pd

df = pd.read_csv("data/procurement_transactions.csv")
df["order_date"] = pd.to_datetime(df["order_date"])


def get_dashboard_summary():

    import requests

    summary = requests.get(
        "http://127.0.0.1:8000/analytics/summary"
    ).json()

    total_spend = summary["total_spend"]
    total_suppliers = summary["total_suppliers"]
    total_categories = summary["total_categories"]
    total_orders = summary["total_orders"]

    return {
        "total_spend": total_spend,
        "total_suppliers": total_suppliers,
        "total_categories": total_categories,
        "total_orders": total_orders
    }