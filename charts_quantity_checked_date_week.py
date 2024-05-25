import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from bokeh.plotting import figure, output_file, save
from plotly.tools import mpl_to_plotly
import plotly.offline as py_offline
import plotly.io as pio
import mpld3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import filenames

target_date = 9
target_week = 30
target_month = 180


def chart_week(filename_checked_week, target_week):
    # open csv file with needed data and create dataframe
    df_week_counts = pd.read_csv(filename_checked_week, sep=';')
    
    # adding collumn with % of target
    df_week_counts['percentage_of_goal'] = (df_week_counts['quantity'] / target_week) * 100


    # create chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=df_week_counts['week'], y=df_week_counts['quantity'], 
            name='Ilość wykonanych sprawdzeń', marker=dict(color='blue'), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_week_counts['week'], y=[target_week]*len(df_week_counts), 
                mode='lines', name='Cel', line=dict(color='red', dash='dash'), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=df_week_counts['week'], y=df_week_counts['percentage_of_goal'], 
            name='Procent realizacji celu', marker=dict(color='green'), hovertemplate='%{y:.1f}%'),
        secondary_y=True,
    )

    fig.update_layout(
        title='Ilość wykonanych korekt i procent realizacji celu w tygodniach',
        xaxis_title='Tydzień',
        yaxis_title='Ilość wykonanych korekt',
        yaxis2_title='Procent realizacji celu',
        barmode='group'  # group bars together
    )

    fig.update_xaxes(
        dtick='W1',  # set x-axis to increment weekly
    )

    fig.update_yaxes(
        dtick=2,  # set left y-axis to increment by 2
        secondary_y=False
    )

    fig.update_yaxes(
        dtick=5,  # set right y-axis to increment by 5
        secondary_y=True
    )

    fig.show()
    fig.write_html(filenames.filename_chart_week)
    

chart_week(filenames.filename_checked_week, target_week)