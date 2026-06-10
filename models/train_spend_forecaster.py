import pandas as pd
import mlflow
import mlflow.sklearn

df = pd.read_csv('data/procurement_transactions.csv')


# #### Forecast
df["order_date"] = pd.to_datetime(df["order_date"])

df["month"] = (
    df["order_date"]
    .dt.to_period("M")
    .astype(str)
)


monthly_df = (
    df.groupby(
        ["month", "category"]
    )["spend"]
    .sum()
    .reset_index()
)


monthly_df["month"] = pd.to_datetime(
    monthly_df["month"]
)

monthly_df["year"] = monthly_df["month"].dt.year

monthly_df["month_num"] = monthly_df["month"].dt.month

monthly_df["quarter"] = monthly_df["month"].dt.quarter



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

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

monthly_df["category_encoded"] = (
    le.fit_transform(
        monthly_df["category"]
    )
)

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

target = "spend"

train_size = int(
    len(monthly_df) * 0.8
)

train = monthly_df.iloc[:train_size]
test = monthly_df.iloc[train_size:]

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error

model = XGBRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    random_state=42
)

# model.fit(
#     train[features],
#     train[target]
# )

# predictions = model.predict(
#     test[features]
# )


# mape = mean_absolute_percentage_error(
#     test[target],
#     predictions
# )
# print("MAPE:", round(mape * 100, 2), "%")


X_train = train[features]
y_train = train[target]
X_test,y_test = test[features],test[target]


with mlflow.start_run():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mape = mean_absolute_percentage_error(
        y_test,
        predictions
    )

    mlflow.log_param(
        "n_estimators",
        200
    )

    mlflow.log_param(
        "max_depth",
        5
    )

    mlflow.log_metric(
        "mape",
        mape
    )

    mlflow.sklearn.log_model(
        model,
        "spend_forecaster"
    )

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance.sort_values(
    "importance",
    ascending=False
)

# print(importance)

importance.to_csv(
    "models/feature_importance.csv",
    index=False
)

mlflow.log_artifact(
    "models/feature_importance.csv"
)

import joblib

joblib.dump(
    model,
    "models/spend_forecaster.pkl"
)



joblib.dump(le, "models/category_encoder.pkl")

mlflow.sklearn.log_model(
    sk_model=model,
    artifact_path="spend_forecaster"
)