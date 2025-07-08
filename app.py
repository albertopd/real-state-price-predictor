import os
from fastapi import FastAPI, HTTPException, status
import pandas as pd
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
    message_predict = {
        "habitableSurface [Mandatory]": "Float-type number that describes the livable area of the property",
        "type [Mandatory]": 'String-type input that indicates if the property is a "HOUSE" or an "APARTMENT"',
        "subtype [Mandatory]": "String-type input that indicates the subtype of property",
        "province [Mandatory]": "String-type input that indicates in which Belgian province the property is located. Must be a valid province",
        "postCode [Mandatory]": "Int-type number that indicates the property location",
        "bedroomCount [Mandatory]": "Int-type number that indicates the number of bedrooms",
        "bathroomCount [Mandatory]": "Int-type number that indicates the number of bathrooms",
        "toiletCount [Optional]": "Int-type number that indicates the number of toilets",
        "epcScore [Optional]": "String-type input that indicates the value of the energy score. Values between A+ and G",
        "terraceSurface [Optional]": "Float-type number that indicates the area of the terrace, if present",
        "gardenSurface [Optional]": "Float-type number that indicates the are of the garden, if present",
        "hasAttic [Optional]": "Bool-type input that indicates if the property has an attic",
        "hasGarden [Optional]": "Bool-type input that indicates if the property has a garden",
        "hasAirConditioning [Optional]": "Bool-type input that indicates if the property has air conditioning",
        "hasArmoredDoor [Optional]": "Bool-type input that indicates if the property has an armored door",
        "hasVisiophone [Optional]": "Bool-type input that indicates if the property has visiophone",
        "hasOffice [Optional]": "Bool-type input that indicates if the property has an office",
        "hasSwimmingPool [Optional]": "Bool-type input that indicates if the property has a swimming pool",
        "hasFireplace [Optional]": "Bool-type input that indicates if the property has a fireplace",
        "hasBasement [Optional]": "Bool-type input that indicates if the property has a basement",
        "hasDressingRoom [Optional]": "Bool-type input that indicates if the property has a dressing room",
        "hasDiningRoom [Optional]": "Bool-type input that indicates if the property has a dining room",
        "hasLift [Optional]": "Bool-type input that indicates if the property has a lift",
        "hasHeatPump [Optional]": "Bool-type input that indicates if the property has a heat pump",
        "hasPhotovoltaicPanels [Optional]": "Bool-type input that indicates if the property has photvoltaic panels",
        "hasLivingRoom [Optional]": "Bool-type input that indicates if the property has a living room",
    }

    return {"The POST method requires the following fields": message_predict}


# Request that receives the data of a house in JSON format.
@app.post("/predict")
async def predict_post(data: PropertyInput):
    try:
        # TODO: handle exceptions/errors

        data_dict = data.model_dump()  # extract dict once here
        df = preprocess(data_dict)
        print("-------------Preprocessing completed----------------")
        predicted_price = predict(df)

        return {"prediction": predicted_price, "status_code": status.HTTP_200_OK}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
