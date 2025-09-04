import os
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class MapEncoder(BaseEstimator, TransformerMixin):
    """
    Transformer that maps categorical values in a specified column to new encoded values.

    Parameters
    ----------
    mapping : dict
        Dictionary mapping original category values to encoded values.
    column : str
        Name of the input column to map.
    output_column : str
        Name of the output column to store mapped/encoded values.

    Methods
    -------
    fit(X, y=None)
        Does nothing and returns self. Required for sklearn compatibility.
    transform(X)
        Returns a DataFrame with the new encoded column added.
    """

    def __init__(self, mapping: dict, column: str, output_column: str):
        self.mapping = mapping
        self.column = column
        self.output_column = output_column

    def fit(self, X, y=None):
        """
        Fit method - no fitting necessary for this transformer.

        Parameters
        ----------
        X : pandas.DataFrame
            Input data.
        y : None
            Ignored.

        Returns
        -------
        self : MapEncoder
            Returns self.
        """
        return self

    def transform(self, X):
        """
        Map values in the specified column using the provided mapping dictionary.

        Parameters
        ----------
        X : pandas.DataFrame
            Input data to transform.

        Returns
        -------
        pandas.DataFrame
            DataFrame with a new column containing mapped values.
        """
        X = X.copy()
        X[self.output_column] = X[self.column].map(self.mapping)
        return X


class BooleanEncoder(BaseEstimator, TransformerMixin):
    """
    Transformer that converts boolean columns into integer encoded columns (0/1).

    Parameters
    ----------
    columns : list of str
        List of column names containing boolean values to encode.

    Methods
    -------
    fit(X, y=None)
        Does nothing and returns self. Required for sklearn compatibility.
    transform(X)
        Returns a DataFrame with encoded boolean columns appended.
    """

    def __init__(self, columns: list):
        self.columns = columns

    def fit(self, X, y=None):
        """
        Fit method - no fitting necessary for this transformer.

        Parameters
        ----------
        X : pandas.DataFrame
            Input data.
        y : None
            Ignored.

        Returns
        -------
        self : BooleanEncoder
            Returns self.
        """
        return self

    def transform(self, X):
        """
        Encode specified boolean columns as integers (0 or 1).

        Parameters
        ----------
        X : pandas.DataFrame
            Input data to transform.

        Returns
        -------
        pandas.DataFrame
            DataFrame with new columns for each boolean column encoded as integers,
            suffixed with '_encoded'.
        """
        X = X.copy()
        for col in self.columns:
            X[f"{col}_encoded"] = X[col].astype(int)
        return X


class AddLatLon(BaseEstimator, TransformerMixin):
    """
    Transformer that adds latitude and longitude columns to a DataFrame
    using a postal codes CSV.
    """

    def __init__(self, georef_csv_path: str | None = None):
        """
        Parameters
        ----------
        georef_csv_path : str | None
            Path to the CSV containing postal codes and geolocation.
            Defaults to '../../data/georef-belgium-postal-codes.csv' relative to this file.
        """
        if georef_csv_path is None:
            # Relative path to the data folder from this file
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
            georef_csv_path = os.path.join(base_dir, "georef-belgium-postal-codes.csv")
        if not os.path.exists(georef_csv_path):
            print(f"Error: Georef CSV file not found at {georef_csv_path}")
            raise FileNotFoundError(f"Georef CSV file not found at {georef_csv_path}")
        self.georef_csv_path = georef_csv_path
        self._geo_df_unique = None

    def fit(self, X, y=None):
        # Load and preprocess georef CSV once during fitting
        geo_df = pd.read_csv(self.georef_csv_path, delimiter=";")
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