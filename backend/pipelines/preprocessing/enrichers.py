from importlib import resources
import os
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class PostalCodeEnricher(BaseEstimator, TransformerMixin):
    """
    Transformer that enriches a DataFrame with latitude and longitude columns
    based on postal codes using a reference CSV.
    """

    def __init__(self):
        self._geo_df_unique = None

    def fit(self, X, y=None):
        # Load and preprocess georef CSV once during fitting
        with resources.open_text("pipelines.preprocessing.data", "georef-belgium-postal-codes.csv") as f:
            geo_df = pd.read_csv(f, delimiter=";")

        geo_df[["lat", "lon"]] = geo_df["Geo Point"].str.split(",", expand=True)
        geo_df["lat"] = geo_df["lat"].astype(float)
        geo_df["lon"] = geo_df["lon"].astype(float)
        geo_df["postCode"] = geo_df["Post code"].astype(str)

        self._geo_df_unique = geo_df.drop_duplicates(subset=["postCode"])

        return self

    def transform(self, X):
        assert self._geo_df_unique is not None, "fit() must be called before transform()"
        
        df = X.copy()
        df["postCode"] = df["postCode"].astype(str)

        return df.merge(
            self._geo_df_unique[["postCode", "lat", "lon"]],
            on="postCode",
            how="left"
        )