from __future__ import annotations
from pathlib import Path
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


def _assemble_dataframe(raw_dir: Path) -> pd.DataFrame:
    apts = list((raw_dir / "apartments").glob("*.parquet"))
    houses = list((raw_dir / "houses").glob("*.parquet"))
    frames = []
    for p in apts + houses:
        frames.append(pd.read_parquet(p))
    if not frames:
        raise RuntimeError("No raw data found to build training dataset")
    return pd.concat(frames, ignore_index=True)


def build_training_datasets(raw_dir: Path, out_dir: Path, test_size: float = 0.2) -> None:
    df = _assemble_dataframe(raw_dir)

    # Drop rows with missing critical fields
    df = df.dropna(subset=["price_eur", "living_area_m2", "postal_code"])

    # Define features and target
    y = df["price_eur"]
    X = df.drop(columns=["price_eur", "id", "listing_date"])

    numeric = [c for c in X.columns if X[c].dtype != "object"]
    categoric = [c for c in X.columns if X[c].dtype == "object"]

    # Preprocessing: impute numeric NaNs, scale numeric, encode categorical
    pre = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ]), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categoric),
        ]
    )

    pipe = Pipeline([("pre", pre)])
    X_trans = pipe.fit_transform(X)

    # Build transformed dataframe
    X_cols_num = numeric
    X_cols_cat = list(pipe.named_steps["pre"].named_transformers_["cat"].get_feature_names_out(categoric))
    X_all = pd.DataFrame(X_trans, columns=X_cols_num + X_cols_cat)
    X_all["target_price_eur"] = y.reset_index(drop=True)

    # Split train/test
    train_df, test_df = train_test_split(X_all, test_size=test_size, random_state=42)

    # Save both parquet files
    out_dir.mkdir(parents=True, exist_ok=True)
    train_file = out_dir / "train_data.parquet"
    test_file = out_dir / "test_data.parquet"

    train_df.to_parquet(train_file, index=False)
    test_df.to_parquet(test_file, index=False)

    print(f"Training set saved to {train_file} ({train_df.shape})")
    print(f"Test set saved to {test_file} ({test_df.shape})")
