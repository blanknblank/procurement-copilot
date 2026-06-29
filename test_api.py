import requests

payload = {
    "year": 2025,
    "month_num": 6,
    "quarter": 2,
    "category_encoded": 0,
    "lag_1": 1200000,
    "lag_2": 1180000,
    "lag_3": 1210000,
    "rolling_3": 1195000
}

response = requests.post(
    "http://127.0.0.1:8000/forecast",
    json=payload
)

print(response.json())