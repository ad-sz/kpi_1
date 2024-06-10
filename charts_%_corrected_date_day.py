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

target_date = 6
target_week = 42
target_month = 180


def chart_date(filename_checked_date, target_date):
    # open csv file with needed data and create dataframe
    df_date_counts = pd.read_csv(filename_checked_date, sep=';')
    
    # change date collumn on date time
    df_date_counts['date'] = pd.to_datetime(df_date_counts['date'], format='%Y-%m-%d')

    # filtring only day from current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    df_date_counts = df_date_counts[(df_date_counts['date'].dt.month == current_month) & (df_date_counts['date'].dt.year == current_year)]

    # adding collumn with % of target
    df_date_counts['percentage_of_goal'] = (df_date_counts['quantity'] / target_date) * 100


    # create chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df_date_counts['date'], 
            y=df_date_counts['quantity'], 
            name='Ilość wykonanych sprawdzeń', 
            marker=dict(color='blue'), 
            hovertemplate='%{y:.1f}',
            text=df_date_counts['percentage_of_goal'].apply(lambda x: f'{x:.1f}%'),  # adding percentage text
            textposition='outside',  # position text outside the bars
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df_date_counts['date'], 
            y=[target_date]*len(df_date_counts), 
            mode='lines', 
            name='Cel', 
            line=dict(color='red', dash='dash'), 
            hovertemplate='%{y:.1f}'
        ),
        secondary_y=False,
    )

    fig.update_layout(
        title='Ilość wykonanych korekt i procent realizacji celu w tygodniach',
        xaxis_title='Dzień',
        yaxis_title='Ilość wykonanych korekt',
        yaxis2_title='Procent realizacji celu',
        barmode='group',  # group bars together
    )

    fig.update_xaxes(
        dtick='W1',  # set x-axis to increment dayly
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
    fig.write_html(filenames.filename_chart_date)
    

chart_date(filenames.filename_checked_date, target_date)