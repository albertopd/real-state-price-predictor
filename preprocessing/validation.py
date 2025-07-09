import os
import pandas as pd


def get_belgian_postcodes() -> list["str"]:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(
        base_dir, "estefania_drafts", "data", "georef-belgium-postal-codes.csv"
    )
    geo_df = pd.read_csv(data_path, delimiter=";")
    postCodes = [int(code) for code in list(geo_df["Post code"])]

    return postCodes
