import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

DATA_PATH = (
    Path(__file__).resolve().parents[3] / "data" / "analysis" / "analysis_dataset.parquet"
)

st.title("Real Estate Analysis Dashboard")

if not DATA_PATH.exists():
    st.warning("Analysis dataset not found. Run the Airflow DAG to generate it.")
else:
    df = pd.read_parquet(DATA_PATH)

    # Filters
    cols = st.columns(3)
    type_sel = cols[0].selectbox(
        "Type", options=["All"] + sorted(df["Type of property"].dropna().unique().tolist())
    )
    city = cols[1].selectbox(
        "Locality", options=["All"] + sorted(df["Locality"].dropna().unique().tolist())
    )
    min_bed = cols[2].number_input("Min bedrooms", value=1, step=1)

    f = df.copy()
    if type_sel != "All":
        f = f[f["Type of property"] == type_sel]
    if city != "All":
        f = f[f["Locality"] == city]
    f = f[f["Number of bedrooms"] >= min_bed]

    st.metric("Listings", len(f))
    st.metric("Median price €/m²", round(f["price_per_m2"].median() if len(f) else 0))

    st.subheader("Price €/m² distribution")
    st.bar_chart(f["price_per_m2"])

    st.subheader("Sample rows")
    st.dataframe(f.head(200))
