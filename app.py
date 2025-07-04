from fastapi import FastAPI, HTTPException, status
from preprocessing.property_input import PropertyInput
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict

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
    return {"message": "We have to put in here the explanation of what the POST expect"}

# Request that receives the data of a house in JSON format.
@app.post("/predict")
async def predict_post(data: PropertyInput):
    try:
        # TODO: handle exceptions/errors
        df = preprocess(data)
        predicted_price = predict(df)

        return {"prediction": predicted_price, "status_code": status.HTTP_200_OK}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# TODO: remove after testing is done
import pandas as pd

sample_data = {
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
    "hasArmoredDoor": False,
    "hasVisiophone": False,
    "hasTerrace": True,
    "hasOffice": False,
    "hasSwimmingPool": True,
    "hasFireplace": True,
    "hasBasement": True,
    "hasDressingRoom": False,
    "hasDiningRoom": True,
    "hasLift": False,
    "hasHeatPump": False,
    "hasPhotovoltaicPanels": False,
    "hasLivingRoom": True,
}
property_input = PropertyInput(**sample_data)
preprocessed_df = preprocess(property_input)
predicted_price = predict(preprocessed_df)
print(predicted_price)
