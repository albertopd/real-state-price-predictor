from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TITLE: str = "Real Estate Price Predictor API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API to predict real estate prices based on property features."
    CURRENCY: str = "EUR"

    class Config:
        env_file = ".env"

settings = Settings()
