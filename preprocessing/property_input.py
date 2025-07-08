from pydantic import BaseModel, Field
from typing import Optional, Annotated


# TODO: Select what fields we have in our model and decided which one wil lbe optional
# TODO: Add some basic validation and metada (description of the fields)
class PropertyInput(BaseModel):
    habitableSurface: Annotated[
        float, Field(gt=0, description="Must be a float: greater than zero")
    ]
    type: Annotated[str, Field(description='Must be a string: "APARTMENT" or "HOUSE"')]
    subtype: Annotated[str, Field(description="Must be a string")]
    province: Annotated[str, Field(description="Must be a province of Belgium")]
    postCode: Annotated[int, Field(description="Must be a postal code of Belgium")]
    epcScore: Annotated[
        str | None, Field(description="Must be a value between A+ and G")
    ] = "C"
    bedroomCount: Annotated[
        int, Field(ge=0, description="Number of bedrooms must be ≥ 0.")
    ] = 3
    bathroomCount: Annotated[
        int, Field(ge=0, description="Number of bedrooms. Must be ≥ 0.")
    ] = 1
    toiletCount: Annotated[
        int | None, Field(ge=0, description="Number of toilets. Must be ≥ 0.")
    ] = 2
    terraceSurface: Annotated[
        float | None, Field(ge=0, description="Must be a float ≥ zero")
    ] = 0
    gardenSurface: Annotated[
        float | None, Field(ge=0, description="Must be a float ≥ zero")
    ] = 0
    hasAttic: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has an attic. If not, default value will be False",
        ),
    ] = False
    hasGarden: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has a garden. If not, default value will be False",
        ),
    ] = False
    hasAirConditioning: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has air condtioning installed. If not, default value will be False",
        ),
    ] = False
    hasArmoredDoor: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has armored door. If not, default value will be False",
        ),
    ] = False
    hasVisiophone: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has visiophone. If not, default value will be False",
        ),
    ] = False
    hasTerrace: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has terrace. If not, default value will be False",
        ),
    ] = False
    hasOffice: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has office. If not, default value will be False",
        ),
    ] = False
    hasSwimmingPool: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has swimming pool. If not, default value will be False",
        ),
    ] = False
    hasFireplace: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has fireplace. If not, default value will be False",
        ),
    ] = False
    hasBasement: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has basement. If not, default value will be False",
        ),
    ] = False
    hasDressingRoom: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has dresssing room. If not, default value will be False",
        ),
    ] = False
    hasDiningRoom: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has dining room. If not, default value will be False",
        ),
    ] = False
    hasLift: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has lift. If not, default value will be False",
        ),
    ] = False
    hasHeatPump: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has heat pump. If not, default value will be False",
        ),
    ] = False
    hasPhotovoltaicPanels: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has photvoltaic panels. If not, default value will be False",
        ),
    ] = False
    hasLivingRoom: Annotated[
        bool | None,
        Field(
            default=False,
            description="Property has living room. If not, default value will be False",
        ),
    ] = False
