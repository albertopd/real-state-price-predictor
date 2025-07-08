import joblib
import os
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import xgboost as xgb
import pandas as pd


def predict(preprocessed_data: dict) -> float:
    try:
        df = pd.DataFrame([preprocessed_data])

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "model", "model.pkl")
        model = joblib.load(model_path)

        predicted_price = model.predict(df)
        predicted_price = round(float(predicted_price[0]), 2)
        return predicted_price

    except Exception as e:
        raise ValueError(f"Prediction failed: {e}")
