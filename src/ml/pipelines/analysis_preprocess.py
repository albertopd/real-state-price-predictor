from __future__ import annotations
from pathlib import Path
import pandas as pd

def build_analysis_dataset(raw_dir: Path, out_file: Path) -> None:
    # Read all parquet files under raw
    apts = list((raw_dir / "apartments").glob("*.parquet"))
    houses = list((raw_dir / "houses").glob("*.parquet"))
    frames = []
    for p in apts + houses:
        frames.append(pd.read_parquet(p))
    if not frames:
        raise RuntimeError("No raw data found to build analysis dataset")

    df = pd.concat(frames, ignore_index=True)

    # Analysis-focused cleaning: keep human-friendly fields, derive a few KPIs
    df["price_per_m2"] = df["price_eur"] / df["living_area_m2"]
    # Simple winsorization to reduce outliers impact on dashboard
    df["price_per_m2"] = df["price_per_m2"].clip(lower=df["price_per_m2"].quantile(0.01),
                                                 upper=df["price_per_m2"].quantile(0.99))

    # Optional: map postal_code to province here if available
    # df["province"] = df["postal_code"].map(...)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_file, index=False)
