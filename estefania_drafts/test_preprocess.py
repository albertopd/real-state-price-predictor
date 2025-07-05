import sys
import os
from joblib import dump, load

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from preprocessing.cleaning_data import encode_categorical_features, preprocess
from preprocessing.property_input import PropertyInput

import json


def main():

    ## Load toy example

    with open(r"estefania_drafts\toy_data.json", "r") as f:
        json_data = json.load(f)

    parsed_data = PropertyInput(**json_data[0])

    ## Preprocess toy example
    df = preprocess(parsed_data)

    print("Printing data")
    for column_name in df:
        print(f"\n{column_name}")
        print(df[column_name])

    loaded_model = load(".\model\model.pkl")

    ## Predict toy example with NaN

    prediction = loaded_model.predict(df)

    print("Printing prediction")
    print(prediction)

    ## TODO Predict toy example filling NaN


if __name__ == "__main__":
    main()
