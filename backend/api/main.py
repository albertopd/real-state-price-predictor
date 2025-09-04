import os
import pandas as pd
import uvicorn
from fastapi import FastAPI
from api.schemas.common import SuccessResponse, ErrorResponse, ValidationErrorResponse
from api.schemas.prediction_result import PredictionResult
from api.schemas.predict_request import PredictRequest
from api.predict.prediction import predict
from pipelines.preprocessing.pipeline import preprocess


# Define the FastAPI app instance
app = FastAPI()


@app.get(
    "/",
    response_model=SuccessResponse[None],
    responses={
        200: {
            "description": "Successful heartbeat check",
            "content": {"application/json": {"example": {"message": "alive"}}},
        }
    },
    response_model_exclude_none=True,
)
async def root():
    """
    Health check endpoint to confirm the API is running.

    Returns:
        SuccessResponse: A message confirming the API is alive.
    """
    return SuccessResponse(message="alive")


@app.get(
    "/predict",
    response_model=SuccessResponse[None],
    responses={
        200: {
            "description": "Instructions on how to use the POST /predict endpoint",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Send a POST request to /predict with a JSON body matching the schema. "
                        "See the documentation (Swagger UI) for details."
                    }
                }
            },
        }
    },
    response_model_exclude_none=True,
)
async def predict_get():
    """
    Instructional endpoint that explains how to use the POST /predict route.

    Returns:
        SuccessResponse: A message with usage instructions.
    """
    return SuccessResponse(
        message="Send a POST request to /predict with a JSON body matching the schema. "
        "See the documentation (Swagger UI) for details."
    )


@app.post(
    "/predict",
    response_model=SuccessResponse[PredictionResult],
    responses={
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "enum",
                                "loc": ["body", "data", "type"],
                                "msg": "Input should be 'APARTMENT' or 'HOUSE'",
                                "input": "OTHER",
                                "ctx": {"expected": "'APARTMENT' or 'HOUSE'"}
                            }
                        ]
                    }
                }
            }
        },
        500: {"model": ErrorResponse},
    },
)
async def predict_post(request: PredictRequest):
    """
    Predicts property price based on input features.

    Args:
        request (PredictRequest): Request object containing the input data for the property.

    Returns:
        SuccessResponse[PredictionResult]: Predicted price for the given property input.

    Raises:
        ErrorResponse: If preprocessing or prediction fails (e.g., invalid data types, missing encodings, etc.).
    """
    try:
        data = request.data
        df = pd.DataFrame([data.model_dump()])
        df = preprocess(df)

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
        model_path = os.path.join(base_dir, "model.joblib")
        predicted_price = predict(df, model_path)

        return SuccessResponse(data=PredictionResult(prediction=predicted_price))

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return ErrorResponse(error=f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
