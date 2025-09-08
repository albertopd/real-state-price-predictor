from typing import Annotated, Self
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError


from app.schemas.enums import (
    PropertyType,
    CommonSubtype,
    ApartmentSubtype,
    HouseSubtype,
    PropertySubtype,
    Province,
    EPCScore,
)
from app.schemas.validators import (
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

DEFAULT_APARTMENT_SUBTYPE = "APARTMENT"
DEFAULT_HOUSE_SUBTYPE = "HOUSE"


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
        PropertySubtype | None,
        Field(
            description=f"Property subtype. Must be one of these values: {', '.join(e.value for e in PropertySubtype)}"
        ),
    ] = None

    province: Annotated[
        Province | None,
        Field(
            description=f"Province where the property is located. Must be one of these values: {', '.join([p for p in Province])}"
        ),
    ] = None

    postal_code: Annotated[
        int | None,
        Field(
            description="Postal code of the property's location. Must correspond to the selected province and fall within valid Belgian postal code ranges."
        ),
    ] = None

    habitable_surface: Annotated[
        float,
        Field(
            gt=0,
            description="Livable surface area in square meters. Must be > 0.",
        ),
    ]

    terrace_surface: Annotated[
        float,
        Field(ge=0, description="Terrace surface area in m²."),
    ] = 0

    garden_surface: Annotated[
        float,
        Field(ge=0, description="Garden surface area in m²."),
    ] = 0

    bedroom_count: Annotated[
        int, Field(ge=0, description="Number of bedrooms.")
    ] = 0

    bathroom_count: Annotated[
        int, Field(ge=0, description="Number of bathrooms.")
    ] = 0

    toilet_count: Annotated[
        int, Field(ge=0, description="Number of toilets.")
    ] = 0

    epc_score: Annotated[
        EPCScore | None,
        Field(
            description=f"Energy performance classification. Must be one of these values: {', '.join([e.value for e in EPCScore])}",
        ),
    ] = None

    has_attic: bool = Field(default=False)
    has_garden: bool = Field(default=False)
    has_air_conditioning: bool = Field(default=False)
    has_armored_door: bool = Field(default=False)
    has_visiophone: bool = Field(default=False)
    has_terrace: bool = Field(default=False)
    has_office: bool = Field(default=False)
    has_swimming_pool: bool = Field(default=False)
    has_fireplace: bool = Field(default=False)
    has_basement: bool = Field(default=False)
    has_dressing_room: bool = Field(default=False)
    has_dining_room: bool = Field(default=False)
    has_lift: bool = Field(default=False)
    has_heat_pump: bool = Field(default=False)
    has_photovoltaic_panels: bool = Field(default=False)
    has_living_room: bool = Field(default=False)


    @model_validator(mode="before")
    @classmethod
    def infer_default_subtype(cls, data):
        """Infer default subtype before field validation."""
        if (
            isinstance(data, dict)
            and data.get("subtype") is None
            and data.get("type") is not None
        ):
            property_type = data.get("type")
            if property_type == PropertyType.APARTMENT:
                data["subtype"] = DEFAULT_APARTMENT_SUBTYPE
            elif property_type == PropertyType.HOUSE:
                data["subtype"] = DEFAULT_HOUSE_SUBTYPE
        return data

    @field_validator("subtype")
    @classmethod
    def validate_subtype(cls, v, info):
        """Validate subtype against property type."""
        if v is None:
            return v

        property_type = info.data.get("type")

        if property_type and v not in PROPERTY_TYPE_TO_SUBTYPES.get(property_type, []):
            allowed_subtypes = ", ".join(
                PROPERTY_TYPE_TO_SUBTYPES.get(property_type, [])
            )
            raise PydanticCustomError(
                "invalid_subtype",
                "Subtype '{subtype}' is not allowed for property type '{type}'. Allowed: {allowed}",
                {
                    "subtype": v.value,
                    "type": property_type.value,
                    "allowed": allowed_subtypes,
                },
            )

        return v

    @field_validator("postal_code")
    @classmethod
    def validate_post_code(cls, v, info):
        """Validate postal code against province if provided, otherwise against all provinces."""
        if v is None:
            return v

        if info.data.get("province") is not None:
            if not is_postal_code_valid_for_province(v, info.data["province"]):
                ranges = PROVINCE_POSTAL_CODE_RANGES.get(info.data["province"]) or []
                formatted_ranges = ", ".join(f"{r.start}-{r.stop - 1}" for r in ranges)
                raise PydanticCustomError(
                    "invalid_postal_code",
                    "Postal code {postal_code} is not valid for province {province}. Allowed ranges: {ranges}",
                    {
                        "postal_code": v,
                        "province": info.data["province"].value,
                        "ranges": formatted_ranges,
                    },
                )
        elif not is_postal_code_valid_in_any_province(v):
            formatted_ranges = ", ".join(
                ", ".join(f"{r.start}-{r.stop - 1}" for r in ranges) + f" ({prov})"
                for prov, ranges in PROVINCE_POSTAL_CODE_RANGES.items()
            )
            raise PydanticCustomError(
                "invalid_postal_code",
                "Postal code {postal_code} is not valid. Allowed ranges: {ranges}",
                {
                    "postal_code": v,
                    "ranges": formatted_ranges,
                },
            )

        return v

    @model_validator(mode="after")
    def infer_default_province(self) -> Self:
        """Infer province from postal code."""
        if self.province is None and self.postal_code is not None:
            for prov, ranges in PROVINCE_POSTAL_CODE_RANGES.items():
                if any(self.postal_code in r for r in ranges):
                    self.province = Province(prov)
                    break
        return self

    def to_ml_format(self) -> dict:
        """
        Convert snake_case API fields to camelCase expected by the ML model.
        """
        mapping = {
            "postal_code": "postCode",
            "habitable_surface": "habitableSurface",
            "terrace_surface": "terraceSurface",
            "garden_surface": "gardenSurface",
            "bedroom_count": "bedroomCount",
            "bathroom_count": "bathroomCount",
            "toilet_count": "toiletCount",
            "epc_score": "epcScore",
            "has_attic": "hasAttic",
            "has_garden": "hasGarden",
            "has_air_conditioning": "hasAirConditioning",
            "has_armored_door": "hasArmoredDoor",
            "has_visiophone": "hasVisiophone",
            "has_terrace": "hasTerrace",
            "has_office": "hasOffice",
            "has_swimming_pool": "hasSwimmingPool",
            "has_fireplace": "hasFireplace",
            "has_basement": "hasBasement",
            "has_dressing_room": "hasDressingRoom",
            "has_dining_room": "hasDiningRoom",
            "has_lift": "hasLift",
            "has_heat_pump": "hasHeatPump",
            "has_photovoltaic_panels": "hasPhotovoltaicPanels",
            "has_living_room": "hasLivingRoom",
        }

        data = self.model_dump()
        return {mapping.get(k, k): v for k, v in data.items()}