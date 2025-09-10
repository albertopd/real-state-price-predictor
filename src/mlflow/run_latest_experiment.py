from pathlib import Path
import os
import mlflow
import mlflow.sklearn as mlflow_sklearn
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature

# --- Detect MLflow URI ---
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://mlflow:5001" if os.path.exists("/.dockerenv") else "http://localhost:5001",
)
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

REGISTERED_MODEL_NAME = "RealEstatePriceModel"


def test_mlflow_connection():
    """Test if MLflow server is accessible and Model Registry is enabled"""
    try:
        client = MlflowClient()
        # Test basic connection
        experiments = client.search_experiments()
        print(f"Connected to MLflow. Found {len(experiments)} experiments.")

        # Test Model Registry
        try:
            models = client.search_registered_models()
            print(f"Model Registry is accessible. Found {len(models)} registered models.")
            return True
        except Exception as e:
            print(f"Model Registry not accessible: {e}")
            return False
    except Exception as e:
        print(f"Cannot connect to MLflow: {e}")
        return False


def run_latest_experiment(test_data: Path, models_dir: Path):
    print(f"Using MLflow tracking at: {MLFLOW_TRACKING_URI}")
    print(f"MLflow version: {mlflow.__version__}\n")

    # Test connection first
    registry_available = test_mlflow_connection()

    # find latest model file
    pkl_files = sorted(models_dir.glob("*.pkl"), reverse=True)
    if not pkl_files:
        raise FileNotFoundError(f"\nNo models found in {models_dir}")
    latest_model_path = pkl_files[0]
    print(f"\nLoading latest model: {latest_model_path}")

    # load model and test data
    model = joblib.load(latest_model_path)
    df = pd.read_parquet(test_data)
    y_test = df["target_price_eur"]
    X_test = df.drop(columns=["target_price_eur"])

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nTest MAE: {mae:.2f}, R2: {r2:.3f}\n")

    with mlflow.start_run(run_name="manual_test_run") as run:
        mlflow.log_metric("test_mae", float(mae))
        mlflow.log_metric("test_r2", float(r2))

        # Create model signature and input example
        from mlflow.models.signature import infer_signature

        # Use a sample of test data for input example (first few rows)
        input_example = X_test.head(5)

        # Infer signature from test data
        signature = infer_signature(X_test, y_pred)

        if registry_available:
            try:
                # Log and register model with signature and input example
                mlflow_sklearn.log_model(
                    sk_model=model,
                    name="model",
                    registered_model_name=REGISTERED_MODEL_NAME,
                    signature=signature,
                    input_example=input_example,
                )
                print(f"Model logged and registered as '{REGISTERED_MODEL_NAME}' with signature")
            except Exception as e:
                print(f"Model registration failed: {e}")
                # Fall back to just logging
                mlflow_sklearn.log_model(
                    sk_model=model,
                    name="model",
                    signature=signature,
                    input_example=input_example,
                )
                print("Model logged without registration")
        else:
            # Just log the model without registration
            mlflow_sklearn.log_model(
                sk_model=model,
                name="model",
                signature=signature,
                input_example=input_example,
            )
            print("Model logged without registration (Registry not available)")

        run_url = f"{MLFLOW_TRACKING_URI}/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}"
        exp_url = f"{MLFLOW_TRACKING_URI}/#/experiments/{run.info.experiment_id}"

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    test_data = repo_root / "data" / "training" / "test_data.parquet"
    models_dir = repo_root / "ml_models"
    run_latest_experiment(test_data, models_dir)
