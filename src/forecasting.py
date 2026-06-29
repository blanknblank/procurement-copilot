import joblib
import pandas as pd

model = joblib.load("models/spend_forecaster.pkl")
encoder = joblib.load("models/category_encoder.pkl")


def predict_spend(data: dict):

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return float(prediction[0])