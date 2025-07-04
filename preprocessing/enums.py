from enum import Enum

class CaseInsensitiveEnum(str, Enum):
    """
    Base Enum class that supports case-insensitive lookup from strings.

    Methods
    -------
    from_str(value: str) -> Enum member
        Converts a string to the corresponding Enum member,
        ignoring case differences.

    Raises
    ------
    TypeError
        If the input value is not a string.
    ValueError
        If the input string does not match any Enum member.
    """

    @classmethod
    def from_str(cls, value: str):
        """
        Convert a string to the corresponding Enum member, case-insensitively.

        Parameters
        ----------
        value : str
            String representation of the enum member (case-insensitive).

        Returns
        -------
        Enum member
            Corresponding Enum member matching the input string.

        Raises
        ------
        TypeError
            If value is not a string.
        ValueError
            If value does not match any Enum member.
        """
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        for item in cls:
            if item.value.lower() == value.lower():
                return item
        valid_values = [e.value for e in cls]
        raise ValueError(f"Invalid value '{value}'. Must be one of: {valid_values}")

class PropertyType(CaseInsensitiveEnum):
    """
    Enumeration of property types.
    """
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"

class PropertySubtype(CaseInsensitiveEnum):
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

class Province(CaseInsensitiveEnum):
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

class EPCScore(CaseInsensitiveEnum):
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
