"""create chart showing kpi by weeks"""

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


# upload "Premix" sheet from korekty excel file to DatFrame object
# remove first row from excel because have not needed informations (skiprows=1)
df_korekty = pd.read_excel(filenames.filename_korekty, sheet_name="Premix",dtype={'Nr partii': str}, skiprows=1)

# searching last fulfill element in collumn "index"
last_index_korekty = df_korekty['index'].last_valid_index()

# cut the DataFrame obiect on last fulfill element
df_korekty = df_korekty.iloc[:last_index_korekty + 1, :18]

# # designation columns which are needed for df_korekty
# df_korekty_needed_columns_for_kpi = [2, 3, 4]
df_korekty_needed_columns_for_kpi = ['index', 'Nr partii', 'Data kontroli']

# create DataFrame obiect with collums needed for kpi analysis
df_korekty = df_korekty.loc[:, df_korekty_needed_columns_for_kpi]

def quantity_checked (filename_processed_data):
    # open csv file with needed data and create dataframe
    df_processed_data = pd.read_csv(filename_processed_data, sep=';')

    # change collumns for date type
    df_processed_data['date_correction'] = pd.to_datetime(df_processed_data['date_correction'], errors='coerce')

    # leave only collumn with date for calculate quantity of corrections done
    df_processed_data_week = df_processed_data[['date_correction']].dropna()

    # change date for week number
    df_processed_data_week['week'] = df_processed_data_week['date_correction'].dt.strftime('%W')
    
    # count quantity of unique weeks
    df_week_counts = df_processed_data_week['week'].value_counts().reset_index()

    # change collumns names
    df_week_counts.columns = ['week', 'quantity']

    # sorting by weeks
    df_week_counts = df_week_counts.sort_values('week').reset_index(drop=True)
    

    # leave only collumn with date for calculate quantity of corrections done
    df_processed_data_month = df_processed_data[['date_correction']].dropna()

    # change date for month number
    df_processed_data_month['month'] = df_processed_data['date_correction'].dt.strftime('%M')
    
    # count quantity of unique months
    df_month_counts = df_processed_data_month['month'].value_counts().reset_index()

    # change collumns names
    df_month_counts.columns = ['month', 'quantity']

    # sorting by month
    df_month_counts = df_month_counts.sort_values('month').reset_index(drop=True)
    






quantity_checked(filenames.filename_processed_data)





#df_processed_data['batch_production'] = pd.to_datetime(df_processed_data['batch_production'], errors='coerce')

    # #grouping data by week number and sum of looses in kg for weeks numbers, remove axis name
    # df_dane_losses_week_losses_sum = df_dane_losses_week.groupby(df_dane_losses_week.columns[11])[df_dane_losses_week.columns[3]].sum().rename_axis(None)
    # #remove series name
    # df_dane_losses_week_losses_sum.name = None

    # #grouping data by week number and sum of inserts in kg for weeks numbers, remove axis name
    # df_dane_losses_week_insert_sum = df_dane_losses_week.groupby(df_dane_losses_week.columns[11])[df_dane_losses_week.columns[1]].sum().rename_axis(None)
    # #remove series name
    # df_dane_losses_week_insert_sum.name = None

    # #connecting both DataFrame obiects (df_dane_losses_week_losses_sum, df_dane_losses_week_insert_sum) in one
    # df_combined_week_looses_insert = pd.concat([df_dane_losses_week_losses_sum, df_dane_losses_week_insert_sum], axis=1)

    # #adding new column to df_combined_week_looses_insert with % of looses
    # df_combined_week_looses_insert[2] = df_combined_week_looses_insert.apply(lambda row: (row[0] / row[1]) * 100 if row[1] != 0 else 0, axis=1)

    # #create chart with two y axis
    # #create a subplot with two y axis
    # fig = make_subplots(specs=[[{"secondary_y": True}]])

    # #create chart for % of losses
    # fig.add_trace(
    #     go.Scatter(x=df_combined_week_looses_insert.index, y=df_combined_week_looses_insert.iloc[:, 2], 
    #             mode='markers+lines', name='% of losses', marker=dict(color='blue', size=10), hovertemplate='%{y:.1f}'),
    #     secondary_y=False,
    # )

    # #create secondary chart for kg of losses
    # fig.add_trace(
    #     go.Scatter(x=df_combined_week_looses_insert.index, y=df_combined_week_looses_insert.iloc[:, 0], 
    #             mode='markers', name='kg of losses', marker=dict(color='red', symbol='x', size=12), hovertemplate='%{y:.0f}'),
    #     secondary_y=True,
    # )

    # #adding labels
    # fig.update_layout(
    #     title_text='losses by weeks',
    #     xaxis_title='week',
    #     yaxis_title='% of losses',
    #     yaxis2_title='kg of losses',
    # )

    # #setting y(primary) axis range and ticks
    # fig.update_yaxes(range=[0, 10], tickvals=np.arange(0, 10.5, 1), secondary_y=False)

    # #setting y(secondary) axis properties
    # fig.update_yaxes(tickcolor='red', secondary_y=True)

    # #saving chart in HTML format
    # fig.write_html("D:/python_data/sherwin/losses/looses_by_week.html")