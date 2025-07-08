import pandas as pd
import joblib

def predict(df: pd.DataFrame) -> int:
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
    with open("model/model.joblib", "rb") as f:
        model = joblib.load(f)

    predicted_price = model.predict(df)[0]

    # Convert numpy scalar to native Python type
    predicted_price_value = predicted_price.item()

    return round(predicted_price_value)
