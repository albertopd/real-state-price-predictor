import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from utils.logging_utils import setup_logger


TRAINING_DATASET_FILE = "training_dataset.parquet"
PREPROCESSOR_FILE = "preprocessor.joblib"

logger = setup_logger(__name__)


def _assemble_dataframe(raw_dir: Path) -> pd.DataFrame:
    """
    Assemble dataframe by loading the latest parquet file from apartments and houses folders.

    Args:
        raw_dir: Directory containing 'apartments' and 'houses' subdirectories

    Returns:
        Combined dataframe from the latest files in each category
    """
    frames = []

    # Process apartments - get latest file
    apartments_dir = raw_dir / "apartments"
    if apartments_dir.exists():
        apt_files = list(apartments_dir.glob("*.parquet"))
        if apt_files:
            # Sort by modification time and get the latest
            latest_apt = max(apt_files, key=lambda p: p.stat().st_mtime)
            frames.append(pd.read_parquet(latest_apt))
            logger.info(f"Loaded latest apartments file: {latest_apt.name}")

    # Process houses - get latest file
    houses_dir = raw_dir / "houses"
    if houses_dir.exists():
        house_files = list(houses_dir.glob("*.parquet"))
        if house_files:
            # Sort by modification time and get the latest
            latest_house = max(house_files, key=lambda p: p.stat().st_mtime)
            frames.append(pd.read_parquet(latest_house))
            logger.info(f"Loaded latest houses file: {latest_house.name}")

    if not frames:
        raise RuntimeError("No parquet files found in apartments or houses directories")

    combined_df = pd.concat(frames, ignore_index=True)
    logger.info(f"Combined dataset shape: {combined_df.shape}")

    return combined_df


def prepare_training_dataset(raw_dir: Path, out_dir: Path) -> Path:
    """
    Prepare and preprocess the training dataset for later use by a trainer.

    Args:
        raw_dir: Directory containing raw data files
        out_dir: Directory to save the processed dataset
    """
    df = _assemble_dataframe(raw_dir)

    # Drop rows with missing critical fields
    df = df.dropna(subset=["Price", "Living area", "Postal Code"])

    if df.empty:
        raise ValueError(
            "No valid data remaining after dropping rows with missing critical fields"
        )

    # Define features and target
    y = df["Price"]
    X = df.drop(columns=["Price"])

    # Identify column types
    numeric_cols = [col for col in X.columns if X[col].dtype != "object"]
    categorical_cols = [col for col in X.columns if X[col].dtype == "object"]

    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="mean")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_cols,
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_cols,
            ),
        ]
    )

    # Fit and transform the data
    X_transformed = preprocessor.fit_transform(X)

    # Ensure we have a dense array
    if hasattr(X_transformed, "toarray"):
        # It's a sparse matrix - cast to Any to avoid type checker issues
        X_transformed = getattr(X_transformed, "toarray")()

    # Ensure it's a proper numpy array
    X_transformed = np.asarray(X_transformed)

    # Get feature names for the transformed data
    numeric_feature_names = numeric_cols
    categorical_feature_names = list(
        preprocessor.named_transformers_["categorical"].get_feature_names_out(
            categorical_cols
        )
    )
    all_feature_names = numeric_feature_names + categorical_feature_names

    # Create final dataframe with transformed features and target
    processed_df = pd.DataFrame(X_transformed, columns=all_feature_names)
    processed_df["target_price"] = y.reset_index(drop=True)

    # Ensure output directory exists
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save processed dataset
    training_dataset_path = out_dir / TRAINING_DATASET_FILE
    processed_df.to_parquet(training_dataset_path, index=False)

    # Also save the fitted preprocessor for potential reuse
    preprocessor_path = out_dir / PREPROCESSOR_FILE
    joblib.dump(preprocessor, preprocessor_path)

    logger.info(f"Processed dataset saved to {training_dataset_path}")
    logger.info(f"Dataset shape: {processed_df.shape}")
    logger.info(
        f"Features: {len(all_feature_names)} ({len(numeric_cols)} numeric, {len(categorical_feature_names)} categorical)"
    )
    logger.info(f"Preprocessor saved to {preprocessor_path}")

    return training_dataset_path
