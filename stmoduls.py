import streamlit as st
import docx2txt
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
    file = st.sidebar.file_uploader("Upload a CHECK file", help='Pick a file to process', accept_multiple_files=False, type=['xlsx'])
    clinic_file = st.sidebar.file_uploader("Upload a clinic file", help='Pick a clinic file to read', accept_multiple_files=False, type=['txt', 'docx'])

    st.sidebar.write('Trend selection')
    all_trends = st.sidebar.checkbox('Show all trends', value=True)
    trend = str()
    if not all_trends:
        trend = st.sidebar.selectbox('Select a trend to analyze...', ('Weight', 'Shoulder', 'Chest', 'Arms', 'Waist', 'Legs', 'Calfs', 'Buttock'), index=0)

    st.sidebar.write('Plot customization')
    color = st.sidebar.color_picker("Pick a color", '#7200F9', help='Plot color')

    return (file, clinic_file, all_trends, trend, color)

def parse_text_clinic(clinic: str):
    for line in clinic:
        decoded_line = str(line.rstrip(),'utf-8')
        st.text(decoded_line)

def parse_docx_clinic(clinic: str):
    st.text(docx2txt.process(clinic))

def client_details(details: tuple, clinic: str):
    expander = st.expander(label="Expand client details")
    with expander:
        if st.checkbox('Expand client details', value=False, help='Show client details'):
            display.display_client_details(details[0])
        if clinic is not None:
            if st.checkbox('Expand client clinic', value=False, help='Show client clinic'):
                if (clinic.name).endswith('.txt'):
                    parse_text_clinic(clinic)
                if (clinic.name).endswith('.docx'):
                    parse_docx_clinic(clinic)
        if st.checkbox('Expand measurements', value=False, help='Show all measurements'):
            display.display_dataset(details[1])
    st.write("")

def weight(measurements: dict, color: str):
    
    st.write('# Weight')
    weight, weight_macro, weight_macro_stack = st.columns(3)
    with weight:
        plots.single_plot(measurements, yvar="weight", yvar_name="Weight (Kg)", plot_title="Weight Time Evolution", style_color=color)
    with weight_macro:
        plots.macro_plain(measurements, style_color=color)
    with weight_macro_stack:
        plots.macro_stack(measurements)
    
    display.display_var_details(measurements, var_title="weight", var="weight", var_name="Weight (Kg)", mu="Kg", plot_title="Weight Distribution", style_color=color)

    st.write('# Macros')
    wcorr_macro1, wcorr_macro2, wcorr_macro3 = st.columns(3)
    with wcorr_macro1:
        plots.correlation_plot(measurements, xvar="weight", xvar_name="Weight (Kg)", yvar="carbo", yvar_name="Carbo", plot_title="Weight and Carbo correlation", style_color=color)
    with wcorr_macro2:
        plots.correlation_plot(measurements, xvar="weight", xvar_name="Weight (Kg)", yvar="proteins", yvar_name="Proteins", plot_title="Weight and Proteins correlation", style_color=color)
    with wcorr_macro3:
        plots.correlation_plot(measurements, xvar="weight", xvar_name="Weight (Kg)", yvar="fat", yvar_name="Fat", plot_title="Weight and Fat correlation", style_color=color)
    
    plots.weight_macro_correlation_plot(measurements)
    
        

def shoulders(measurements: dict, color: str):
    st.write('# Shoulders')
    
    plots.single_plot(measurements, yvar="shoulder", yvar_name="Shoulder (cm)", plot_title="Shoulder Time Evolution", style_color=color)
    display.display_var_details(measurements, var_title="shoulder", var="shoulder", var_name="Shoulder (cm)", mu="cm", plot_title="Shoulder Distribution", style_color=color)

def chest(measurements: dict, color: str):
    st.write('# Chest')

    plots.single_plot(measurements, yvar="chest", yvar_name="Chest (cm)", plot_title="Chest Time Evolution", style_color=color)
    display.display_var_details(measurements, var_title="chest", var="chest", var_name="Chest (cm)", mu="cm", plot_title="Chest Distribution", style_color=color)

def arm(measurements: dict, color: str):
    st.write('# Arm')

    right_arm, left_arm, arm_correlation = st.columns(3)
    with right_arm:
        plots.single_plot(measurements, yvar="arm_dx", yvar_name="Arm dx (cm)", plot_title="Arm dx Time Evolution", style_color=color)
    with left_arm:
        plots.single_plot(measurements, yvar="arm_sx", yvar_name="Arm sx (cm)", plot_title="Arm sx Time Evolution", style_color=color)
    with arm_correlation:
        plots.correlation_plot(measurements, xvar="arm_dx", xvar_name="Arm dx (cm)", yvar="arm_sx", yvar_name="Arm sx (cm)", plot_title="Arm Correlation", style_color=color)
    
    display.display_var_details(measurements, var_title="arm dx", var="arm_dx", var_name="Arm dx (cm)", mu="cm", plot_title="Arm dx Distribution", style_color=color)
    display.display_var_details(measurements, var_title="arm sx", var="arm_sx", var_name="Arm sx (cm)", mu="cm", plot_title="Arm sx Distribution", style_color=color)

def waist(measurements: dict, color: str):
    st.write('# Waist')

    plots.single_plot(measurements, yvar="waist", yvar_name="Waist (cm)", plot_title="Waist Time Evolution", style_color=color, reverse_bullets=True)
    display.display_var_details(measurements, var_title="waist", var="waist", var_name="Waist (cm)", mu="cm", plot_title="Waist Distribution", style_color=color)

def legs(measurements: dict, color: str):
    st.write('# Legs')

    st.write('**Leg roin**')
    right_leg, left_leg, leg_correlation = st.columns(3)
    with right_leg:
        plots.single_plot(measurements, yvar="leggroin_dx", yvar_name="Leg roin dx (cm)", plot_title="Leg roin dx Time Evolution", style_color=color)
    with left_leg:
        plots.single_plot(measurements, yvar="leggroin_sx", yvar_name="Leg roin sx (cm)", plot_title="Leg roin sx Time Evolution", style_color=color)
    with leg_correlation:
        plots.correlation_plot(measurements, xvar="leggroin_dx", xvar_name="Leg roin dx (cm)", yvar="leggroin_sx", yvar_name="Leg roin sx (cm)", plot_title="Leg Roin Correlation", style_color=color)

    display.display_var_details(measurements, var_title="leg roin dx", var="leggroin_dx", var_name="Leg roin dx (cm)", mu="cm", plot_title="Leg roin dx Distribution", style_color=color)
    display.display_var_details(measurements, var_title="leg roin sx", var="leggroin_sx", var_name="Leg roin sx (cm)", mu="cm", plot_title="Leg roin sx Distribution", style_color=color)

    st.write('**Half leg**')

    right_leg, left_leg, leg_correlation = st.columns(3)
    with right_leg:
        plots.single_plot(measurements, yvar="leghalf_dx", yvar_name="Leg half dx (cm)", plot_title="Leg half dx Time Evolution", style_color=color)
    with left_leg:
        plots.single_plot(measurements, yvar="leghalf_sx", yvar_name="Leg half sx (cm)", plot_title="Leg half sx Time Evolution", style_color=color)
    with leg_correlation:
        plots.correlation_plot(measurements, xvar="leghalf_dx", xvar_name="Leg half dx (cm)", yvar="leghalf_sx", yvar_name="Leg half sx (cm)", plot_title="Half Leg Correlation", style_color=color)

    display.display_var_details(measurements, var_title="half leg dx", var="leghalf_dx", var_name="Half Leg dx (cm)", mu="cm", plot_title="Half Leg dx Distribution", style_color=color)
    display.display_var_details(measurements, var_title="half leg sx", var="leghalf_sx", var_name="Half Leg sx (cm)", mu="cm", plot_title="Half Leg sx Distribution", style_color=color)

def calf(measurements: dict, color: str):
    st.write('# Calf')

    right_leg, left_leg, leg_correlation = st.columns(3)
    with right_leg:
        plots.single_plot(measurements, yvar="calf_dx", yvar_name="Calf dx (cm)", plot_title="Calf dx Time Evolution", style_color=color)
    with left_leg:
        plots.single_plot(measurements, yvar="calf_sx", yvar_name="Calf sx (cm)", plot_title="Calf sx Time Evolution", style_color=color)
    with leg_correlation:
        plots.correlation_plot(measurements, xvar="calf_dx", xvar_name="Calf dx (cm)", yvar="calf_sx", yvar_name="Calf sx (cm)", plot_title="Calf Correlation", style_color=color)

def buttock(measurements: dict, color: str):
    st.write('# Buttock')

    plots.single_plot(measurements, yvar="buttock", yvar_name="Nuttock (cm)", plot_title="Buttock Time Evolution", style_color=color)
    display.display_var_details(measurements, var_title="buttock", var="buttock", var_name="Buttock (cm)", mu="cm", plot_title="Buttock Distribution", style_color=color)
