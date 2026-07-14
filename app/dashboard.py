import pandas as pd
import streamlit as st
import plotly.express as px
import requests

st.set_page_config(
    page_title="Procurement Intelligence",
    layout="wide"
)

st.title("Procurement Intelligence Dashboard")

df = pd.read_csv("data/procurement_transactions.csv")

st.write(df.head())

summary = requests.get(
    "http://127.0.0.1:8000/analytics/summary"
).json()

total_spend = summary["total_spend"]
total_suppliers = summary["total_suppliers"]
total_categories = summary["total_categories"]
total_orders = summary["total_orders"]

col1, col2, col3, col4 ,col5= st.columns(5)

col1.metric("Total Spend", f"₹{total_spend:,.0f}")
col2.metric("Suppliers", total_suppliers)
col3.metric("Categories", total_categories)
col4.metric("Orders", total_orders)
col5.metric('eww',33)


category_spend = requests.get(
    "http://127.0.0.1:8000/analytics/category-spend"
).json()

category_spend = pd.DataFrame(category_spend)



fig = px.bar(
    category_spend,
    x='category',
    y='spend',
    title='Spend by Category'
)
st.plotly_chart(fig, use_container_width=True)


supplier_spend = requests.get(
    "http://127.0.0.1:8000/analytics/top-suppliers"
).json()

supplier_spend = pd.DataFrame(supplier_spend)

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

monthly_spend = requests.get(
    "http://127.0.0.1:8000/analytics/monthly-trend"
).json()

monthly_spend = pd.DataFrame(monthly_spend)

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

consolidation = requests.get(
    "http://127.0.0.1:8000/analytics/supplier-consolidation"
).json()

consolidation = pd.DataFrame(consolidation)
st.subheader("Supplier Consolidation Opportunities")

st.dataframe(
    consolidation.sort_values(
        "price_difference",
        ascending=False
    )
)

anomalies = requests.get(
    "http://127.0.0.1:8000/analytics/price-anomalies"
).json()

anomalies = pd.DataFrame(anomalies)

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


tail_spend = requests.get(
    "http://127.0.0.1:8000/analytics/tail-spend"
).json()

tail_spend = pd.DataFrame(tail_spend)



total_spend=summary["total_spend"]

st.subheader("Tail Spend Suppliers")

st.dataframe(tail_spend)



maverick = requests.get(
    "http://127.0.0.1:8000/analytics/maverick-spend"
).json()

st.subheader("Maverick Spend")

st.metric(
    "Maverick Transactions",
    maverick["transactions"]
)

st.metric(
    "Maverick Spend Value",
    f"₹{maverick['spend'].sum():,.0f}"
)
# ==================================
# FORECAST SECTION
# ==================================

import joblib

st.header("Spend Forecast")

forecast_table = requests.get(
    "http://127.0.0.1:8000/forecast/next-month"
).json()

forecast_table = pd.DataFrame(forecast_table)




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

from copilot.procurement_copilot import ask_copilot
analytics_context = f"""
Total Spend: {total_spend}
Top Supplier: {top_supplier}
Top Category: {top_category}
Potential Savings: {potential_savings} 
"""

if ask_button:

    try:
        response = requests.post(
    "http://127.0.0.1:8000/copilot/ask",
    json={
        "question": user_question,
        "context": analytics_context
    }
)

        answer = response.json()["answer"]

        st.write(answer)

    except Exception as e:
        st.error(
            f"Copilot unavailable: {e}"
        )

    st.write(answer)