from pydantic import BaseModel, Field
from preprocessing.enums import PropertyType, PropertySubtype, Province, EPCScore
from utils.validators import case_insensitive_enum_validator

# TODO: Add some basic validation and metada (description of the fields)
class PropertyInput(BaseModel):
    habitableSurface: float = Field(
        title="Habitable surface",
        description="The habitable surface of the property (must be me greater than 0)",
        gt=0,
    )

    type: PropertyType
    subtype: PropertySubtype
    province: Province
    epcScore: EPCScore

    # Attach validators dynamically
    _validate_property_type = case_insensitive_enum_validator("type", PropertyType)
    _validate_subtype = case_insensitive_enum_validator("subtype", PropertySubtype)
    _validate_province = case_insensitive_enum_validator("province", Province)
    _validate_epc_score = case_insensitive_enum_validator("epcScore", EPCScore)

    postCode: int
    bedroomCount: int = 0
    bathroomCount: int = 0
    toiletCount: int = 0
    terraceSurface: float = 0.0
    gardenSurface: float = 0.0
    hasAttic: bool = False
    hasGarden: bool = False
    hasAirConditioning: bool = False
    hasArmoredDoor: bool = False
    hasVisiophone: bool = False
    hasTerrace: bool = False
    hasOffice: bool = False
    hasSwimmingPool: bool = False
    hasFireplace: bool = False
    hasBasement: bool = False
    hasDressingRoom: bool = False
    hasDiningRoom: bool = False
    hasLift: bool = False
    hasHeatPump: bool = False
    hasPhotovoltaicPanels: bool = False
    hasLivingRoom: bool = False
