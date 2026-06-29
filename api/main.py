from fastapi import FastAPI
from pydantic import BaseModel
from src.forecasting import predict_spend
from src.analytics.summary import get_summary
from src.analytics.spend import category_spend


app = FastAPI(
    title="Procurement Copilot API",
    version="1.0"
)


class ForecastRequest(BaseModel):
    year: int
    month_num: int
    quarter: int
    category_encoded: int
    lag_1: float
    lag_2: float
    lag_3: float
    rolling_3: float


@app.get("/")
def home():
    return {
        "message": "Procurement Copilot API is running"
    }


@app.post("/forecast")
def forecast(request: ForecastRequest):

    prediction = predict_spend(request.model_dump())

    return {
        "forecast": round(prediction, 2)
    }

@app.get("/analytics/summary")

def summary():

    return get_summary()


@app.get("/analytics/category-spend")

def spend():

    return category_spend()
@app.get("/analytics/category-spend")
def category_spend_api():
    return category_spend()

from src.analytics.suppliers import top_suppliers

@app.get("/analytics/top-suppliers")
def top_suppliers_api():
    return top_suppliers()