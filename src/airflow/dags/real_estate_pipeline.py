from __future__ import annotations

import os
import sys
import pandas as pd
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any
from airflow import DAG
from airflow.decorators import task
from ml.training.train_regression import train_and_log_model
from ml.pipelines.analysis_preprocess import build_analysis_dataset
from ml.pipelines.training_preprocess import build_training_datasets
from scrapers.scrape_apartments import run as scrape_apartments_run
from scrapers.scrape_houses import run as scrape_houses_run


# Make project root importable for tasks
REPO_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[3]))
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

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
        print("Scraping apartments...")
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_DIR / "apartments" / f"apartments_{datetime.now(timezone.utc).date()}.parquet"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rows = scrape_apartments_run()
        pd.DataFrame(rows).to_parquet(out_path)
        print(f"Scraped apartments saved to {out_path}")
        return str(out_path)

    @task
    def scrape_houses():
        print("Scraping houses...")
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_DIR / "houses" / f"houses_{datetime.now(timezone.utc).date()}.parquet"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rows = scrape_houses_run()
        pd.DataFrame(rows).to_parquet(out_path)
        print(f"Scraped houses saved to {out_path}")
        return str(out_path)

    @task
    def prep_analysis_data():
        print("Preparing analysis data...")
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        out_file = ANALYSIS_DIR / "listings.parquet"
        build_analysis_dataset(RAW_DIR, out_file)
        print(f"Analysis dataset saved to {out_file}")
        return str(out_file)

    @task
    def prep_training_data():
        print("Preparing training data...")
        TRAINING_DIR.mkdir(parents=True, exist_ok=True)
        build_training_datasets(RAW_DIR, TRAINING_DIR)
        out_file = TRAINING_DIR / "train_data.parquet"
        print(f"Training dataset saved to {out_file}")
        return str(out_file)

    @task
    def train_model(train_path: Any):
        print("Training model...")
        if not train_path or not Path(train_path).exists():
            raise RuntimeError("Training data not found, cannot train model")
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        model_path = train_and_log_model(train_path, MODELS_DIR)
        print(f"Model trained and saved to {model_path}")
        return model_path


    # Define tasks and dependencies
    t_scrape_apartments = scrape_apartments()
    t_scrape_houses = scrape_houses()
    t_prep_analysis_data = prep_analysis_data()
    t_prep_training_data = prep_training_data()
    t_train_model = train_model(t_prep_training_data)

    # Both analysis and training prep depend on both scrapers
    [t_scrape_apartments, t_scrape_houses] >> t_prep_analysis_data
    [t_scrape_apartments, t_scrape_houses] >> t_prep_training_data

    # Training model depends only on training prep
    t_prep_training_data >> t_train_model
