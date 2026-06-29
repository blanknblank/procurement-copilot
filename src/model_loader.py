import joblib

print("Loading XGBoost model...")

model = joblib.load("models/spend_forecaster.pkl")

encoder = joblib.load("models/category_encoder.pkl")