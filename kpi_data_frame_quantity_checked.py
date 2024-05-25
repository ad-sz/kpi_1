"""create data frames for quantity checked by date, weeks, months"""

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


def quantity_checked (filename_korekty):
    # open excel file with needed data and create dataframe
    df_korekty = pd.read_excel(filenames.filename_korekty, sheet_name="Premix",dtype={'Nr partii': str}, skiprows=1)

    # searching last fulfill element in collumn "index"
    last_index_korekty = df_korekty['index'].last_valid_index()

    # cut the DataFrame obiect on last fulfill element
    df_korekty = df_korekty.iloc[:last_index_korekty + 1, :18]

    # leave only collumn with date for calculate quantity of corrections done
    df_processed_data = df_korekty[['Data kontroli']].dropna()

    # change collumns for date type
    df_processed_data['Data kontroli'] = pd.to_datetime(df_processed_data['Data kontroli'],dayfirst=True, errors='coerce')


    # create a new DataFrame for week numbers
    df_processed_data_week = df_processed_data.copy()

    # change date for week number
    df_processed_data_week['week'] = df_processed_data['Data kontroli'].dt.strftime('%W')

    # count quantity of unique weeks
    df_week_counts = df_processed_data_week['week'].value_counts().reset_index()

    # change collumns names
    df_week_counts.columns = ['week', 'quantity']

    # sorting by weeks
    df_week_counts = df_week_counts.sort_values('week').reset_index(drop=True)
    


    # create a new DataFrame for month numbers
    df_processed_data_month = df_processed_data.copy()

    # change date for month number
    df_processed_data_month['month'] = df_processed_data['Data kontroli'].dt.strftime('%m')

    # count quantity of unique months
    df_month_counts = df_processed_data_month['month'].value_counts().reset_index()

    # change collumns names
    df_month_counts.columns = ['month', 'quantity']

    # sorting by months
    df_month_counts = df_month_counts.sort_values('month').reset_index(drop=True)


    # create a new DataFrame for each day numbers
    df_date_counts = df_processed_data['Data kontroli'].dt.date.value_counts().reset_index()

    # change collumns names
    df_date_counts.columns = ['date', 'quantity']

    # sorting by dates
    df_date_counts = df_date_counts.sort_values('date').reset_index(drop=True)


    # save ready dataframes to csv files
    df_week_counts.to_csv(filenames.filename_checked_week, sep=';', index=False)
    df_month_counts.to_csv(filenames.filename_checked_month, sep=';', index=False)
    df_date_counts.to_csv(filenames.filename_checked_date, sep=';', index=False)




quantity_checked(filenames.filename_korekty)