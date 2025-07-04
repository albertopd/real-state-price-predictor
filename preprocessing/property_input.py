from pydantic import BaseModel

# TODO: Select what fields we have in our model and decided which one wil lbe optional
# TODO: Add some basic validation and metada (description of the fields)
class PropertyInput(BaseModel):
    habitableSurface: float
    type: str   #"APARTMENT" | "HOUSE"
    subtype: str
    province: str
    postCode: int
    epcScore: str
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