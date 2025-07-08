import os
import pandas as pd
import numpy as np
from preprocessing.property_input import PropertyInput


def encode_categorical_features(df: pd) -> pd:
    """
    Encode all categorical features in the real estate dataset using ordinal/label encoding
    """
    print("\n Starting categorical encoding...")
    df_encoded = df.copy()

    cols_to_drop = []

    # 1. PROVINCE ENCODING (Ordinal based on specified order)
    print("\n Encoding provinces...")
    province_mapping = {
        "Brussels": 1,
        "Luxembourg": 2,
        "Antwerp": 3,
        "FlemishBrabant": 4,
        "Flemish Brabant": 4,
        "EastFlanders": 5,
        "East Flanders": 5,
        "WestFlanders": 6,
        "West Flanders": 6,
        "Liège": 7,
        "WalloonBrabant": 8,
        "Walloon Brabant": 8,
        "Limburg": 9,
        "Namur": 10,
        "Hainaut": 11,
    }
    if "province" in df_encoded.columns:
        df_encoded["province_encoded"] = df_encoded["province"].map(province_mapping)
        print(
            f"Province encoding: {df_encoded['province_encoded'].value_counts().sort_index().to_dict()}"
        )
        cols_to_drop.append("province")

    # 2. TYPE ENCODING (Simple ordinal)
    print("\n Encoding property types...")
    type_mapping = {
        "APARTMENT": 1,
        "HOUSE": 2,
    }
    if "type" in df_encoded.columns:
        df_encoded["type_encoded"] = df_encoded["type"].map(type_mapping)
        print(f"Type encoding: {df_encoded['type_encoded'].value_counts().to_dict()}")
        cols_to_drop.append("type")

    # 3. SUBTYPE ENCODING
    print("\n Encoding property subtypes...")
    subtype_mapping = {
        "APARTMENT": 1,
        "HOUSE": 2,
        "FLAT_STUDIO": 3,
        "FLATSTUDIO": 3,  # Handle version without underscore
        "DUPLEX": 4,
        "PENTHOUSE": 5,
        "GROUND_FLOOR": 6,
        "GROUNDFLOOR": 6,  # Handle version without underscore
        "APARTMENT_BLOCK": 7,
        "APARTMENTBLOCK": 7,  # Handle version without underscore
        "MANSION": 8,
        "EXCEPTIONAL_PROPERTY": 9,
        "EXCEPTIONALPROPERTY": 9,  # Handle version without underscore
        "MIXED_USE_BUILDING": 10,
        "MIXEDUSEBUILDING": 10,  # Handle version without underscore
        "TRIPLEX": 11,
        "LOFT": 12,
        "VILLA": 13,
        "TOWN_HOUSE": 14,
        "TOWNHOUSE": 14,  # Handle version without underscore
        "CHALET": 15,
        "MANOR_HOUSE": 16,
        "MANORHOUSE": 16,  # Handle version without underscore
        "SERVICE_FLAT": 17,
        "SERVICEFLAT": 17,  # Handle version without underscore
        "KOT": 18,
        "FARMHOUSE": 19,
        "BUNGALOW": 20,
        "COUNTRY_COTTAGE": 21,
        "COUNTRYCOTTAGE": 21,  # Handle version without underscore
        "OTHER_PROPERTY": 22,
        "OTHERPROPERTY": 22,  # Handle version without underscore
        "CASTLE": 23,
        "PAVILION": 24,
    }
    if "subtype" in df_encoded.columns:
        df_encoded["subtype_encoded"] = df_encoded["subtype"].map(subtype_mapping)
        print(
            f"Subtype encoding: {df_encoded['subtype_encoded'].value_counts().to_dict()}"
        )
        cols_to_drop.append("subtype")

    # 4. EPC SCORE ENCODING (Energy Performance Certificate - ordinal)
    print("\n Encoding EPC scores...")
    if "epcScore" in df_encoded.columns:
        epc_mapping = {"A+": 8, "A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}
        df_encoded["epcScore_encoded"] = df_encoded["epcScore"].map(epc_mapping)
        print(
            f"EPC encoding: {df_encoded['epcScore_encoded'].value_counts().sort_index().to_dict()}"
        )
        cols_to_drop.append("epcScore")

    # 5. BOOLEAN FEATURES - Convert True/False to 1/0 (updated list)
    print("\n Encoding boolean features...")
    boolean_columns = [
        "hasAttic",
        "hasGarden",
        "hasAirConditioning",
        "hasArmoredDoor",
        "hasVisiophone",
        "hasTerrace",
        "hasOffice",
        "hasSwimmingPool",
        "hasFireplace",
        "hasBasement",
        "hasDressingRoom",
        "hasDiningRoom",
        "hasLift",
        "hasHeatPump",
        "hasPhotovoltaicPanels",
        "hasLivingRoom",
    ]

    for col in boolean_columns:
        if col in df_encoded.columns:
            df_encoded[f"{col}_encoded"] = df_encoded[col].map(
                {True: 1, False: 0, np.nan: 0}
            )
            print(
                f"{col} encoded: {df_encoded[f'{col}_encoded'].value_counts(dropna=False).to_dict()}"
            )
            cols_to_drop.append(col)

    df_encoded = df_encoded.drop(columns=cols_to_drop)

    return df_encoded


def add_lat_lon(df: pd.DataFrame) -> pd.DataFrame:
    df["postCode"] = df["postCode"].astype(str)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(
        base_dir, "estefania_drafts", "data", "georef-belgium-postal-codes.csv"
    )  # have to check this after
    geo_df = pd.read_csv(data_path, delimiter=";")
    geo_df[["lat", "lon"]] = geo_df["Geo Point"].str.split(",", expand=True)
    geo_df["lat"] = geo_df["lat"].astype(float)
    geo_df["lon"] = geo_df["lon"].astype(float)
    geo_df["postCode"] = geo_df["Post code"].astype(str)
    df = df.merge(geo_df[["postCode", "lat", "lon"]], on="postCode", how="left")
    return df


def preprocess(data_dict: dict) -> pd.DataFrame:
    # Convert to dict

    # Convert to single-row DataFrame
    df = pd.DataFrame([data_dict])
    df_coded = encode_categorical_features(df)

    # TODO: Add latitude, longitude features
    df_coded = add_lat_lon(df_coded)
    return df_coded
