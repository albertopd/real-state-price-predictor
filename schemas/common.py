from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    """
    Generic success response model for successful API responses.

    Attributes:
        message (str): Status message (defaults to "success").
        data (T | None): Optional payload data. Excluded from output if None.

    Example:
        {
            "message": "alive"
        }
    """

    message: str = "success"
    data: T | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "alive",
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """
    Error response model for failed API calls.

    Attributes:
        error (str): A human-readable error message.

    Example:
        {
            "error": "Prediction failed: Something went wrong internally"
        }
    """
    
    error: str

    model_config = {
        "json_schema_extra": {
            "examples": [
            	{
                    "error": "Prediction failed: Something went wrong internaly",
                }
            ]
        }
    }
