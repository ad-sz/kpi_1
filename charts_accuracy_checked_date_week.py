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

target_accuracy = 50

def chart_week(filename_accuracy_week, target_week):
    # open csv file with needed data and create dataframe
    df_week_accuracy = pd.read_csv(filename_accuracy_week, sep=';')

    # create chart
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(
        go.Bar(
            x=df_week_accuracy['week'], 
            y=df_week_accuracy['accuracy'], 
            name='procent skuteczności korekt', 
            marker=dict(color='blue'), 
            hovertemplate='%{y:.1f}',
            text=df_week_accuracy['accuracy'].apply(lambda x: f'{x:.1f}%'),  # adding percentage text
            textposition='outside',  # position text outside the bars
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df_week_accuracy['week'], 
            y=[target_accuracy]*len(df_week_accuracy), 
            mode='lines', 
            name='Cel', 
            line=dict(color='red', dash='dash'), 
            hovertemplate='%{y:.1f}'
        ),
        secondary_y=False,
    )

    fig.update_layout(
        title='Procent skuteczności korekt',
        xaxis_title='Tydzień',
        yaxis_title='Procent skuteczności korekt',
        barmode='group',  # group bars together
    )

    fig.update_xaxes(
        dtick='W1',  # set x-axis to increment weekly
    )

    fig.update_yaxes(
        dtick=5,  # set left y-axis to increment by 5
        secondary_y=False
    )

    # fig.show()
    fig.write_html(filenames.filename_chart_accuracy_week)
    

chart_week(filenames.filename_accuracy_week, target_accuracy)