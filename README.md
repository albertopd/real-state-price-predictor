# 🏠 Real Estate Price Prediction API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

This is a machine learning-powered API to **predict property prices in Belgium** based on detailed property features such as location, surface area, room count, and amenities.

Built with [FastAPI](https://fastapi.tiangolo.com/) and packaged for quick deployment via `uvicorn`.

---

## 🚀 Features

- Predict real estate prices using a trained model.
- Schema-validated input using Pydantic v2.
- Automatically infers property details like subtype and province.
- Auto-generated interactive API docs via Swagger/OpenAPI.
- Custom preprocessing pipeline.
- Designed for fast deployment and extensibility.

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/albertopd/challenge-api-deployment.git
cd challenge-api-deployment
pip install -r requirements.txt
```

---

## 🧪 Usage

Start the FastAPI server locally:

```bash
uvicorn app:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API interactively.

### Example request to `/predict`:

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

Expected response:

```json
{
  "message": "success",
  "data": {
    "prediction": 500000
  }
}
```

---

## 🐳 Docker Deployment

You can run the project inside a Docker container:

```bash
docker build -t property-price-api .
docker run -p 8000:8000 property-price-api
```

---

## 🧾 Requirements

Main dependencies include:

- fastapi
- uvicorn
- pandas
- scikit-learn
- pydantic
- python 3.10+

All required packages are listed in [`requirements.txt`](requirements.txt).

---

## 👥 Contributors

- [Alberto](https://github.com/albertopd)
- [Choti](https://github.com/jgchoti)
- [Estefania](https://github.com/hermstefanny)
---

## ⏳ Timeline

This API was developed as part of the BeCode Data Science & AI challenge during July 2025. It demonstrates the application of machine learning with modern API practices.

---