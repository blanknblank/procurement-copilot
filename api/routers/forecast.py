from fastapi import APIRouter
from pydantic import BaseModel

from src.forecasting import predict_spend

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
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


@router.post("/")
def forecast(request: ForecastRequest):

    prediction = predict_spend(
        request.model_dump()
    )

    return {
        "forecast": round(prediction, 2)
    }