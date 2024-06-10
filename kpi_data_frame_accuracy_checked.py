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
import re
import filenames


def accuracy_checked(filename_processed_data):
    # open csv file with needed data and create dataframe
    df_accuracy = pd.read_csv(filename_processed_data, sep=';')

    # leave rows with needed data (row with value in 'index_production', 'index_correction')
    df_accuracy_filtered = df_accuracy.dropna(subset=['index_production', 'index_correction'])
    
    # change collumns for date type
    df_accuracy_filtered['date_correction'] = pd.to_datetime(df_accuracy_filtered['date_correction'],dayfirst=False, errors='coerce')
    df_accuracy_filtered['date_production'] = pd.to_datetime(df_accuracy_filtered['date_production'],dayfirst=False, errors='coerce')

    # leave only needed collumns for calculate accuracy of corrections done
    df_accuracy_filtered = df_accuracy_filtered[['if_corrected_on_the_extruder', 'date_production', 'reason_correction']].dropna()
    
    # change collumn name
    df_accuracy_filtered.rename(columns={'if_corrected_on_the_extruder': 'accuracy'}, inplace=True)

    # change namer reason of correction for english
    df_accuracy_filtered.loc[df_accuracy_filtered['reason_correction'].str.contains(r'polysk', case=False, regex=True), 'reason_correction'] = 'gloss'
    df_accuracy_filtered.loc[df_accuracy_filtered['reason_correction'].str.contains(r'kolor', case=False, regex=True), 'reason_correction'] = 'color'
    df_accuracy_filtered['reason_correction'] = df_accuracy_filtered['reason_correction'].apply(lambda x: x if x in ['gloss', 'color'] else np.nan)

    # changing values 0.0 on 100 and 1.0 on 0 in collumn 'accuracy' for having % of accuracy
    # df_accuracy_filtered['accuracy'] = df_accuracy_filtered['accuracy'].apply(lambda x: 0 if x == 1.0 else 100)
    df_accuracy_filtered['accuracy'] = df_accuracy_filtered.apply(lambda row: 0 if row['accuracy'] == 1.0 and row['reason_correction'] in ['gloss', 'color'] else (100 if row['accuracy'] == 0.0 else 100), axis=1)

    # adding columns with gloss and color
    df_accuracy_filtered['gloss'] = df_accuracy_filtered['reason_correction'].apply(lambda x: 1 if x == 'gloss' else 0)
    df_accuracy_filtered['color'] = df_accuracy_filtered['reason_correction'].apply(lambda x: 1 if x == 'color' else 0)


    """create a new DataFrame for accuracy for week numbers"""
    # copy DataFrame
    df_processed_data_week = df_accuracy_filtered.copy()
    

    # change date for week number
    df_processed_data_week['week'] = df_processed_data_week['date_production'].dt.strftime('%W')
    df_processed_data_week.drop(columns=['date_production'], inplace=True)

    # group by week and calculate mean accuracy
    df_processed_data_week = df_processed_data_week.groupby('week').agg({'accuracy': 'mean', 'gloss': 'sum', 'color': 'sum'}).reset_index()


    """create a new DataFrame for accuracy for month numbers"""
    # copy DataFrame
    df_processed_data_month = df_accuracy_filtered.copy()

    # change date for month number
    df_processed_data_month['month'] = df_processed_data_month['date_production'].dt.strftime('%m')
    df_processed_data_month.drop(columns=['date_production'], inplace=True)

    # group by month and calculate mean accuracy
    df_processed_data_month = df_processed_data_month.groupby('month').agg({'accuracy': 'mean', 'gloss': 'sum', 'color': 'sum'}).reset_index()


    """create a new DataFrame for each day numbers"""
    # copy DataFrame
    df_processed_data_date = df_accuracy_filtered.copy()

    # group by date and calculate mean accuracy
    df_processed_data_date = df_processed_data_date.groupby('date_production').agg({'accuracy': 'mean', 'gloss': 'sum', 'color': 'sum'}).reset_index()



    """save ready dataframes to csv files"""
    df_processed_data_week.to_csv(filenames.filename_accuracy_week, sep=';', index=False)
    df_processed_data_month.to_csv(filenames.filename_accuracy_month, sep=';', index=False)
    df_processed_data_date.to_csv(filenames.filename_accuracy_date, sep=';', index=False)




accuracy_checked(filenames.filename_processed_data)