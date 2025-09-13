"""Configuration management for ML pipeline."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class MLFlowConfig:
    """MLFlow configuration."""
    training_experiment_name: str = "real_estate_price_prediction_training"
    evaluation_experiment_name: str = "real_estate_price_prediction_evaluation"
    registered_model_name: str = "RealEstatePricePredictionModel"
    tracking_uri: str = os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://mlflow:5001" if os.path.exists("/.dockerenv") else "http://localhost:5001",
    )


@dataclass
class ModelConfig:
    """Model hyperparameters and configuration."""
    alpha: float = 0.1
    l1_ratio: float = 0.5
    random_state: int = 42
    test_size: float = 0.2


@dataclass
class PathConfig:
    """Path configuration."""
    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            repo_root = Path(__file__).resolve().parents[2]
        
        self.repo_root = repo_root
        self.data_dir = repo_root / "data"
        self.models_dir = repo_root / "ml_models"
        self.train_data = self.data_dir / "training" / "train_data.parquet"
        self.test_data = self.data_dir / "training" / "test_data.parquet"