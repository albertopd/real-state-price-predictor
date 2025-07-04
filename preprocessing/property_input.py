from pydantic import BaseModel

# TODO: Add some basic validation and metada (description of the fields)
class PropertyInput(BaseModel):
    area: int
    property_type: str #"APARTMENT" | "HOUSE" | "OTHERS"
    rooms_number: int 
    zip_code: int
    land_area: int | None = None
    garden: bool | None = None
    garden_area: int | None = None
    equipped_kitchen: bool | None = None
    full_address: str | None = None
    swimming_pool: bool | None = None
    furnished: bool | None = None
    open_fire: bool | None = None
    terrace: bool | None = None
    terrace_area: int | None = None
    facades_number: int | None = None
    building_state: str | None = None #"NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"