from pathlib import Path


def extract_experiment_run_name(model_path: Path) -> str:
    """
    Convert filename like '20250911_130413_elasticnet.pkl'
    into experiment run name 'elasticnet_20250911_130413'
    """
    stem = model_path.stem
    parts = stem.split("_", 2)
    if len(parts) == 3:
        ts_date, ts_time, model_name = parts
        return f"{model_name}_{ts_date}_{ts_time}"
    return stem  # fallback: just use the filename stem