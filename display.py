import streamlit as st
import pandas as pd
import numpy as np
import plots


def display_dataset(measurements: dict):
    tmp_df = pd.DataFrame(measurements)
    st.write(tmp_df)

def display_client_details(header: dict):
    st.text("")
    st.text(f"Name: {header['name']}")
    st.text(f"Surname: {header['surname']}")
    st.text(f"Age: {header['age']}")
    st.text(f"Height: {header['height']}")
    st.text(f"Dominant arm: {header['dominant_arm']}")
    st.text("")

def display_var_details(measurements: dict, var_title: str, var: str, var_name: str, mu: str, plot_title: str, style_color: str):
    expander = st.expander(label=f"Expand {var_title} detailed information")
    with expander:
        mean = np.mean(np.array(measurements[var]))
        
        st.text(f"Number of measurements: {len(measurements[var])}")
        st.text(f"Min value: {np.amin(np.array(measurements[var]))} {mu}")
        st.text(f"Max value: {np.amax(np.array(measurements[var]))} {mu}")
        st.text(f"Mean value: {round(mean, 2)} {mu}")

        values_above_mean = 0
        values_below_mean = 0

        for elm in measurements[var]:
            if elm > mean:
                values_above_mean += 1
            if elm < mean:
                values_below_mean += 1

        st.text(f"Number of values below the mean: {values_below_mean}")
        st.text(f"Number of values above the mean: {values_above_mean}")
        st.text(f"Mean frequency: {len(measurements[var])-values_above_mean-values_below_mean}")

        plots.single_histo_with_mean(measurements, xvar=var, xvar_name=var_name, plot_title=plot_title, style_color=style_color)
