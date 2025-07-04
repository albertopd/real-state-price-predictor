import pandas as pd
import joblib
import xgboost as xgb
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def predict(df: pd.DataFrame) -> float:
    with open('model/model.pkl', 'rb') as f:
        model = joblib.load(f)

    predicted_price = model.predict(df)

    return predicted_price