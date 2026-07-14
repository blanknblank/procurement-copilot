import requests

BASE_URL = "http://api:8000"

def get(endpoint):
    return requests.get(
        f"{BASE_URL}{endpoint}"
    ).json()

def post(endpoint, data):
    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=data
    ).json()