from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from preprocessing.property_input import PropertyInput, CompareInput
from preprocessing.cleaning_data import PropertyPreprocessor
from predict.prediction import HousePricePredictor
from typing import List
class PredictionAPI:
    def __init__(self):
        self.app = FastAPI()
        self.preprocessor = PropertyPreprocessor()
        self.predictor = HousePricePredictor()

        self.register_routes()
        self.register_exception_handlers()
        
    def register_routes(self):
        # Request returning "alive" if the server is alive.
        @self.app.get("/")
        async def root():
            return {"message": "alive"}
        # Request returning a string to explain what the POST expect (data and format).
        @self.app.get("/predict")
        async def predict_get():
            return {
                "message": "POST request expected with property data",
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
        @self.app.post("/predict")
        async def predict_post(data: PropertyInput):
            preprocessed_data = preprocess(data)
            predicted_price = predict(preprocessed_data)
            return {"prediction": predicted_price, "status_code": 200}
        
        @self.app.get("/compare")
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
        }}
        
        @self.app.post("/compare")
        async def compare_price(self, data: CompareInput):
            preprocessed_data = self.preprocessor(data.property)
            predicted_price = self.predict(preprocessed_data)
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
        "status_code": 200,}
        
    def register_exception_handlers(self):
        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(self, request: Request, exc: RequestValidationError):
            details = []
            for err in exc.errors():
                field = err["loc"][1] if len(err["loc"]) > 1 else err["loc"][0]
                message = err["msg"]
                error_type = err["type"]
                details.append({"field": field, "message": message, "type": error_type})
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid Input", "detail": details},)
        
        @self.app.exception_handler(ValueError)
        async def value_error_handler(self, request: Request, exc: ValueError):
            return JSONResponse( status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid Input", "detail": str(exc)},)
            
    def get_app(self) -> FastAPI:
        return self.app

api = PredictionAPI()
app = api.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)