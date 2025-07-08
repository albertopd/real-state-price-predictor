# Streamlit (frontend)
import requests
import streamlit as st

st.title("House Price Predictor")

left_column, center_column, right_column = st.columns(3)


with left_column:
    # Manual Inputs
    habitableSurface = st.number_input(
        "Habitable Surface",
        format="%f",
        key="habitableSurface",
        width=200,
        min_value=1.0,
    )
    print(habitableSurface)

    postCode = st.number_input("Postal Code", key="postCode", width=200, min_value=0)
    print(postCode)

    bedroomCount = st.number_input(
        "Bedroom Count", key="bedroomCount", width=200, min_value=0
    )
    print(bedroomCount)

    bathroomCount = st.number_input(
        "Bathroom Count", key="bathroomCount", width=200, min_value=0
    )
    print(bathroomCount)

    toiletCount = st.number_input(
        "Toilet Count", key="toiletCount", width=200, min_value=0
    )
    print(toiletCount)

with center_column:
    # Selectors
    type_p = st.selectbox("Type of Property", ("HOUSE", "APARTMENT"), width=200)
    print(type_p)

    subtype = st.selectbox(
        "Subtype of Property",
        (
            "APARTMENT",
            "HOUSE",
            "FLAT_STUDIO",
            "DUPLEX",
            "PENTHOUSE",
            "GROUND_FLOOR",
            "APARTMENT_BLOCK",
            "MANSION",
            "EXCEPTIONAL_PROPERTY",
            "MIXED_USE_BUILDING",
            "TRIPLEX",
            "LOFT",
            "VILLA",
            "TOWN_HOUSE",
            "CHALET",
            "MANOR_HOUSE",
            "SERVICE_FLAT",
            "KOT",
            "FARMHOUSE",
            "BUNGALOW",
            "COUNTRY_COTTAGE",
            "OTHER_PROPERTY",
            "CASTLE",
            "PAVILION",
        ),
        width=200,
    )
    print(subtype)

    province = st.selectbox(
        "Brussels Province",
        (
            "Brussels",
            "Luxembourg",
            "Antwerp",
            "Flemish Brabant",
            "East Flanders",
            "West Flanders",
            "Liège",
            "Walloon Brabant",
            "Limburg",
            "Namur",
            "Hainaut",
        ),
        width=200,
    )
    print(province)

    epcScore = st.selectbox(
        "Energy Score (EPC)",
        (
            "A+",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
        ),
        width=200,
    )
    print(epcScore)

gardenSurface = 0
terraceSurface = 0

with right_column:
    hasGarden = st.checkbox("Garden")
    if hasGarden:
        gardenSurface = st.number_input(
            "Garden Surface",
            format="%f",
            key="gardenSurface",
            width=200,
            min_value=0.0,
        )

    hasTerrace = st.checkbox("Terrace")
    if hasTerrace:
        terraceSurface = st.number_input(
            "Terrace Surface",
            format="%f",
            key="terraceSurface",
            width=200,
            min_value=0.0,
        )
    hasAttic = st.checkbox("Attic")
    hasAirConditioning = st.checkbox("Air Conditioning")
    hasVisiophone = st.checkbox("Visiophone")
    hasOffice = st.checkbox("Office")
    hasSwimmingPool = st.checkbox("Swimming Pool")
    hasFireplace = st.checkbox("Fireplace")
    hasBasement = st.checkbox("Basement")
    hasDresssingRoom = st.checkbox("Dressing Room")
    hasDiningRoom = st.checkbox("Dining Room")
    hasLift = st.checkbox("Lift")
    hasHeatPump = st.checkbox("Heat Pump")
    hasPhotovoltaicPanels = st.checkbox("Photovoltaic Panels")
    hasLivingRoom = st.checkbox("Living Room")

input_data = {
    "habitableSurface": habitableSurface,
    "type": type_p,
    "subtype": subtype,
    "province": province,
    "postCode": postCode,
    "epcScore": epcScore,
    "bedroomCount": bedroomCount,
    "bathroomCount": bathroomCount,
    "toiletCount": toiletCount,
    "gardenSurface": gardenSurface,
    "terraceSurface": gardenSurface,
    "hasAttic": hasAttic,
    "hasGarden": hasGarden,
    "hasTerrace": hasTerrace,
    "hasFireplace": hasFireplace,
    "hasLivingRoom": hasLivingRoom,
    "hasAirConditioning ": hasAirConditioning,
    "hasVisiophone": hasVisiophone,
    "hasOffice ": hasOffice,
    "hasSwimmingPool": hasSwimmingPool,
    "hasFireplace ": hasFireplace,
    "hasBasement": hasBasement,
    "hasDresssingRoom": hasDresssingRoom,
    "hasDiningRoom": hasDiningRoom,
    "hasLift": hasLift,
    "hasHeatPump": hasHeatPump,
    "hasPhotovoltaicPanels ": hasPhotovoltaicPanels,
    "hasLivingRoom ": hasLivingRoom,
}

get_prediction = st.button("Get Price Prediction")
if get_prediction:
    response = requests.post(
        "https://challenge-api-deployment-estefania-branch.onrender.com/predict",
        json=input_data,
    )
    st.write("Price Prediction")
    st.write(response.json()["prediction"])
