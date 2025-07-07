from pydantic import BaseModel, Field
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
    bedroomCount: Optional[int] = Field(default=0)
    bathroomCount: Optional[int] = Field(default=0)
    toiletCount: Optional[int] = Field(default=0)
    terraceSurface: Optional[float] = Field(default=0.0)
    gardenSurface: Optional[float] = Field(default=0.0)
    hasAttic: Optional[bool] = Field(default=False)
    hasGarden: Optional[bool] = Field(default=False)
    hasAirConditioning: Optional[bool] = Field(default=False)
    hasArmoredDoor: Optional[bool] = Field(default=False)
    hasVisiophone: Optional[bool] = Field(default=False)
    hasTerrace: Optional[bool] = Field(default=False)
    hasOffice: Optional[bool] = Field(default=False)
    hasSwimmingPool: Optional[bool] = Field(default=False)
    hasFireplace: Optional[bool] = Field(default=False)
    hasBasement: Optional[bool] = Field(default=False)
    hasDressingRoom: Optional[bool] = Field(default=False)
    hasDiningRoom: Optional[bool] = Field(default=False)
    hasLift: Optional[bool] = Field(default=False)
    hasHeatPump: Optional[bool] = Field(default=False)
    hasPhotovoltaicPanels: Optional[bool] = Field(default=False)
    hasLivingRoom: Optional[bool] = Field(default=False)
