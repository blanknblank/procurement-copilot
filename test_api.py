import requests

category_spend = requests.get(

    "http://api:8000/analytics/category-spend"

).json()