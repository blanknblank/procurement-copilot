from fastapi import APIRouter

from src.analytics.summary import get_summary
from src.analytics.spend import category_spend
from src.analytics.suppliers import get_top_suppliers
from src.analytics.monthly_trend import get_monthly_trend


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def summary():
    return get_summary()


@router.get("/category-spend")
def category_spend_api():
    return category_spend()


@router.get("/top-suppliers")
def top_suppliers_api():
    return get_top_suppliers()

@router.get("/monthly-trend")
def monthly_trend_api():

    return get_monthly_trend()