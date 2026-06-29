import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(
    page_title="Procurement Intelligence",
    layout="wide"
)

st.title("Procurement Intelligence Dashboard")

df = pd.read_csv("data/procurement_transactions.csv")

st.write(df.head())

total_spend = df["spend"].sum()

total_suppliers = df["supplier"].nunique()

total_categories = df["category"].nunique()

total_orders = len(df)


col1, col2, col3, col4 ,col5= st.columns(5)

col1.metric("Total Spend", f"₹{total_spend:,.0f}")
col2.metric("Suppliers", total_suppliers)
col3.metric("Categories", total_categories)
col4.metric("Orders", total_orders)
col5.metric('eww',33)


from src.analytics.summary import get_summary
from src.analytics.spend import category_spend

fig = px.bar(
    category_spend,
    x='category',
    y='spend',
    title='Spend by Category'
)
st.plotly_chart(fig, use_container_width=True)


supplier_spend = (
    df.groupby('supplier')['spend']
    .sum()
    .reset_index()
    .sort_values('spend',ascending=False)
)

fig = px.bar(
    supplier_spend.head(10),

    x='supplier',
    y='spend',
    title='Top 10 supliers'
)

st.plotly_chart(fig,use_container_width=True)




df["order_date"] = pd.to_datetime(df["order_date"])

df["month"] = (
    df["order_date"]
      .dt.to_period("M")
      .astype(str)
)

monthly_spend = (
    df.groupby("month")["spend"]
      .sum()
      .reset_index()
)

fig = px.line(
    monthly_spend,
    x="month",
    y="spend",
    title="Monthly Spend Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Suppliers")

st.dataframe(
    supplier_spend.head(20),
    use_container_width=True
)


st.sidebar.header("Filters")


selected_category = st.sidebar.multiselect(
    "Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)


filtered_df = df[
    df["category"].isin(selected_category)
]


supplier_item_price = (
    df.groupby(["item", "supplier"])["unit_price"]
      .mean()
      .reset_index()
)

cheapest_supplier = (
    supplier_item_price
    .sort_values("unit_price")
    .groupby("item")
    .first()
    .reset_index()
)

cheapest_supplier.columns = [
    "item",
    "best_supplier",
    "best_price"
]

consolidation = supplier_item_price.merge(
    cheapest_supplier,
    on="item"
)

consolidation["price_difference"] = (
    consolidation["unit_price"]
    - consolidation["best_price"]
)

consolidation = consolidation[
    consolidation["price_difference"] > 0
]

st.subheader("Supplier Consolidation Opportunities")

st.dataframe(
    consolidation.sort_values(
        "price_difference",
        ascending=False
    )
)


price_stats = (
    df.groupby("item")["unit_price"]
      .agg(["mean", "std"])
      .reset_index()
)

price_check = df.merge(
    price_stats,
    on="item"
)

price_check["z_score"] = (
    (price_check["unit_price"] - price_check["mean"])
    / price_check["std"]
)

anomalies = price_check[
    abs(price_check["z_score"]) > 2
]


st.subheader("Price Variance Anomalies")

st.dataframe(
    anomalies[
        [
            "supplier",
            "item",
            "unit_price",
            "z_score"
        ]
    ]
) 


supplier_spend = (
    df.groupby("supplier")["spend"]
      .sum()
      .reset_index()
)

total_spend = supplier_spend["spend"].sum()

supplier_spend["share"] = (
    supplier_spend["spend"] / total_spend
)

tail_spend = supplier_spend[
    supplier_spend["share"] < 0.01
]

st.subheader("Tail Spend Suppliers")

st.dataframe(tail_spend)



preferred_suppliers = {
    "IT Hardware": ["Lenovo"],
    "Software": ["Microsoft"],
    "Marketing": ["Publicis"],
    "Logistics": ["BlueDart"],
    "Office Supplies": ["Office Depot"]
}

def is_maverick(row):
    return row["supplier"] not in preferred_suppliers[row["category"]]

df["maverick"] = df.apply(
    is_maverick,
    axis=1
)
 
maverick_spend = df[
    df["maverick"]
]

st.subheader("Maverick Spend")

st.metric(
    "Maverick Transactions",
    len(maverick_spend)
)

st.metric(
    "Maverick Spend Value",
    f"₹{maverick_spend['spend'].sum():,.0f}"
)
# ==================================
# FORECAST SECTION
# ==================================

import joblib

st.header("Spend Forecast")

model = joblib.load("models/spend_forecaster.pkl")
le = joblib.load("models/category_encoder.pkl")

# Monthly aggregation

monthly_df = (
    df.groupby(["month", "category"])["spend"]
      .sum()
      .reset_index()
)

monthly_df["month"] = pd.to_datetime(monthly_df["month"])

monthly_df["year"] = monthly_df["month"].dt.year
monthly_df["month_num"] = monthly_df["month"].dt.month
monthly_df["quarter"] = monthly_df["month"].dt.quarter

monthly_df = monthly_df.sort_values(
    ["category", "month"]
)

# Lag features

monthly_df["lag_1"] = (
    monthly_df.groupby("category")["spend"]
    .shift(1)
)

monthly_df["lag_2"] = (
    monthly_df.groupby("category")["spend"]
    .shift(2)
)

monthly_df["lag_3"] = (
    monthly_df.groupby("category")["spend"]
    .shift(3)
)

monthly_df["rolling_3"] = (
    monthly_df.groupby("category")["spend"]
    .rolling(3)
    .mean()
    .reset_index(level=0, drop=True)
)

monthly_df = monthly_df.dropna()

# IMPORTANT:
# Use saved encoder, don't fit a new one

monthly_df["category_encoded"] = le.transform(
    monthly_df["category"]
)

# Get latest row per category

latest_data = (
    monthly_df
    .sort_values("month")
    .groupby("category")
    .tail(1)
    .copy()
)

# Create next month features

latest_data["month_num"] += 1

latest_data.loc[
    latest_data["month_num"] > 12,
    "month_num"
] = 1

latest_data.loc[
    latest_data["month_num"] == 1,
    "year"
] += 1

latest_data["quarter"] = (
    (latest_data["month_num"] - 1) // 3
) + 1

features = [
    "year",
    "month_num",
    "quarter",
    "category_encoded",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_3"
]

latest_data["forecast_spend"] = model.predict(
    latest_data[features]
)

forecast_table = latest_data[
    ["category", "forecast_spend"]
].copy()

forecast_table["forecast_spend"] = (
    forecast_table["forecast_spend"]
    .round(0)
)

st.dataframe(
    forecast_table,
    use_container_width=True
)

fig = px.bar(
    forecast_table,
    x="category",
    y="forecast_spend",
    title="Next Month Spend Forecast"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# button for usr question

st.header("🤖 Procurement Copilot")

user_question = st.text_area(
    "Ask a procurement question",
    height=100
)

ask_button = st.button("Ask Copilot")

# some context for copilot
top_supplier = (
    df.groupby("supplier")["spend"]
      .sum()
      .idxmax()
)

top_category = (
    df.groupby("category")["spend"]
      .sum()
      .idxmax()
)

total_spend = int(df["spend"].sum())

maverick_spend_value = int(
    maverick_spend["spend"].sum()
)

potential_savings = int(
    consolidation["price_difference"].sum()
)


#copilot
import sys,os 

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
  
from copilot.procurement_copilot import ask_copilot
analytics_context = f"""
Total Spend: {total_spend}
Top Supplier: {top_supplier}
Top Category: {top_category}
Potential Savings: {potential_savings} 
"""

if ask_button:

    try:
        answer = ask_copilot(
            user_question,
            analytics_context
        )
        st.write(answer)

    except Exception as e:
        st.error(
            f"Copilot unavailable: {e}"
        )

    st.write(answer)