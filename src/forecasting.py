import joblib

model = joblib.load("models/spend_forecaster.pkl")
encoder = joblib.load("models/category_encoder.pkl")

def predict(features_df):
    prediction = model.predict(features_df)
    return float(prediction[0])

import pandas as pd

def predict_spend(data):

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return prediction[0]