from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from preprocessing.property_input import PropertyInput, CompareInput
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict
from typing import List


# Define the FastAPI app instance
app = FastAPI()


# Request returning "alive" if the server is alive.
@app.get("/")
async def root():
    return {"message": "alive"}


# Request returning a string to explain what the POST expect (data and format).
@app.get("/predict")
async def predict_get():
    # TODO: update the message
    return {
        "expected_fields": {
            "habitableSurface": "float, e.g. 85.0",
            "type": "string, e.g. 'APARTMENT' or 'HOUSE'",
            "subtype": "string, more specific category like 'VILLA', 'PENTHOUSE'",
            "province": "string, e.g. 'Antwerp', 'Brussels'",
            "postCode": "integer, e.g. 2000",
            "epcScore": "string, e.g. 'A', 'B', 'C', etc.",
            "bedroomCount": "int",
            "bathroomCount": "int",
            "toiletCount": "int",
            "terraceSurface": "float",
            "gardenSurface": "float",
            "hasAttic": "bool",
            "hasGarden": "bool",
            "hasAirConditioning": "bool",
            "hasArmoredDoor": "bool",
            "hasVisiophone": "bool",
            "hasTerrace": "bool",
            "hasOffice": "bool",
            "hasSwimmingPool": "bool",
            "hasFireplace": "bool",
            "hasBasement": "bool",
            "hasDressingRoom": "bool",
            "hasDiningRoom": "bool",
            "hasLift": "bool",
            "hasHeatPump": "bool",
            "hasPhotovoltaicPanels": "bool",
            "hasLivingRoom": "bool",
        },
    }


# Request that receives the data of a house in JSON format.
@app.post("/predict")
async def predict_post(data: PropertyInput):
    preprocessed_data = preprocess(data)
    predicted_price = predict(preprocessed_data)
    return {"prediction": predicted_price, "status_code": 200}


@app.get("/compare")
async def compare_get(data: CompareInput):
    return {
        "expected_fields": {
            "actual_price": "float, e.g. 350000.0",
            "habitableSurface": "float, e.g. 85.0",
            "type": "string, e.g. 'APARTMENT' or 'HOUSE'",
            "subtype": "string, more specific category like 'VILLA', 'PENTHOUSE'",
            "province": "string, e.g. 'Antwerp', 'Brussels'",
            "postCode": "integer, e.g. 2000",
            "epcScore": "string, e.g. 'A', 'B', 'C', etc.",
            "bedroomCount": "int",
            "bathroomCount": "int",
            "toiletCount": "int",
            "terraceSurface": "float",
            "gardenSurface": "float",
            "hasAttic": "bool",
            "hasGarden": "bool",
            "hasAirConditioning": "bool",
            "hasArmoredDoor": "bool",
            "hasVisiophone": "bool",
            "hasTerrace": "bool",
            "hasOffice": "bool",
            "hasSwimmingPool": "bool",
            "hasFireplace": "bool",
            "hasBasement": "bool",
            "hasDressingRoom": "bool",
            "hasDiningRoom": "bool",
            "hasLift": "bool",
            "hasHeatPump": "bool",
            "hasPhotovoltaicPanels": "bool",
            "hasLivingRoom": "bool",
        }
    }


@app.post("/compare")
async def compare_price(data: CompareInput):
    preprocessed_data = preprocess(data.property)
    predicted_price = predict(preprocessed_data)
    diff = data.actual_price - predicted_price
    abs_diff = abs(diff)
    percentage_diff = abs_diff / predicted_price
    if percentage_diff < 0.05:
        evaluation = "good"
    elif diff > 0:
        evaluation = "overpriced"
    else:  
        evaluation = "underpriced"

    return {
        "predicted_price": predicted_price,
        "actual_price": data.actual_price,
        "difference": diff, 
        "evaluation": evaluation,
        "status_code": 200,
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []

    for err in exc.errors():
        field = err["loc"][1] if len(err["loc"]) > 1 else err["loc"][0]
        message = err["msg"]
        error_type = err["type"]

        details.append({"field": field, "message": message, "type": error_type})
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid Input", "detail": details},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid Input", "detail": str(exc)},
    )
