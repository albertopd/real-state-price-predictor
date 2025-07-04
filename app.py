from fastapi import FastAPI
from model.pydantic_model import PropertyInput
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict

# Define the FastAPI app instance
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "alive"
    }

# Request returning a string to explain what the POST expect (data and format).
@app.get("/predict")
async def predict_get():
    return {
        "result": "We have to put in here the explanation of what the POST expect"
    }

# Request that receives the data of a house in JSON format.
@app.post("/predict")
async def predict_post(data: PropertyInput):
    preprocessed_data = preprocess(data)
    predicted_price = predict(preprocessed_data)
    return {
        "result": predicted_price
    }