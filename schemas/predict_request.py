from pydantic import BaseModel
from schemas.property_input import PropertyInput 

class PredictRequest(BaseModel):
    """
    Wrapper schema to encapsulate a PropertyInput instance in a request body.
    """

    data: PropertyInput

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": {
                        "habitableSurface": 500,
                        "type": "HOUSE",
                        "subtype": "VILLA",
                        "province": "Brussels",
                        "postCode": 1000,
                        "epcScore": "B",
                        "bedroomCount": 4,
                        "bathroomCount": 2,
                        "toiletCount": 2,
                        "terraceSurface": 100,
                        "gardenSurface": 300,
                        "hasAttic": True,
                        "hasGarden": True,
                        "hasAirConditioning": True,
                        "hasTerrace": True,
                        "hasSwimmingPool": True,
                        "hasFireplace": True,
                        "hasBasement": True,
                        "hasDressingRoom": True,
                        "hasDiningRoom": True,
                        "hasLivingRoom": True,
                    }
                },
                {
                    "data": {
                        "habitableSurface": 85,
                        "type": "APARTMENT",
                        "subtype": "PENTHOUSE",
                        "province": "Antwerp",
                        "postCode": 2000,
                        "epcScore": "C",
                        "bedroomCount": 2,
                        "bathroomCount": 1,
                        "toiletCount": 1,
                        "terraceSurface": 15,
                        "hasTerrace": True,
                        "hasLift": True,
                        "hasAirConditioning": True,
                        "hasLivingRoom": True,
                    }
                },
                {
                    "data": {
                        "habitableSurface": 35,
                        "type": "APARTMENT",
                        "subtype": "FLAT_STUDIO",
                        "province": "Liège",
                        "postCode": 4000,
                        "epcScore": "D",
                        "bedroomCount": 1,
                        "bathroomCount": 1,
                        "toiletCount": 1,
                        "hasLivingRoom": False,
                    }
                },
            ]
        }
    }
