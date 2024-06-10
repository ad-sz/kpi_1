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

target_date = 20
target_week = 20
target_month = 20


def chart_week(filename_percent_corrected_week, target_week):
    # open csv file with needed data and create dataframe
    df_week_counts = pd.read_csv(filename_percent_corrected_week, sep=';')
    df_week_counts['percent_corrected_containers'] = df_week_counts['percent_corrected_containers'] * 100

    # create chart
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(
        go.Bar(
            x=df_week_counts['week'], 
            y=df_week_counts['percent_corrected_containers'], 
            name='Procent poprawianych kadzi', 
            marker=dict(color='blue'), 
            textposition='outside',  # position text outside the bars
        ),
        secondary_y=False,
    )

    fig.update_layout(
        title='Ilość wykonanych korekt i procent realizacji celu w tygodniach',
        xaxis_title='Tydzień',
        yaxis_title='Ilość wykonanych korekt',
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

    # fig.show()
    fig.write_html(filenames.filename_chart_percent_corrected_week)
    

chart_week(filenames.filename_percent_corrected_week, target_week)