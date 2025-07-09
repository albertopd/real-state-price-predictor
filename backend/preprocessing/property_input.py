from pydantic import BaseModel, Field
from typing import Optional


class PropertyInput(BaseModel):
    habitableSurface: float = Field(description="Total habitable area in m²")
    type: str = Field(description="Main property type: APARTMENT or HOUSE")
    subtype: str = Field(description="Detailed subtype (e.g. VILLA, LOFT, etc.)")
    province: str = Field(description="Belgian province (e.g. Antwerp, Brussels)")
    postCode: int = Field(description="Postal code of the property")
    epcScore: str = Field(description="EPC energy label, e.g. A+, B, G")
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


class CompareInput(BaseModel):
    actual_price: float
    property: PropertyInput
