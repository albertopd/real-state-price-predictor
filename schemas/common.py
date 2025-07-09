from pydantic import BaseModel
from typing import Generic, TypeVar
from typing import Any, Dict, List, Union

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

# Custom 422 response example schema (not enforced, just for docs)
class ValidationErrorItem(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str
    input: Union[str, int, float, None] = None
    ctx: Dict[str, Any] | None = None

class ValidationErrorResponse(BaseModel):
    detail: List[ValidationErrorItem]