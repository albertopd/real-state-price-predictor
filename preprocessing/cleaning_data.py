import pandas as pd
from preprocessing.property_input import PropertyInput

def preprocess(data: PropertyInput) -> pd.DataFrame:
    # Convert to dict
    data_dict = data.model_dump()

    # Convert to single-row DataFrame
    df = pd.DataFrame([data_dict])

    # TODO: Add all the preprocessing

    return df
