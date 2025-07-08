from preprocessing.property_input import PropertyInput
import os
import pandas as pd

class PropertyPreprocessor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(base_dir, "data", "georef-belgium-postal-codes.csv")
        self.geo_df = self.load_geodata()
        
    def load_geodata(self):
         base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
         data_path = os.path.join(base_dir, "data", "georef-belgium-postal-codes.csv")
         geo_df = pd.read_csv(data_path, delimiter=";")
         geo_df[["lat", "lon"]] = geo_df["Geo Point"].str.split(",", expand=True)
         geo_df["lat"] = geo_df["lat"].astype(float)
         geo_df["lon"] = geo_df["lon"].astype(float)
         geo_df["postCode"] = geo_df["Post code"].astype(str)
         grouped_df = geo_df.groupby("postCode")[["lat", "lon"]].mean()
         return grouped_df
     
    def postcode_lookup_latlon(self, postcode: str):
        if postcode in self.geo_df.index:
            lat, lon = self.geo_df.loc[postcode]
            print(f"from {postcode}: lat: {lat}, lon: {lon}")
            return lat, lon
        else:
            print(f"postcode {postcode} not found.")
            raise ValueError(f"Invalid input: postcode {postcode} not found.")
    
    def get_EPC_encoded(self, epc_score: str) -> int:
        epc_mapping = {
        "A+": 8,
        "A": 7,
        "B": 6,
        "C": 5,
        "D": 4,
        "E": 3,
        "F": 2,
        "G": 1,}
        clean_epc_score = epc_score.strip().upper()
        if clean_epc_score not in epc_mapping:
            raise ValueError(f"Unrecognized EPC score: '{clean_epc_score}'")
        epcScore_encoded = epc_mapping.get(clean_epc_score, 0)
        return epcScore_encoded
    
    def get_subtype_encoded(self, subtype: str) -> int:
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
        clean_subtype = subtype.strip().upper().replace(" ", "_")
        if clean_subtype not in subtype_mapping:
            raise ValueError(f"Unrecognized property subtype: '{clean_subtype}'")
        subtype_encoded = subtype_mapping.get(clean_subtype, 0)
        return subtype_encoded
    
    def get_province_encoded(self, province: str, postcode:str) -> int:
        province_mapping = {
        "BRUSSELS": 1,
        "LUXEMBOURG": 2,
        "ANTWERP": 3,
        "FLEMISH_BRABANT": 4,
        "EAST_FLANDERS": 5,
        "WEST_FLANDERS": 6,
        "LIÈGE": 7,
        "WALLOON_BRABANT": 8,
        "LIMBURG": 9,
        "NAMUR": 10,
        "HAINAUT": 11,
    }
        clean_province = province.strip().upper().replace(" ", "_")
        if clean_province not in province_mapping:
            raise ValueError(f"Unrecognized province: '{clean_province}'")
        province_from_postcode = self.check_province_from_postcode(postcode)
        if province_from_postcode != clean_province:
            raise ValueError(f"{postcode} is not in {clean_province}")
        province_encoded = province_mapping.get(clean_province, 0)
        return province_encoded
    
    def get_type_encoded(self, property_type: str) -> int:
        type_mapping = {
        "APARTMENT": 1,
        "HOUSE": 2,}
        clean_type = property_type.strip().upper()
        if clean_type not in type_mapping:
            raise ValueError(f"Unrecognized property type: '{clean_type}'")
        type_encoded = type_mapping.get(clean_type, 0)
        return type_encoded
    
    def check_province_from_postcode(self, postcode: str) -> str:
        postcode = int(postcode)
        if 1000 <= postcode <= 1299:
            return "BRUSSELS"
        elif 1300 <= postcode <= 1499:
            return "WALLOON_BRABANT"
        elif (1500 <= postcode <= 1999) or (3000 <= postcode <= 3499):
            return "FLEMISH_BRABANT"
        elif 2000 <= postcode <= 2999:
            return "ANTWERP"
        elif 3500 <= postcode <= 3999:
            return "LIMBURG"
        elif 4000 <= postcode <= 4999:
            return "LIÈGE"
        elif 5000 <= postcode <= 5999:
            return "NAMUR"
        elif (6000 <= postcode <= 6599) or (7000 <= postcode <= 7999):
            return "HAINAUT"
        elif 6600 <= postcode <= 6999:
            return "LUXEMBOURG"
        elif 8000 <= postcode <= 8999:
            return "WEST_FLANDERS"
        elif 9000 <= postcode <= 9999:
            return "EAST_FLANDERS"
        else:
            raise ValueError(f"Invalid Belgian postcode: {postcode}")
    
    def preprocess(self, data:PropertyInput ) -> dict:
        preprocessed_data = data.model_dump()
        # get lat and lon
        preprocessed_data["postCode"] = str(preprocessed_data["postCode"])
        lat, lon = self.postcode_lookup_latlon(preprocessed_data["postCode"])
        preprocessed_data["lat"] = lat
        preprocessed_data["lon"] = lon
        
        # Encode categorical variables
        preprocessed_data["province_encoded"] = self.get_province_encoded(
        preprocessed_data["province"],preprocessed_data["postCode"])
        preprocessed_data["type_encoded"] = self.get_type_encoded(preprocessed_data["type"])
        preprocessed_data["subtype_encoded"] = self.get_subtype_encoded(preprocessed_data["subtype"])
        preprocessed_data["epcScore_encoded"] = self.get_EPC_encoded(preprocessed_data["epcScore"])
        
        boolean_fields = [
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
        "hasLivingRoom",]
        
        for field in boolean_fields:
            if field in preprocessed_data:
                preprocessed_data[f"{field}_encoded"] = int(preprocessed_data[field])
        int_fields = ["bedroomCount", "bathroomCount", "toiletCount"]
        
        for field in int_fields:
            if field in preprocessed_data:
                preprocessed_data[field] = int(preprocessed_data[field])
        float_fields = ["habitableSurface", "terraceSurface", "gardenSurface"]
        for field in float_fields:
            if field in preprocessed_data:
                preprocessed_data[field] = float(preprocessed_data[field])
        
        return preprocessed_data

