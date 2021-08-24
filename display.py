import streamlit as st
import pandas as pd

def display_dataset(measurements: dict):
    tmp_df = pd.DataFrame(measurements)
    st.write(tmp_df)

def display_client_details(header: dict):
    st.text("")
    st.text(f"Age: {header['age']}")
    st.text(f"Height: {header['height']}")
    st.text(f"Dominant arm: {header['dominant_arm']}")
    st.text("")