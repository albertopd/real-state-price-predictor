from preprocessing.property_input import PropertyInput

def preprocess(data: PropertyInput) -> dict:

    province_mapping = {
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
    "Hainaut": 11,}
    
    subtype_mapping = {
    "APARTMENT": 1,
    "HOUSE": 2,
    "FLAT_STUDIO": 3,
    "DUPLEX": 4,
    "PENTHOUSE": 5,
    "GROUND_FLOOR": 6,
    "APARTMENT_BLOCK": 7,
    "MANSION": 8,
    "EXCEPTIONAL_PROPERTY": 9,
    "MIXED_USE_BUILDING": 10,
    "TRIPLEX": 11,
    "LOFT": 12,
    "VILLA": 13,
    "TOWN_HOUSE": 14,
    "CHALET": 15,
    "MANOR_HOUSE": 16,
    "SERVICE_FLAT": 17,
    "KOT": 18,
    "FARMHOUSE": 19,
    "BUNGALOW": 20,
    "COUNTRY_COTTAGE": 21,
    "OTHER_PROPERTY": 22,
    "CASTLE": 23,
    "PAVILION": 24,}
    
    epc_mapping = {
    "A+": 8,
    "A": 7,
    "B": 6,
    "C": 5,
    "D": 4,
    "E": 3,
    "F": 2,
    "G": 1,}

    preprocessed_data = data.model_dump()

    preprocessed_data["province_encoded"] = province_mapping.get(preprocessed_data["province"], 0)
    preprocessed_data["subtype_encoded"] = subtype_mapping.get(preprocessed_data["subtype"], 0)
    preprocessed_data["epc_encoded"] = epc_mapping.get(preprocessed_data["epc"], 0)

    # Optional: drop or convert fields
    preprocessed_data["postCode"] = str(preprocessed_data["postCode"])
    preprocessed_data["has_garden"] = int(preprocessed_data["has_garden"])
    preprocessed_data["has_terrace"] = int(preprocessed_data["has_terrace"])

    return preprocessed_data