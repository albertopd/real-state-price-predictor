from __future__ import annotations
from pathlib import Path
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import ElasticNet
import joblib
import mlflow
import mlflow.sklearn as mlflow_sklearn


def train_and_log_model(train_parquet: str | Path, models_dir: Path) -> str:
    df = pd.read_parquet(train_parquet)
    y = df["target_price_eur"]
    X = df.drop(columns=["target_price_eur"])

    if X.isna().any().any():
        raise ValueError("Training data contains NaNs. Check preprocessing!")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Simple baseline regressor
    model = ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42)
    with mlflow.start_run(run_name="nightly_regression"):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_metric("mae", float(mae))
        mlflow.log_metric("r2", float(r2))
        mlflow_sklearn.log_model(model, "model")

        # Persist a copy under models/ for the app to load without MLflow if desired
        stamp = time.strftime("%Y%m%d_%H%M%S")
        out = Path(models_dir) / f"{stamp}_elasticnet.pkl"
        out.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, out)

        mlflow.log_artifact(str(out))

    return str(out)
