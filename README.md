# ImmoEliza Price Prediction

## Introduction

This project establishes a RESTful API to predict house prices from property features for the Belgian real-estate market

## Description

The project is developed with FastAPI and deployed through a Docker image to build a reliable, efficient API that wraps a ML model for real-estate price prediction.

## API

### Endpoints

**/**

- GET: Returns a message to attest server connection.

**/predict**

- GET: Returns a message with the information of the features to send to the endpoint.
- POST: Returns a price prediction for the property.

### API Usage

The API is live in Render following this [link](https://challenge-api-deployment-estefania-branch.onrender.com/)

- Postman: Create a new Collection and add the base URL.
- CURL

## Requirements

- Python version: Python 3.10.4
- Recommended IDE : VsCode
- Further requirements are described in _requirements.txt_

## Usage:

1. Clone or download the project from its repository
2. Create a Python virtual environment using the requirements file in the directory:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
