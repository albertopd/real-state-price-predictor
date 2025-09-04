# 🏠 Real Estate Price Predictor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.115.14-brightgreen.svg)](https://fastapi.tiangolo.com/)

This is a machine learning-powered API to **predict property prices in Belgium** based on detailed property features such as location, surface area, room count, and amenities.

Built with [FastAPI](https://fastapi.tiangolo.com/) and packaged for quick deployment via `uvicorn`.

## 🚀 Features

- Predict real estate prices using a trained model.
- Schema-validated input using Pydantic v2.
- Automatically infers property details like subtype and province.
- Auto-generated interactive API docs via Swagger/OpenAPI.
- Custom preprocessing pipeline.
- Designed for fast deployment and extensibility.

## 📂 Project Structure

```
real-state-price-predictor/
├── app.py                                # Main FastAPI application entry point
├── Dockerfile                            # Docker configuration for containerized deployment
├── LICENSE                               # Project license (MIT)
├── README.md                             # Project documentation
├── requirements.txt                      # Python dependencies
├── data/                                 # Data files used for inference
│   └── georef-belgium-postal-codes.csv   # Belgian postal codes reference
├── model/                                # Trained ML model storage
│   └── model.joblib                      # Serialized model file
├── predict/                              # Prediction logic
│   └── prediction.py                     # Functions for price prediction
├── preprocessing/                        # Data preprocessing pipeline
│   ├── mappings.py                       # Feature mappings and lookups
│   ├── pipeline.py                       # Preprocessing pipeline definition
│   └── transformers.py                   # Custom transformers for data
├── schemas/                              # Pydantic schemas for request/response validation
│   ├── common.py                         # Shared schema components
│   ├── enums.py                          # Enum definitions for property types, etc.
│   ├── predict_request.py                # Input schema for prediction endpoint
│   ├── prediction_result.py              # Output schema for prediction results
│   ├── property_input.py                 # Property feature input schema
├── utils/                                # Utility functions
│   ├── feature_engineering.py            # Feature engineering helpers
│   └── validators.py                     # Input validation utilities
```

## 🧾 Requirements

Main dependencies include:

- fastapi
- uvicorn
- pandas
- scikit-learn
- pydantic
- python 3.10+

All required packages are listed in [`requirements.txt`](requirements.txt).

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/albertopd/real-state-price-predictor.git
cd real-state-price-predictor
pip install -r requirements.txt
```

## 🚀 Usage

Start the FastAPI server locally:

```bash
uvicorn app:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API interactively.

**Example request to** `/predict` **endpoint:**

```json
{
  "data": {
    "habitableSurface": 500,
    "type": "HOUSE",
    "subtype": "VILLA",
    "province": "Brussels",
    "postCode": 1000,
    "epcScore": "B",
    "bedroomCount": 4,
    "bathroomCount": 2,
    "toiletCount": 2,
    "terraceSurface": 100,
    "gardenSurface": 300,
    "hasAttic": true,
    "hasGarden": true,
    "hasAirConditioning": true,
    "hasTerrace": true,
    "hasSwimmingPool": true,
    "hasFireplace": true,
    "hasBasement": true,
    "hasDressingRoom": true,
    "hasDiningRoom": true,
    "hasLivingRoom": true
  }
}
```

**Expected response:**

```json
{
  "message": "success",
  "data": {
    "prediction": 500000
  }
}
```

## 🐳 Docker Deployment

You can run the project inside a Docker container:

```bash
docker build -t realstate-price-predictor-api .
docker run -p 8000:8000 realstate-price-predictor-api
```

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 👥 Contributors

- [Alberto](https://github.com/albertopd)
- [Choti](https://github.com/jgchoti)
- [Estefania](https://github.com/hermstefanny)
