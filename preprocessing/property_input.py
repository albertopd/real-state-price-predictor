from pydantic import BaseModel
from typing import Optional


# TODO: Select what fields we have in our model and decided which one wil lbe optional
# TODO: Add some basic validation and metada (description of the fields)
class PropertyInput(BaseModel):
    habitableSurface: float
    type: str  # "APARTMENT" | "HOUSE"
    subtype: str
    province: str
    postCode: int
    epcScore: str
    bedroomCount: Optional[int] = 0
    bathroomCount: Optional[int] = 0
    toiletCount: Optional[int] = 0
    terraceSurface: Optional[float] = 0.0
    gardenSurface: Optional[float] = 0.0
    hasAttic: Optional[bool] = False
    hasGarden: Optional[bool] = False
    hasAirConditioning: Optional[bool] = False
    hasArmoredDoor: Optional[bool] = False
    hasVisiophone: Optional[bool] = False
    hasTerrace: Optional[bool] = False
    hasOffice: Optional[bool] = False
    hasSwimmingPool: Optional[bool] = False
    hasFireplace: Optional[bool] = False
    hasBasement: Optional[bool] = False
    hasDressingRoom: Optional[bool] = False
    hasDiningRoom: Optional[bool] = False
    hasLift: Optional[bool] = False
    hasHeatPump: Optional[bool] = False
    hasPhotovoltaicPanels: Optional[bool] = False
    hasLivingRoom: Optional[bool] = False
