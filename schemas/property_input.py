from typing import Annotated
from pydantic import BaseModel, Field, model_validator

from schemas.enums import (
    PropertyType,
    CommonSubtype,
    ApartmentSubtype,
    HouseSubtype,
    PropertySubtype,
    Province,
    EPCScore,
)
from utils.validators import (
    PROVINCE_POSTAL_CODE_RANGES,
    is_postal_code_valid_in_any_province,
    is_postal_code_valid_for_province,
)


# Mapping of property types to their allowed subtypes, including both specific and common subtypes.
PROPERTY_TYPE_TO_SUBTYPES = {
    PropertyType.APARTMENT: {
        *(item.value for item in ApartmentSubtype),
        *(item.value for item in CommonSubtype),
    },
    PropertyType.HOUSE: {
        *(item.value for item in HouseSubtype),
        *(item.value for item in CommonSubtype),
    },
}


class PropertyInput(BaseModel):
    """
    Schema for representing detailed information about a property listing. This includes
    structural attributes (e.g. surface areas, rooms), location data (e.g. province, postal code),
    and amenities (e.g. lift, terrace, fireplace).
    """

    type: Annotated[
        PropertyType,
        Field(
            description=f"Property type. Must be one of these values: {', '.join([pt for pt in PropertyType])}"
        ),
    ]

    subtype: Annotated[
        CommonSubtype | ApartmentSubtype | HouseSubtype | None,
        Field(
            description=f"Property subtype. Must be one of these values: {', '.join([pst for pst in PropertySubtype])}"
        ),
    ] = None

    province: Annotated[
        Province | None,
        Field(
            description=f"Province where the property is located. Must be one of these values: {', '.join([p for p in Province])}"
        ),
    ] = None

    postCode: Annotated[
        int | None,
        Field(
            description="Postal code of the neighbourhood. Must match province if provided and be within valid Belgian postal code ranges."
        ),
    ] = None

    habitableSurface: Annotated[
        float,
        Field(gt=0, description="Livable surface area in square meters. Must be > 0."),
    ]

    terraceSurface: Annotated[
        float,
        Field(ge=0, description="Terrace surface area in square meters. Must be ≥ 0."),
    ] = 0

    gardenSurface: Annotated[
        float,
        Field(ge=0, description="Garden surface area in square meters. Must be ≥ 0."),
    ] = 0

    bedroomCount: Annotated[
        int, Field(ge=0, description="Number of bedrooms. Must be ≥ 0.")
    ] = 0

    bathroomCount: Annotated[
        int, Field(ge=0, description="Number of bathrooms. Must be ≥ 0.")
    ] = 0

    toiletCount: Annotated[
        int, Field(ge=0, description="Number of toilets. Must be ≥ 0.")
    ] = 0

    epcScore: Annotated[
        EPCScore | None,
        Field(
            description=f"Energy performance classification. Must be one of these values: {', '.join([e.value for e in EPCScore])}"
        ),
    ] = None

    hasAttic: Annotated[
        bool,
        Field(
            default=False, description="Indicates whether the property has an attic."
        ),
    ] = False

    hasGarden: Annotated[
        bool,
        Field(
            default=False, description="Indicates whether the property has a garden."
        ),
    ] = False

    hasAirConditioning: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has air conditioning.",
        ),
    ] = False

    hasArmoredDoor: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has an armored door.",
        ),
    ] = False

    hasVisiophone: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a video intercom (visiophone).",
        ),
    ] = False

    hasTerrace: Annotated[
        bool,
        Field(
            default=False, description="Indicates whether the property has a terrace."
        ),
    ] = False

    hasOffice: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a dedicated office space.",
        ),
    ] = False

    hasSwimmingPool: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a swimming pool.",
        ),
    ] = False

    hasFireplace: Annotated[
        bool,
        Field(
            default=False, description="Indicates whether the property has a fireplace."
        ),
    ] = False

    hasBasement: Annotated[
        bool,
        Field(
            default=False, description="Indicates whether the property has a basement."
        ),
    ] = False

    hasDressingRoom: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a dressing room.",
        ),
    ] = False

    hasDiningRoom: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a dining room.",
        ),
    ] = False

    hasLift: Annotated[
        bool,
        Field(
            default=False, description="Indicates whether the property has an elevator."
        ),
    ] = False

    hasHeatPump: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a heat pump system.",
        ),
    ] = False

    hasPhotovoltaicPanels: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has solar photovoltaic panels.",
        ),
    ] = False

    hasLivingRoom: Annotated[
        bool,
        Field(
            default=False,
            description="Indicates whether the property has a living room.",
        ),
    ] = False

    @model_validator(mode="after")
    def validate_subtype_or_infere(self) -> "PropertyInput":
        """
        Validates or infers the subtype based on the property type.

        - If `subtype` is not provided (`None`), it assigns a default based on `type`:
            - `ApartmentSubtype.APARTMENT` for type `APARTMENT`
            - `HouseSubtype.HOUSE` for type `HOUSE`
        - If `subtype` is provided, it ensures the subtype is valid for the given property type.
        Raises a ValueError if the subtype does not belong to the allowed set.

        Returns:
            PropertyInput: The validated or updated instance.

        Raises:
            ValueError: If an invalid subtype is provided for the given property type.
        """
        if self.subtype is None:
            self.subtype = (
                ApartmentSubtype.APARTMENT
                if self.type == PropertyType.APARTMENT
                else HouseSubtype.HOUSE
            )
        elif self.subtype not in PROPERTY_TYPE_TO_SUBTYPES[self.type]:
            raise ValueError(
                f"Subtype '{self.subtype}' is not valid for property type {self.type.value}. "
                f"Must be one of these values: {PROPERTY_TYPE_TO_SUBTYPES[self.type]}"
            )

        return self

    @model_validator(mode="after")
    def validate_postalcode_infer_province(self) -> "PropertyInput":
        """
        Validates postal code and infers the province if not provided.
        """
        if self.postCode is not None:
            if self.province is not None:
                if not is_postal_code_valid_for_province(self.postCode, self.province):
                    ranges = PROVINCE_POSTAL_CODE_RANGES.get(self.province) or []
                    formatted_ranges = ", ".join(
                        f"{r.start}-{r.stop - 1}" for r in ranges
                    )
                    raise ValueError(
                        f"Postal code {self.postCode} is not valid for province {self.province.value}. "
                        f"Must be in one of these ranges: {formatted_ranges}"
                    )
            else:
                if not is_postal_code_valid_in_any_province(self.postCode):
                    formatted_ranges = ", ".join(
                        ", ".join(f"{r.start}-{r.stop - 1}" for r in ranges)
                        + f" ({prov})"
                        for prov, ranges in PROVINCE_POSTAL_CODE_RANGES.items()
                    )
                    raise ValueError(
                        f"Invalid postal code {self.postCode}. Must be in one of these ranges: {formatted_ranges}"
                    )

                # Infer province from postal code
                for prov, ranges in PROVINCE_POSTAL_CODE_RANGES.items():
                    if any(self.postCode in r for r in ranges):
                        self.province = Province(prov)
                        break
        return self
