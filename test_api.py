import requests

category_spend = requests.get(

    "http://127.0.0.1:8000/analytics/category-spend"

).json()