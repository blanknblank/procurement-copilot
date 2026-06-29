from fastapi import FastAPI

from api.routers.analytics import router as analytics_router
from api.routers.forecast import router as forecast_router
from api.routers.copilot import router as copilot_router

app = FastAPI(
    title="Procurement Copilot API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Procurement Copilot API is running"
    }


app.include_router(analytics_router)
app.include_router(forecast_router)
app.include_router(copilot_router)