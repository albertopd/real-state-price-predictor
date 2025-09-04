import pandas as pd
import os
import joblib

def predict(df: pd.DataFrame, model_path: str) -> int:
    """
    Load a pre-trained model and predict a price based on the input DataFrame.

    This function loads a serialized model from "model/model.joblib" using joblib,
    applies the model's predict method to the input DataFrame, extracts the first
    prediction, converts it to a native Python type, and returns it rounded as an integer.

    Parameters
    ----------
    df : pd.DataFrame
        Input data containing features for the prediction. Must match the model's expected input format.

    Returns
    -------
    int
        The predicted price rounded to the nearest integer.
    """
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at '{model_path}'")
        raise FileNotFoundError(f"Model file not found at '{model_path}'")

    with open(model_path, "rb") as f:
        model = joblib.load(f)

    predicted_price = model.predict(df)[0]

    # Convert numpy scalar to native Python type
    predicted_price_value = predicted_price.item()

    return round(predicted_price_value)
