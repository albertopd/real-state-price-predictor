import pandas as pd
import os
import joblib


def predict_price(df: pd.DataFrame, model_path: str) -> int:
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at '{model_path}'")
        raise FileNotFoundError(f"Model file not found at '{model_path}'")

    with open(model_path, "rb") as f:
        model = joblib.load(f)

    predicted_price = model.predict(df)[0]

    # Convert numpy scalar to native Python type
    predicted_price_value = predicted_price.item()

    return round(predicted_price_value)
