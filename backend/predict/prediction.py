import joblib
import os
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import xgboost as xgb
import pandas as pd
class HousePricePredictor:
    def __init__(self, model_dir: str = None):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_dir = os.path.join(self.base_dir, "model")
        self.model_path = os.path.join(self.model_dir, "model.pkl")
        self.model = self.load_model()


    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")
        model = joblib.load(self.model_path)
        return model

    def predict(self, preprocessed_data: dict) -> float:
        try:
            df = pd.DataFrame([preprocessed_data])
            predicted_price = self.model.predict(df)
            return round(float(predicted_price[0]), 2)
        except Exception as e:
            raise ValueError(f"Prediction failed: {e}")