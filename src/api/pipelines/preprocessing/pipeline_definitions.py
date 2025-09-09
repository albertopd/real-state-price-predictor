import pandas as pd
from sklearn.pipeline import Pipeline
from pipelines.preprocessing.encoders import CategoryMapper, BooleanBinarizer
from pipelines.preprocessing.enrichers import PostalCodeEnricher
from pipelines.preprocessing.mappings import (
    property_type_map,
    property_subtype_map,
    province_map,
    epc_score_map,
)


bool_columns = [
    "hasAttic",
    "hasTerrace",
    "hasGarden",
    "hasLift",
    "hasOffice",
    "hasDiningRoom",
    "hasSwimmingPool",
    "hasFireplace",
    "hasPhotovoltaicPanels",
    "hasAirConditioning",
    "hasHeatPump",
    "hasBasement",
    "hasArmoredDoor",
    "hasVisiophone",
    "hasDressingRoom",
    "hasLivingRoom",
]


class PreprocessingPipeline(Pipeline):
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
        transformed = super().fit_transform(X, y, **fit_params)
        if isinstance(transformed, pd.DataFrame):
            return transformed
        return pd.DataFrame(transformed, index=X.index)


preprocessing_pipeline = PreprocessingPipeline(
    [
        ("geo", PostalCodeEnricher()),
        ("type", CategoryMapper(property_type_map, "type", "type_encoded")),
        ("subtype", CategoryMapper(property_subtype_map, "subtype", "subtype_encoded")),
        ("province", CategoryMapper(province_map, "province", "province_encoded")),
        ("epc", CategoryMapper(epc_score_map, "epcScore", "epcScore_encoded")),
        ("bools", BooleanBinarizer(bool_columns)),
    ]
)
