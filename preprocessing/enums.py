from enum import Enum

class PropertyType(str, Enum):
    """
    Enumeration of property types.
    """
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"

class PropertySubtype(str, Enum):
    """
    Enumeration of property subtypes, covering various detailed categories.
    """
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    FLAT_STUDIO = "FLAT_STUDIO"
    DUPLEX = "DUPLEX"
    PENTHOUSE = "PENTHOUSE"
    GROUND_FLOOR = "GROUND_FLOOR"
    APARTMENT_BLOCK = "APARTMENT_BLOCK"
    MANSION = "MANSION"
    EXCEPTIONAL_PROPERTY = "EXCEPTIONAL_PROPERTY"
    MIXED_USE_BUILDING = "MIXED_USE_BUILDING"
    TRIPLEX = "TRIPLEX"
    LOFT = "LOFT"
    VILLA = "VILLA"
    TOWN_HOUSE = "TOWN_HOUSE"
    CHALET = "CHALET"
    MANOR_HOUSE = "MANOR_HOUSE"
    SERVICE_FLAT = "SERVICE_FLAT"
    KOT = "KOT"
    FARMHOUSE = "FARMHOUSE"
    BUNGALOW = "BUNGALOW"
    COUNTRY_COTTAGE = "COUNTRY_COTTAGE"
    OTHER_PROPERTY = "OTHER_PROPERTY"
    CASTLE = "CASTLE"
    PAVILION = "PAVILION"

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
