from typing import Annotated
from pydantic import BaseModel, Field, field_validator
from preprocessing.enums import PropertyType, PropertySubtype, Province, EPCScore
from utils.validators import PROVINCE_POSTAL_CODE_RANGES, is_postal_code_valid_in_any_province, is_postal_code_valid_for_province

class PropertyInput(BaseModel):
    type: Annotated[
        PropertyType,
        Field(description=f'Property type. Must be one of these values: {", ".join([pt for pt in PropertyType])}')
    ]    

    subtype: Annotated[
        PropertySubtype | None,
        Field(description=f'Property subtype. Must be one of these values: {", ".join([pst for pst in PropertySubtype])}')
    ] = None

    province: Annotated[
        Province | None,
        Field(description=f'Province where the property is located. Must be one of these values: {", ".join([p for p in Province])}')
    ] = None

    postCode: Annotated[
        int,
        Field(description='Postal code of the neighbourhood. Must match province if provided and be within valid Belgian postal code ranges.')
    ]

    habitableSurface: Annotated[
        float,
        Field(gt=0, description='Livable surface area in square meters. Must be > 0.')
    ]

    terraceSurface: Annotated[
        float,
        Field(ge=0, description='Terrace surface area in square meters. Must be ≥ 0.')
    ] = 0

    gardenSurface: Annotated[
        float,
        Field(ge=0, description='Garden surface area in square meters. Must be ≥ 0.')
    ] = 0

    bedroomCount: Annotated[
        int,
        Field(ge=0, description='Number of bedrooms. Must be ≥ 0.')
    ] = 0

    bathroomCount: Annotated[
        int,
        Field(ge=0, description='Number of bathrooms. Must be ≥ 0.')
    ] = 0

    toiletCount: Annotated[
        int,
        Field(ge=0, description='Number of toilets. Must be ≥ 0.')
    ] = 0

    epcScore: Annotated[
        EPCScore | None,
        Field(description=f'Energy performance classification. Must be one of these values: {", ".join([e.value for e in EPCScore])}')
    ] = None

    hasAttic: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has an attic.")
    ] = False

    hasGarden: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a garden.")
    ] = False

    hasAirConditioning: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has air conditioning.")
    ] = False

    hasArmoredDoor: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has an armored door.")
    ] = False

    hasVisiophone: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a video intercom (visiophone).")
    ] = False

    hasTerrace: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a terrace.")
    ] = False

    hasOffice: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a dedicated office space.")
    ] = False

    hasSwimmingPool: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a swimming pool.")
    ] = False

    hasFireplace: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a fireplace.")
    ] = False

    hasBasement: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a basement.")
    ] = False

    hasDressingRoom: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a dressing room.")
    ] = False

    hasDiningRoom: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a dining room.")
    ] = False

    hasLift: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has an elevator.")
    ] = False

    hasHeatPump: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a heat pump system.")
    ] = False

    hasPhotovoltaicPanels: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has solar photovoltaic panels.")
    ] = False

    hasLivingRoom: Annotated[
        bool,
        Field(default=False, description="Indicates whether the property has a living room.")
    ] = False
    
    @field_validator('postCode')
    @classmethod
    def postalcode_in_valid_ranges(cls, value: int) -> int:
        '''
        Validates that the postal code exists in at least one province's allowed range.

        Args:
            value (int): The postal code to check.

        Raises:
            ValueError: If the postal code is not within any known valid ranges.

        Returns:
            int: The validated postal code.
        '''
        if not is_postal_code_valid_in_any_province(value):
            valid_ranges = ', '.join(
                ', '.join(f'{r.start}-{r.stop - 1}' for r in ranges) + f' ({prov})'
                for prov, ranges in PROVINCE_POSTAL_CODE_RANGES.items()
            )
            raise ValueError(f'Invalid postal code {value}. Must be in one of these ranges: {valid_ranges}')
        return value
    
    @field_validator('postCode', mode='after')
    @classmethod
    def validate_postal_code_for_province(cls, value: int, info) -> int:
        '''
        Validates that the postal code matches the expected province, if provided.

        This validator runs after all fields are initialized.

        Args:
            value (int): The postal code to check.
            info: Pydantic validation context containing other field values.

        Raises:
            ValueError: If a province is specified and the postal code does not
                        belong to that province.

        Returns:
            int: The validated postal code.
        '''
        province = info.data.get('province')
        if province and not is_postal_code_valid_for_province(value, province):
            ranges = PROVINCE_POSTAL_CODE_RANGES.get(province)
            if ranges:
                formatted = ', '.join(f'{r.start}-{r.stop - 1}' for r in ranges)
                raise ValueError(
                    f'Postal code {value} is not valid for province {province}. '
                    f'Must be in one of these ranges: {formatted}'
                )
        return value

