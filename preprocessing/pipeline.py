import pandas as pd
from sklearn.pipeline import Pipeline
from preprocessing.transformers import MapEncoder, BooleanEncoder, AddLatLon
from preprocessing.mappings import type_map, subtype_map, province_map, epc_score_map
from typing import Union

bool_columns = [
    "hasAttic", "hasTerrace", "hasGarden", "hasLift", "hasOffice", "hasDiningRoom",
    "hasSwimmingPool", "hasFireplace", "hasPhotovoltaicPanels", "hasAirConditioning",
    "hasHeatPump", "hasBasement", "hasArmoredDoor", "hasVisiophone", "hasDressingRoom",
    "hasLivingRoom"
]

class DataFramePipeline(Pipeline):
    """
    A scikit-learn Pipeline subclass that returns the transformed output as a pandas DataFrame.

    This pipeline is designed to process property data by applying a series of
    transformations such as adding geolocation, encoding categorical variables via mapping,
    and encoding boolean features. It appends new encoded columns to the original DataFrame columns.

    Methods
    -------
    fit_transform(X: pd.DataFrame, y=None, **fit_params) -> pd.DataFrame
        Fit the pipeline on the input DataFrame X and return the transformed DataFrame
        with original plus new encoded columns.
    """

    def fit_transform(self, X: pd.DataFrame, y=None, **fit_params) -> pd.DataFrame:
        """
        Fit the pipeline and transform the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            Input data frame containing raw features.
        y : array-like, optional
            Target variable (default is None).
        **fit_params : dict
            Additional parameters to pass to the fit method.

        Returns
        -------
        pd.DataFrame
            A new DataFrame containing the original columns plus:
            - 'lat', 'lon' columns added by AddLatLon transformer
            - Encoded columns: 'type_encoded', 'subtype_encoded', 'province_encoded', 'epcScore_encoded'
            - Encoded boolean feature columns, each suffixed with '_encoded'
        """
        column_names = X.columns.tolist() + [
            "lat", "lon", "type_encoded", "subtype_encoded",
            "province_encoded", "epcScore_encoded"
        ] + [f"{col}_encoded" for col in bool_columns]

        transformed = super().fit_transform(X, y, **fit_params)
        return pd.DataFrame(transformed, columns=column_names)


preprocessing_pipeline = DataFramePipeline([
    ("latlon", AddLatLon()),
    ("type", MapEncoder(type_map, "type", "type_encoded")),
    ("subtype", MapEncoder(subtype_map, "subtype", "subtype_encoded")),
    ("province", MapEncoder(province_map, "province", "province_encoded")),
    ("epc", MapEncoder(epc_score_map, "epcScore", "epcScore_encoded")),
    ("bools", BooleanEncoder(bool_columns)),
])


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the input property DataFrame by applying a series of transformations.

    This function applies the full preprocessing pipeline which:
    - Adds latitude and longitude based on address or coordinates
    - Maps categorical columns to encoded numeric values
    - Encodes multiple boolean feature columns

    Parameters
    ----------
    df : pd.DataFrame
        Raw input DataFrame containing property data.

    Returns
    -------
    pd.DataFrame
        Transformed DataFrame including original features and newly added encoded columns.
    """
    return preprocessing_pipeline.fit_transform(df)
