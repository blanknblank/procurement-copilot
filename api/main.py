from fastapi import FastAPI
from src.forecasting import predict
from pydantic import BaseModel

class ForecastRequest(BaseModel):

    year: int
    month_num: int
    quarter: int

    category_encoded: int

    lag_1: float
    lag_2: float
    lag_3: float

    rolling_3: float

from src.forecasting import predict_spend

app = FastAPI(
    title="Procurement Copilot API",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Procurement Copilot API is running"
    }

from fastapi import FastAPI


@app.post("/forecast")

def forecast(request: ForecastRequest):

    prediction = predict_spend(

        request.model_dump()

    )

    return {

        "forecast": round(prediction,2)

    }