import pandas as pd

from src.data_loader import df
from src.model_loader import model, encoder


def predict_spend(data):

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)

    return float(prediction[0])


def forecast_next_month():

    monthly_df = (
        df.groupby(["month", "category"])["spend"]
        .sum()
        .reset_index()
    )

    monthly_df["month"] = pd.to_datetime(
        monthly_df["month"]
    )

    monthly_df["year"] = (
        monthly_df["month"].dt.year
    )

    monthly_df["month_num"] = (
        monthly_df["month"].dt.month
    )

    monthly_df["quarter"] = (
        monthly_df["month"].dt.quarter
    )

    monthly_df = monthly_df.sort_values(
        ["category", "month"]
    )

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

    monthly_df["category_encoded"] = encoder.transform(
        monthly_df["category"]
    )

    latest_data = (
        monthly_df
        .sort_values("month")
        .groupby("category")
        .tail(1)
        .copy()
    )

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
        [
            "category",
            "forecast_spend"
        ]
    ].copy()

    forecast_table["forecast_spend"] = (
        forecast_table["forecast_spend"]
        .round(0)
    )

    return forecast_table