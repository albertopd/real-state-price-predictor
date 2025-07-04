import pandas as pd
from preprocessing.property_input import PropertyInput
from utils.feature_engineering import add_lat_lon

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Manual label maps (used during training)
    type_map = {"APARTMENT": 1, "HOUSE": 2}
    subtype_map = {
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
        "PAVILION": 24
    }
    province_map = {
        "Brussels": 1,
        "Luxembourg": 2,
        "Antwerp": 3,
        "FlemishBrabant": 4, 
        "EastFlanders": 5,
        "WestFlanders": 6,
        "Liège": 7,
        "WalloonBrabant": 8,
        "Limburg": 9,
        "Namur": 10,
        "Hainaut": 11
    }
    epc_score_map = {"A+": 8, "A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}

    df["type_encoded"] = df["type"].map(type_map)
    df["subtype_encoded"] = df["subtype"].map(subtype_map)
    df["province_encoded"] = df["province"].map(province_map)
    df["epcScore_encoded"] = df["epcScore"].map(epc_score_map)

    # Keep postCode as-is or normalize it (depending on training)
    df["postCode"] = df["postCode"]

    # Binary encoding for boolean flags
    bool_fields = [col for col in df.columns if col.startswith("has") or col in [
        "hasAttic", "hasTerrace", "hasGarden", "hasLift", "hasOffice", "hasDiningRoom",
        "hasSwimmingPool", "hasFireplace", "hasPhotovoltaicPanels", "hasAirConditioning",
        "hasHeatPump", "hasBasement", "hasArmoredDoor", "hasVisiophone", "hasDressingRoom",
        "hasLivingRoom"
    ]]

    for col in bool_fields:
        df[f"{col}_encoded"] = df[col].astype(int)

    return df

def preprocess(data: PropertyInput) -> pd.DataFrame:
    # Convert to dict
    data_dict = data.model_dump()

    # Convert to single-row DataFrame
    df = pd.DataFrame([data_dict])

    df = add_lat_lon(df)
    df = encode_categorical_features(df)

    return df
