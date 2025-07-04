from fastapi import FastAPI
from preprocessing.property_input import PropertyInput
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict

# Define the FastAPI app instance
app = FastAPI()

# Request returning "alive" if the server is alive.
@app.get("/")
async def root():
    return {
        "message": "alive"
    }

# Request returning a string to explain what the POST expect (data and format).
@app.get("/predict")
async def predict_get():
    # TODO: update the message
    return {
        "message": "We have to put in here the explanation of what the POST expect"
    }

# Request that receives the data of a house in JSON format.
@app.post("/predict")
async def predict_post(data: PropertyInput):
    # TODO: handle exceptions/errors
    preprocessed_data = preprocess(data)
    predicted_price = predict(preprocessed_data)
    return {
        "prediction": predicted_price,
        "status_code": 200
    }