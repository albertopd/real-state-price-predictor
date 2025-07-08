from enum import Enum

class PropertyType(str, Enum):
    """
    Enumeration of property types.
    """
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"

class CommonSubtype(str, Enum):
    EXCEPTIONAL_PROPERTY = "EXCEPTIONAL_PROPERTY"
    MIXED_USE_BUILDING = "MIXED_USE_BUILDING"
    OTHER_PROPERTY = "OTHER_PROPERTY"

class ApartmentSubtype(str, Enum):
    APARTMENT = "APARTMENT"
    FLAT_STUDIO = "FLAT_STUDIO"
    DUPLEX = "DUPLEX"
    PENTHOUSE = "PENTHOUSE"
    GROUND_FLOOR = "GROUND_FLOOR"
    APARTMENT_BLOCK = "APARTMENT_BLOCK"
    TRIPLEX = "TRIPLEX"
    LOFT = "LOFT"
    SERVICE_FLAT = "SERVICE_FLAT"
    KOT = "KOT"

class HouseSubtype(str, Enum):
    HOUSE = "HOUSE"
    VILLA = "VILLA"
    TOWN_HOUSE = "TOWN_HOUSE"
    CHALET = "CHALET"
    MANOR_HOUSE = "MANOR_HOUSE"
    MANSION = "MANSION"
    FARMHOUSE = "FARMHOUSE"
    BUNGALOW = "BUNGALOW"
    COUNTRY_COTTAGE = "COUNTRY_COTTAGE"
    CASTLE = "CASTLE"
    PAVILION = "PAVILION"

# Merge all enum values into one dictionary (no duplicates)
def _collect_property_subtypes():
    seen = {}
    for enum_cls in [CommonSubtype, ApartmentSubtype, HouseSubtype]:
        for item in enum_cls:
            if item.name not in seen:
                seen[item.name] = item.value
    return seen

# Dynamically create PropertySubtype Enum from merged values
PropertySubtype = Enum("PropertySubtype", _collect_property_subtypes(), type=str)

class Province(str, Enum):
    """
    Enumeration of Belgian provinces.
    """
    BRUSSELS = "Brussels"
    LUXEMBOURG = "Luxembourg"
    ANTWERP = "Antwerp"
    FLEMISH_BRABANT = "FlemishBrabant"
    EAST_FLANDERS = "EastFlanders"
    WEST_FLANDERS = "WestFlanders"
    LIEGE = "Liège"
    WALLOON_BRABANT = "WalloonBrabant"
    LIMBURG = "Limburg"
    NAMUR = "Namur"
    HAINAUT = "Hainaut"

class EPCScore(str, Enum):
    """
    Enumeration of EPC (Energy Performance Certificate) scores.
    """
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
