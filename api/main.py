from fastapi import FastAPI
from pydantic import BaseModel
from src.analytics import get_dashboard_summary
from src.forecasting import predict_spend

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
def analytics_summary():

    return get_dashboard_summary()