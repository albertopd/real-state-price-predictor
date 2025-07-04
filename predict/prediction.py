import joblib 

def predict(preprocessed_data: dict) -> float:
    # TODO: load model, do the prediction, handle errors
    model = joblib.load('model.joblib')
    predicted_price = model.predict(preprocessed_data)
    return predicted_price