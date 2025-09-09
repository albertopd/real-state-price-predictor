from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.property_input import PropertyInput


class RootResponse(BaseModel):
    success: bool = True
    message: str = Field(
        examples=["Real Estate Price Predictor. Visit /docs for API documentation."]
    )
    version: str = Field(examples=["1.0.0"])


class HealthResponse(BaseModel):
    success: bool = True
    status: str = Field(examples=["healthy"])


class PredictRequest(BaseModel):
    property: PropertyInput


class PredictionResult(BaseModel):
    predicted_price: float = Field(..., examples=[350000.0])
    currency: str = Field("EUR", examples=["EUR"])


class PredictResponse(BaseModel):
    success: bool = True
    result: PredictionResult


class ErrorResponse(BaseModel):
    success: bool = False
    error: str = Field(examples=["Validation error"])
    details: Optional[dict] = Field(
        None,
        examples=[
            {
                "type": "greater_than",
                "loc": "property.habitableSurface",
                "input": 0,
                "msg": "Input should be greater than 0",
            }
        ],
    )
