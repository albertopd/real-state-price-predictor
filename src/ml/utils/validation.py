"""Data validation utilities."""

import pandas as pd
from typing import List


def validate_data(df: pd.DataFrame, required_columns: List[str]) -> None:
    """Validate input data."""
    if df.empty:
        raise ValueError("Dataset is empty")

    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if df.isna().any().any():
        nan_summary = df.isna().sum()
        nan_cols = nan_summary[nan_summary > 0]
        raise ValueError(f"Data contains NaN values:\n{nan_cols}")


def detect_data_drift(X_train: pd.DataFrame, X_test: pd.DataFrame, 
                     threshold: float = 0.1) -> List[str]:
    """Detect potential data drift between train and test sets."""
    drift_columns = []
    
    for col in X_train.columns:
        if X_train[col].dtype in ['int64', 'float64']:
            train_mean = X_train[col].mean()
            test_mean = X_test[col].mean()
            
            if train_mean != 0:
                relative_diff = abs(test_mean - train_mean) / abs(train_mean)
                if relative_diff > threshold:
                    drift_columns.append(col)
    
    return drift_columns
