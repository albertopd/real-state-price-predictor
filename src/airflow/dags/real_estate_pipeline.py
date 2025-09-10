from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any
from airflow import DAG
from airflow.decorators import task
from airflow.models.baseoperator import chain

# Make project root importable for tasks
REPO_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from ml.training.train_regression import train_and_log_model
from ml.pipelines.analysis_preprocess import build_analysis_dataset
from ml.pipelines.training_preprocess import build_training_datasets
from scrapers.scrape_apartments import run as scrape_apartments_run
from scrapers.scrape_houses import run as scrape_houses_run


DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
ANALYSIS_DIR = DATA_DIR / "analysis"
TRAINING_DIR = DATA_DIR / "training"
MODELS_DIR = REPO_ROOT / "ml_models"


default_args = {
    "owner": "data-eng",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="real_estate_pipeline",
    start_date=datetime(2025, 9, 7),
    schedule="0 2 * * *",  # 02:00 every night
    catchup=False,
    default_args=default_args,
    tags=[
        "real_estate",
        "scraping",
        "etl",
        "ml-training",
        "dvc",
        "nightly",
        "data-eng",
    ]
) as dag:

    @task
    def scrape_apartments():
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_DIR / "apartments" / f"apartments_{datetime.utcnow().date()}.parquet"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rows = scrape_apartments_run()
        import pandas as pd
        pd.DataFrame(rows).to_parquet(out_path)
        return str(out_path)

    @task
    def scrape_houses():
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_DIR / "houses" / f"houses_{datetime.utcnow().date()}.parquet"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rows = scrape_houses_run()
        import pandas as pd
        pd.DataFrame(rows).to_parquet(out_path)
        return str(out_path)

    @task
    def version_raw_data_with_dvc():
        os.system("dvc add data/raw -q")
        os.system("dvc push -q")

    @task
    def prep_analysis():
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        out_file = ANALYSIS_DIR / "listings.parquet"
        build_analysis_dataset(RAW_DIR, out_file)
        return str(out_file)

    @task
    def prep_training():
        TRAINING_DIR.mkdir(parents=True, exist_ok=True)
        build_training_datasets(RAW_DIR, TRAINING_DIR)
        out_file = TRAINING_DIR / "train_data.parquet"
        return str(out_file)

    @task
    def version_prepared_data_with_dvc():
        os.system("dvc add data/analysis data/training -q")
        os.system("dvc push -q")

    @task
    def train_model(train_path: Any):
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        model_path = train_and_log_model(train_path, MODELS_DIR)
        return model_path

    @task
    def version_model_with_dvc():
        os.system("dvc add models -q")
        os.system("dvc push -q")

    # Graph
    t_scrape_appartments = scrape_apartments()
    t_scrape_houses = scrape_houses()
    t_version_raw_data = version_raw_data_with_dvc()
    t_prep_analysis = prep_analysis()
    t_prep_training = prep_training()
    t_version_prepared_data = version_prepared_data_with_dvc()
    t_train_model = train_model(t_prep_training)
    t_version_model = version_model_with_dvc()

    chain([t_scrape_appartments, t_scrape_houses], t_version_raw_data, [t_prep_analysis, t_prep_training], t_version_prepared_data, t_train_model, t_version_model)
