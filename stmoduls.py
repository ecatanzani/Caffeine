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
    file = st.sidebar.file_uploader("Upload an XLSX file", help='Pick a file to process')
    clinic_file = st.sidebar.file_uploader("Upload a clinic file", help='Pick a clinic file to read')

    st.sidebar.write('Trend selection')
    all_trends = st.sidebar.checkbox('Show all trends', value=True)
    trend = str()
    if not all_trends:
        trend = st.sidebar.selectbox('Select a trend to analyze...', ('Weight', 'Shoulder', 'Chest', 'Arms', 'Waist', 'Legs', 'Calfs', 'Buttock'), index=0)

    st.sidebar.write('Plot customization')
    color = st.sidebar.color_picker("Pick a color", '#7200F9', help='Plot color')

    return (file, clinic_file, all_trends, trend, color)

def client_details(details: tuple, clinic: str):

    expander = st.expander(label="Expand client details")
    with expander:
        if st.checkbox('Expand client details', value=False, help='Show client details'):
            display.display_client_details(details[0])
        if clinic is not None:
            if st.checkbox('Expand client clinic', value=False, help='Show client clinic'):
                for line in clinic:
                    decoded_line = str(line.rstrip(),'utf-8')
                    st.text(decoded_line)
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
        plots.macro_stack(measurements)
    plots.single_histo_with_mean(measurements, yvar="weight", yvar_name="Weight (Kg)", plot_title="Weight Distribution", style_color=color)

    wcorr_macro1, wcorr_macro2, wcorr_macro3 = st.columns(3)
    with wcorr_macro1:
        plots.correlation_plot(measurements, xvar="weight", xvar_name="Weight (Kg)", yvar="macro1", yvar_name="Macro 1", plot_title="Weight and Macro 1 correlation", style_color=color)
    with wcorr_macro2:
        plots.correlation_plot(measurements, xvar="weight", xvar_name="Weight (Kg)", yvar="macro2", yvar_name="Macro 2", plot_title="Weight and Macro 2 correlation", style_color=color)
    with wcorr_macro3:
        plots.correlation_plot(measurements, xvar="weight", xvar_name="Weight (Kg)", yvar="macro3", yvar_name="Macro 3", plot_title="Weight and Macro 3 correlation", style_color=color)
    plots.weight_macro_correlation_plot(measurements)

def shoulders(measurements: dict, color: str):
    st.write('**Shoulders**')
    shoulder_chart, shoulder_histo = st.columns(2)
    with shoulder_chart:
        plots.single_plot(measurements, yvar="shoulder", yvar_name="Shoulder (cm)", plot_title="Shoulder Time Evolution", style_color=color)
    with shoulder_histo:
        plots.single_histo_with_mean(measurements, yvar="shoulder", yvar_name="Shoulder (cm)", plot_title="Shoulder Distribution", style_color=color)

def legs(measurements: dict, color: str):
    st.write('**Legs**')
    right_leg, left_leg, leg_correlation = st.columns(3)
    with right_leg:
        plots.single_plot(measurements, yvar="leggroin_dx", yvar_name="Leg roin dx (cm)", plot_title="Leg roin dx Time Evolution", style_color=color)
        plots.single_histo_with_mean(measurements, yvar="leggroin_dx", yvar_name="Leg roin dx (cm)", plot_title="Leg roin dx Distribution", style_color=color)
    with left_leg:
        plots.single_plot(measurements, yvar="leggroin_sx", yvar_name="Leg roin sx (cm)", plot_title="Leg roin sx Time Evolution", style_color=color)
        plots.single_histo_with_mean(measurements, yvar="leggroin_sx", yvar_name="Leg roin sx (cm)", plot_title="Leg roin sx Distribution", style_color=color)
    with leg_correlation:
        plots.correlation_plot(measurements, xvar="leggroin_dx", xvar_name="Leg roin dx (cm)", yvar="leggroin_sx", yvar_name="Leg roin sx (cm)", plot_title="Leg Roin Correlation", style_color=color)