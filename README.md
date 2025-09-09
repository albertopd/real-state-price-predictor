# 🏠 Real Estate Price Predictor
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
real-estate-price-predictor/
├── airflow/
│   ├── dags/
│   │   └── real_estate_pipeline.py
│   └── requirements.txt
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── ml_models/
│   │   └── model.joblib
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── preprocessing/
│   │       ├── __init__.py
│   │       ├── encoders.py
│   │       ├── enrichers.py
│   │       ├── mappings.py
│   │       ├── pipeline_definitions.py
│   │       └── data/
│   │           └── georef-belgium-postal-codes.csv
│   ├── predictors/
│   │   ├── __init__.py
│   │   └── price_predictor.py
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── enums.py
│       │   ├── models.py
│       │   ├── prediction_result.py
│       │   ├── predict_request.py
│       │   ├── property_input.py
│       │   └── validators.py
│       └── settings.py
├── dashboard/
│   └── app.py
├── data/
│   ├── analysis/
│   │   └── .gitkeep
│   ├── raw/
│   │   └── .gitkeep
│   └── training/
│       └── .gitkeep
├── docker-compose.airflow.yml
├── docker-compose.yml
├── LICENSE
├── ml/
│   ├── __init__.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── analysis_preprocess.py
│   │   └── training_preprocess.py
│   └── training/
│       ├── __init__.py
│       └── train_regression.py
├── models/
│   └── .gitkeep
├── README.md
├── scripts/
│   ├── scrape_apartments.py
│   └── scrape_houses.py
```


## 🧾 Requirements

Main dependencies include:

- fastapi
- uvicorn
- pandas
- scikit-learn
- pydantic
- python 3.13+

All required packages are listed in [`requirements.txt`](requirements.txt).

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/albertopd/real-estate-price-predictor.git
cd real-estate-price-predictor
pip install -r requirements.txt
```

## 🚀 Usage

Start the FastAPI server locally:

```bash
cd backend
uvicorn api.main:app --reload
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

You can run the FastAPI application inside a Docker container:

```bash
docker build -t real-estate-price-predictor -f backend/Dockerfile .
docker run -p 8000:8000 real-estate-price-predictor
```

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 👥 Contributors

- [Alberto](https://github.com/albertopd)
- [Choti](https://github.com/jgchoti)
- [Estefania](https://github.com/hermstefanny)
