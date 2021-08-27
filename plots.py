import altair as alt
from altair.vegalite.v4.schema.channels import Color
import pandas as pd
import streamlit as st

def get_slope_color(values: list, reverse=False) -> list:
    green = '#3DF900'
    red = '#F90004'
    yellow = '#F9E300'
    gray = '#606060'
    
    colors = [gray]
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
    
def single_plot(measurements: dict, yvar: str, yvar_name: str, plot_title: str, style_color: str, reverse_bullets=False):
    
    time_data = pd.DataFrame({
        'Date': measurements['date'], 
        yvar_name: measurements[yvar],
        'color': get_slope_color(measurements[yvar], reverse=reverse_bullets)
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
        ).properties(title=plot_title).interactive()

    circles = alt.Chart(time_data).mark_point(
        filled=True,
        size=100
    ).encode(
        x='Date:T',
        y=f'{yvar_name}:Q',
        color = alt.Color('color', legend=None, scale=None)
    ).properties(title=plot_title).interactive()

    st.write(chart + circles)

def macro_plain(measurements: dict, style_color: str):
    
    time_data = pd.DataFrame({
        'Date': measurements['date'], 
        'Weight': measurements['weight'],
        'weight_color_bullets': get_slope_color(measurements['weight'], reverse=False),
        'Carbo': measurements['carbo'], 
        'Proteins': measurements['proteins'], 
        'Fat': measurements['fat']
    })

    weight_chart = alt.Chart(time_data).mark_line(clip=True).mark_area(
        opacity = 0.3,
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
        ).interactive()

    weight_circles = alt.Chart(time_data).mark_point(
        filled=False,
        size=80,
        opacity=0.7
    ).encode(
        x='Date:T',
        y='Weight:Q',
        color = alt.Color('weight_color_bullets', legend=False, scale=None)
    ).interactive()
    
    orange = '#ff7f0e'
    green = '#2ca02c'
    sky = '#17becf'
    color_range = [orange, green, sky]

    macro = alt.Chart(time_data).transform_fold(
        ['Carbo', 'Proteins', 'Fat'],
        as_=["macros", "value"],
    ).mark_line(
        size=3,
        opacity=0.7
    ).encode(
        x='Date:T',
        y=alt.Y("value:Q"),
        color=alt.Color('macros:N', scale=alt.Scale(domain=['Carbo', 'Proteins', 'Fat'], range=color_range, type="ordinal"))
    ).properties(title='Weight and Macros Time Evolution').interactive()
    
    st.write(macro + weight_chart)

def macro_stack(measurements: dict):

    time_data = pd.DataFrame({
        'Date': measurements['date'], 
        'Weight': measurements['weight'],
        'Carbo': measurements['carbo'], 
        'Proteins': measurements['proteins'], 
        'Fat': measurements['fat'] 
    })

    orange = '#ff7f0e'
    green = '#2ca02c'
    sky = '#17becf'
    color_range = [orange, green, sky]

    stack = alt.Chart(time_data).transform_fold(
        ['Carbo', 'Proteins', 'Fat'],
        as_=["macros", "Macro"],
    ).mark_area(opacity=0.3).encode(
        x="Date:T",
        y=alt.Y("Macro:Q", stack=True),
        color=alt.Color('macros:N', scale=alt.Scale(domain=['Carbo', 'Proteins', 'Fat'], range=color_range, type="ordinal"))
    ).properties(title='Macros - Stack Wiew').interactive()

    st.write(stack)

def single_histo_with_mean(measurements: dict, xvar: str, xvar_name: str, plot_title: str, style_color: str):

    time_data = pd.DataFrame({xvar_name: measurements[xvar]})

    bar = alt.Chart(time_data).mark_bar(
        opacity=0.8,
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
            x=alt.X(f"{xvar_name}:Q", bin=True),
            y='count()'
        ).properties(title=plot_title).interactive()

    rule = alt.Chart(time_data).mark_rule(color='red').encode(
        x=f"mean({xvar_name}):Q",
        size=alt.value(5)
    )

    st.write(bar+rule)

def correlation_plot(measurements: dict, xvar: str, xvar_name: str, yvar: str, yvar_name: str, plot_title: str, style_color: str):

    data = pd.DataFrame({
        xvar_name: measurements[xvar],
        yvar_name: measurements[yvar]
    })

    corr_plot = alt.Chart(data).mark_point(
        filled=False,
        size=80,
        color=style_color,
        opacity=0.8
    ).encode(
        x=xvar_name,
        y=yvar_name
    ).properties(title=plot_title).interactive()

    st.write(corr_plot)

def weight_macro_correlation_plot(measurements: dict):

    data = pd.DataFrame({
        'Weight': measurements['weight'],
        'Carbo': measurements['carbo'], 
        'Proteins': measurements['proteins'], 
        'Fat': measurements['fat'] 
    })

    orange = '#ff7f0e'
    green = '#2ca02c'
    sky = '#17becf'
    color_range = [orange, green, sky]

    corr_plot = alt.Chart(data).transform_fold(
        ['Carbo', 'Proteins', 'Fat'],
        as_=["macros", "Macro"],
    ).mark_point(
        filled=False,
        size=80,
        opacity=0.8
    ).encode(
        x='Weight',
        y=alt.Y("Macro:Q"),
        color=alt.Color('macros:N', scale=alt.Scale(domain=['Carbo', 'Proteins', 'Fat'], range=color_range, type="ordinal"))
    ).properties(title='Weight and Macros correlation').interactive()

    st.write(corr_plot)