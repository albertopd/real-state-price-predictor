from sklearn.base import BaseEstimator, TransformerMixin
from utils.feature_engineering import add_lat_lon

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
    Transformer that adds latitude and longitude columns to the DataFrame.

    Uses the external utility function `add_lat_lon` to compute lat/lon values.

    Methods
    -------
    fit(X, y=None)
        Does nothing and returns self. Required for sklearn compatibility.
    transform(X)
        Returns a DataFrame with latitude and longitude columns added.
    """

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
        self : AddLatLon
            Returns self.
        """
        return self

    def transform(self, X):
        """
        Add latitude and longitude columns to the input DataFrame.

        Parameters
        ----------
        X : pandas.DataFrame
            Input data to transform.

        Returns
        -------
        pandas.DataFrame
            DataFrame with added 'lat' and 'lon' columns.
        """
        return add_lat_lon(X)