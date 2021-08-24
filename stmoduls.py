import streamlit as st
import display
import plots

def app_settings() -> tuple:
    st.set_page_config(layout="wide")
    st.write("""
    # Personal Interactive Status Monitor
    Caffeine release v1.0 - alpha
    """)

    st.sidebar.write('**Settings**')
    
    st.sidebar.write('File selection')
    file = st.sidebar.file_uploader("Select an xlsx file to upload...", help='Pick a file to process')
    
    st.sidebar.write('Trend selection')
    all_trends = st.sidebar.checkbox('Show all trends', value=True)
    trend = str()
    if not all_trends:
        trend = st.sidebar.selectbox('Select a trend to analyze...', ('Weight', 'Shoulder', 'Chest', 'Arms', 'Waist', 'Legs', 'Calfs', 'Buttock'), index=0)

    st.sidebar.write('Plot customization')
    color = st.sidebar.color_picker("Pick a color", '#7200F9', help='Plot color')

    return (file, all_trends, trend, color)

def client_details(details: tuple):

    expander = st.expander(label="Expand client details")
    with expander:
        if st.checkbox('Expand client details', value=False, help='Show client details'):
            display.display_client_details(details[0])
        if st.checkbox('Expand client clinic', value=False, help='Show client clinic'):
            st.text('Clinic to be implemented')
        if st.checkbox('Expand measurements', value=False, help='Show all measurements'):
            display.display_dataset(details[1])
    st.write("")

def weight(measurements: dict, color: str):
    st.write('**Weight**')
    
    weight, weight_macro, weight_macro_stack = st.columns(3)
    with weight:
        plots.single_plot(measurements, yvar="weight", yvar_name="Weight (Kg)", plot_title="Weight Time Evolution", style_color=color)
    with weight_macro:
        plots.macro_plain(measurements, style_color=color)
    with weight_macro_stack:
        plots.macro_stack(measurements, style_color=color)

    plots.single_histo_with_mean(measurements, yvar="weight", yvar_name="Weight (Kg)", plot_title="Weight Distribution", style_color=color)

def shoulders(measurements: dict, color: str):
    st.write('**Shoulders**')
    plots.single_plot(measurements, yvar="shoulder", yvar_name="Shoulder (cm)", plot_title="Shoulder Time Evolution", style_color=color)

def legs(measurements: dict, color: str):
    st.write('**Legs**')
    right_leg, left_leg = st.columns(2)
    with right_leg:
        plots.single_plot(measurements, yvar="leggroin_dx", yvar_name="Leg roin dx (cm)", plot_title="Leg roin dx Time Evolution", style_color=color)
    with left_leg:
        plots.single_plot(measurements, yvar="leggroin_sx", yvar_name="Leg roin sx (cm)", plot_title="Leg roin sx Time Evolution", style_color=color)