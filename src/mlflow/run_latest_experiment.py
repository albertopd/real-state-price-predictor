from pathlib import Path
import os
import mlflow
import mlflow.sklearn as mlflow_sklearn
import joblib
import shutil
import tempfile
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from mlflow.exceptions import MlflowException

# --- Detect MLflow URI ---
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://mlflow:5001" if os.path.exists("/.dockerenv") else "http://localhost:5001"
)
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def run_latest_experiment(test_data: Path, models_dir: Path):
    print(f"Using MLflow tracking at: {MLFLOW_TRACKING_URI}")

    # find latest model file
    pkl_files = sorted(models_dir.glob("*.pkl"), reverse=True)
    if not pkl_files:
        raise FileNotFoundError(f"No models found in {models_dir}")
    latest_model_path = pkl_files[0]
    print(f"Loading latest model: {latest_model_path}")

    # load model (joblib) and test data
    model = joblib.load(latest_model_path)
    df = pd.read_parquet(test_data)
    y_test = df["target_price_eur"]
    X_test = df.drop(columns=["target_price_eur"])

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Test MAE: {mae:.2f}, R2: {r2:.3f}")

    with mlflow.start_run(run_name="manual_test_run") as run:
        mlflow.log_metric("test_mae", float(mae))
        mlflow.log_metric("test_r2", float(r2))

        # Try to log model using mlflow.sklearn.log_model.
        # If the tracking server does not support the logged-models API (404),
        # fall back to uploading the model file as a plain artifact.
        try:
            print("Attempting mlflow.sklearn.log_model(...)")
            # avoid registry by not passing a registered_model_name; still may attempt registry internally
            mlflow_sklearn.log_model(model, artifact_path="model_tested")
            print("mlflow.sklearn.log_model succeeded.")
        except MlflowException as e:
            # Known problem: tracking-only server returns 404 for logged-models endpoint.
            print("mlflow.sklearn.log_model failed with MlflowException; falling back to log_artifact().")
            print("Exception:", str(e))
            # copy the model file into a temp dir and upload
            tmp_dir = Path(tempfile.mkdtemp(prefix="mlflow_model_tmp_"))
            try:
                tmp_file = tmp_dir / latest_model_path.name
                shutil.copy(latest_model_path, tmp_file)
                mlflow.log_artifact(str(tmp_file), artifact_path="model_tested")
                print(f"Uploaded model as artifact to run {run.info.run_id}")
            finally:
                # clean up temp dir
                shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception as ex:
            # any other unexpected error -> fallback too
            print("Unexpected error while logging model, fallback to log_artifact().")
            print("Error:", str(ex))
            tmp_dir = Path(tempfile.mkdtemp(prefix="mlflow_model_tmp_"))
            try:
                tmp_file = tmp_dir / latest_model_path.name
                shutil.copy(latest_model_path, tmp_file)
                mlflow.log_artifact(str(tmp_file), artifact_path="model_tested")
                print(f"Uploaded model as artifact to run {run.info.run_id}")
            finally:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    print("Experiment finished. View run at:", mlflow.get_tracking_uri(), f"/#/experiments/0/runs/{run.info.run_id}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    test_data = repo_root / "data" / "training" / "test_data.parquet"
    models_dir = repo_root / "ml_models"
    run_latest_experiment(test_data, models_dir)
