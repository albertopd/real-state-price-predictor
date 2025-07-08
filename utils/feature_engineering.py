import os
import pandas as pd

def add_lat_lon(df: pd.DataFrame) -> pd.DataFrame:
    df["postCode"] = df["postCode"].astype(str)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "georef-belgium-postal-codes.csv")
    geo_df = pd.read_csv(data_path, delimiter=";")
    geo_df[["lat", "lon"]] = geo_df["Geo Point"].str.split(",", expand=True)
    geo_df["lat"] = geo_df["lat"].astype(float)
    geo_df["lon"] = geo_df["lon"].astype(float)
    geo_df["postCode"] = geo_df["Post code"].astype(str)
    geo_df_unique = geo_df.drop_duplicates(subset=["postCode"])
    df = df.merge(geo_df_unique[["postCode", "lat", "lon"]], on="postCode", how="left")
    return df
