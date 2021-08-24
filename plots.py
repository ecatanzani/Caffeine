import altair as alt
from altair.vegalite.v4.schema.channels import Color
import pandas as pd
import streamlit as st

def get_slope_color(values: list, reverse=False) -> list:
    green = '#3DF900'
    red = '#F90004'
    yellow = '#F9E300'
    
    colors = [green]
    last_value = values[0]

    for elm in values[1:]:
        if not reverse:
            if elm > last_value:
                colors.append(green)
            elif elm == last_value:
                colors.append(yellow)
            else:
                colors.append(red)
        else:
            if elm > last_value:
                colors.append(red)
            elif elm == last_value:
                colors.append(yellow)
            else:
                colors.append(green)
        last_value = elm

    return colors
    
def single_plot(measurements: dict, yvar: str, yvar_name: str, plot_title: str, style_color: str):
    
    time_data = pd.DataFrame({
        'Date': measurements['date'], 
        yvar_name: measurements[yvar],
        'color': get_slope_color(measurements[yvar], reverse=False)
    })
    
    chart = alt.Chart(time_data).mark_line(clip=True).mark_area(
        line={'color': style_color},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0), 
                alt.GradientStop(color=style_color, offset=1)],
                x1=1,
                x2=1,
                y1=1,
                y2=0
        )
        ).encode(
            alt.X('Date:T'),
            alt.Y(f"{yvar_name}:Q")
        ).properties(title=plot_title)

    circles = alt.Chart(time_data).mark_point(
        filled=True,
        size=100
    ).encode(
        x='Date:T',
        y=f'{yvar_name}:Q',
        color = alt.Color('color', legend=None, scale=None)
    ).properties(title=plot_title)

    st.write(chart + circles)

def macro_plain(measurements: dict, style_color: str):
    
    time_data = pd.DataFrame({
        'Date': measurements['date'], 
        'Weight': measurements['weight'],
        'Macro1': measurements['macro1'], 
        'Macro2': measurements['macro2'], 
        'Macro3': measurements['macro3'] 
    })

    weight_chart = alt.Chart(time_data).mark_line(clip=True).mark_area(
        line={'color': style_color},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0), 
                alt.GradientStop(color=style_color, offset=1)],
                x1=1,
                x2=1,
                y1=1,
                y2=0
        )
        ).encode(
            alt.X('Date:T'),
            alt.Y('Weight:Q')
        )
    
    points_macro = alt.Chart(time_data).transform_fold(
        ['Weight', 'Macro1', 'Macro2', 'Macro3'],
        as_=["macros", "value"],
    ).mark_point(
        filled=True,
        size=100
    ).encode(
        x='Date:T',
        y='value:Q',
        color='macros:N'
        #color=alt.Color('macros', scale=alt.Scale(domain=['Weight', 'Macro1', 'Macro2', 'Macro3'], range=['red', 'steelblue', 'chartreuse', '#F4D03F'], type="ordinal"))
    ).properties(title='Weight and Macros Time Evolution').interactive()
    
    st.write(weight_chart + points_macro)

def macro_stack(measurements: dict, style_color: str):

    time_data = pd.DataFrame({
        'Date': measurements['date'], 
        'Weight': measurements['weight'],
        'Macro1': measurements['macro1'], 
        'Macro2': measurements['macro2'], 
        'Macro3': measurements['macro3'] 
    })

    stack = alt.Chart(time_data).transform_fold(
        ['Weight', 'Macro1', 'Macro2', 'Macro3'],
        as_=["macros", "value"],
    ).mark_area().encode(
    alt.X('Date:T'),
    alt.Y('sum(value):Q', stack='center', axis=None),
    alt.Color('macros:N')
    
    ).interactive()

    stack = alt.Chart(time_data).transform_fold(
        ['Macro1', 'Macro2', 'Macro3'],
        as_=["macros", "value"],
    ).mark_area(opacity=0.3).encode(
        x="Date:T",
        y=alt.Y("value:Q", stack=None),
        color="macros:N"
    ).properties(title='Macros - Stack Wiew').interactive()

    st.write(stack)