from pydantic import BaseModel


class PredictionResult(BaseModel):
    prediction: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prediction": 500000,
                }
            ]
        }
    }
