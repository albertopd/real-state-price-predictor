import os
import pandas as pd
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.settings import settings
from app.schemas.models import (
    RootResponse,
    HealthResponse,
    PredictRequest,
    PredictionResult,
    PredictResponse,
    ErrorResponse,
)
from pipelines.preprocessing.pipeline_definitions import preprocessing_pipeline
from predictors.price_predictor import predict_price


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)


# =====================
# Exception handlers
# =====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = {
        "errors": [
            {
                "type": err["type"],
                "loc": ".".join(err["loc"][-2:]),
                "input": err["input"],
                "msg": err["msg"],
            }
            for err in exc.errors()
        ]
    }

    content = ErrorResponse(
        success=False, error="Validation error", details=details
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    content = ErrorResponse(
        success=False, error="Internal server error", details={"message": str(exc)}
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )


# ====================
# Routes
# ====================


@app.get("/", response_model=RootResponse, summary="Root endpoint")
async def root():
    return RootResponse(
        message=f"{app.title}. Visit /docs for API documentation.",
        version=app.version,
    )


@app.get("/health", response_model=HealthResponse, summary="Health check")
def health_check():
    return HealthResponse(status="healthy")


@app.post(
    "/predict",
    response_model=PredictResponse,
    responses={422: {"model": ErrorResponse, "description": "Validation Error"}},
    summary="Predict property price",
    description="Predicts property price based on input features.",
)
async def predict(request: PredictRequest):
    property = request.property
    ml_ready = property.to_ml_format()
    df = pd.DataFrame([ml_ready])
    df = preprocessing_pipeline.fit_transform(df)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml_models"))
    model_path = os.path.join(base_dir, "model.joblib")
    predicted_price = predict_price(df, model_path)

    return PredictResponse(
        result=PredictionResult(
            predicted_price=predicted_price,
            currency=settings.CURRENCY,
        )
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
