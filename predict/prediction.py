import pandas as pd
import joblib

def predict(df: pd.DataFrame) -> int:
    with open("model/model.pkl", "rb") as f:
        model = joblib.load(f)

    predicted_price = model.predict(df)[0]

    # Convert numpy types to native Python types
    predicted_price_value = (
        predicted_price.item()
    )  # .item() converts numpy scalar to Python float/int

    return round(predicted_price_value)
