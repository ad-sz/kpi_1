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
import glob
import os
import filenames

# import kpi_create_charts

"""create DataFrame obiect from excel files and prepare data for analysis"""

def process_data(filename_rozliczenie_miesieczne, filename_folder,):
    # create list of excel files with data rozliczenie_miesieczne
    filename_paths = glob.glob(os.path.join(filename_folder, filename_rozliczenie_miesieczne))

    # create list for all dataframes from excel files
    data_frame_list = []

    # upload "dane" sheet from rozliczenie_miesieczne excel file to DatFrame object and put into the list data_frame_list
    # changing colums "NR.PRODUKCYJNY" on strings (dtype={'NR.PRODUKCYJNY': str})
    # remove first row from excel because have not needed informations (skiprows=1)
    for filename_path in filename_paths:
        df = pd.read_excel(filename_path, sheet_name="dane", dtype={'NR.PRODUKCYJNY': str}, skiprows=1)
        # searching last fulfill element in collumn "NR.PRODUKCYJNY"
        last_index_rozliczenie_miesieczne = df['NR.PRODUKCYJNY'].last_valid_index()
        # cut the DataFrame obiect on last fulfill element
        df = df.iloc[:last_index_rozliczenie_miesieczne + 1, :36]
        data_frame_list.append(df)

    # connecting all dataframes in one
    df_rozliczenie_miesieczne = pd.concat(data_frame_list, ignore_index=True)

    # # upload "dane" sheet from rozliczenie_miesieczne excel file to DatFrame object
    # # changing colums "NR.PRODUKCYJNY" on strings (dtype={'NR.PRODUKCYJNY': str})
    # # remove first row from excel because have not needed informations (skiprows=1)
    # df_rozliczenie_miesieczne = pd.read_excel(filename_rozliczenie_miesieczne, sheet_name="dane",dtype={'NR.PRODUKCYJNY': str} ,skiprows=1)

    # searching last fulfill element in collumn "NR.PRODUKCYJNY"
    last_index_rozliczenie_miesieczne = df_rozliczenie_miesieczne['NR.PRODUKCYJNY'].last_valid_index()

    # cut the DataFrame obiect on last fulfill element
    df_rozliczenie_miesieczne = df_rozliczenie_miesieczne.iloc[:last_index_rozliczenie_miesieczne + 1, :36]


    # designation columns which are needed for df_rozliczenie_miesieczne
    # df_rozliczenie_miesieczne_needed_columns_for_kpi = [0, 10, 18, 23, 25]
    df_rozliczenie_miesieczne_needed_columns_for_kpi = ['Lp', 'całkowita\nilość\nmixów', 'ilość ko-\nryg.mixów', 'KONEC PRODUCJI']

    # create DataFrame obiect with collums needed for kpi analysis
    df_rozliczenie_miesieczne = df_rozliczenie_miesieczne.loc[:, df_rozliczenie_miesieczne_needed_columns_for_kpi]

    # remove rows with not correct data format
    def validate_and_convert_date(df, column_index):
        valid_rows = []
        for index, row in df.iterrows():
            try:
                row.iloc[column_index] = pd.to_datetime(row.iloc[column_index], dayfirst=True)
                valid_rows.append(row)
            except:
                pass
        return pd.DataFrame(valid_rows)

    # change data type for date in column
    # df_rozliczenie_miesieczne.iloc[:, 4] = pd.to_datetime(df_rozliczenie_miesieczne.iloc[:, 4],dayfirst=True)
    df_rozliczenie_miesieczne = validate_and_convert_date(df_rozliczenie_miesieczne, 3)


    # create column with % value of corrected containers
    df_rozliczenie_miesieczne['percent_corrected_containers'] = df_rozliczenie_miesieczne['ilość ko-\nryg.mixów'] / df_rozliczenie_miesieczne['całkowita\nilość\nmixów']


    # rename collumns
    df_rozliczenie_miesieczne.rename(columns={
        'Lp': 'no',
        'całkowita\nilość\nmixów' : 'quantity_containers',
        'ilość ko-\nryg.mixów': 'quantity_corrected_containers',
        'KONEC PRODUCJI' : 'date_production',
    }, inplace=True)


    """create a new DataFrame for accuracy for week numbers"""
    # copy DataFrame
    df_processed_data_week = df_rozliczenie_miesieczne.copy()

    # change date for week number
    df_processed_data_week['week'] = df_processed_data_week['date_production'].dt.strftime('%W')
    df_processed_data_week.drop(columns=['date_production'], inplace=True)

    # group by week and calculate mean accuracy
    df_processed_data_week = df_processed_data_week.groupby('week').agg({'percent_corrected_containers': 'mean'}).reset_index()


    """create a new DataFrame for percent_corrected_containers for month numbers"""
    # copy DataFrame
    df_processed_data_month = df_rozliczenie_miesieczne.copy()

    # change date for month number
    df_processed_data_month['month'] = df_processed_data_month['date_production'].dt.strftime('%m')
    df_processed_data_month.drop(columns=['date_production'], inplace=True)

    # group by month and calculate mean percent_corrected_containers
    df_processed_data_month = df_processed_data_month.groupby('month').agg({'percent_corrected_containers': 'mean'}).reset_index()


    """create a new DataFrame for each day numbers"""
    # copy DataFrame
    df_processed_data_date = df_rozliczenie_miesieczne.copy()

    # group by date and calculate mean percent_corrected_containers
    df_processed_data_date = df_processed_data_date.groupby('date_production').agg({'percent_corrected_containers': 'mean'}).reset_index()



    """save ready dataframes to csv files"""
    df_processed_data_week.to_csv(filenames.filename_percent_corrected_week, sep=';', index=False)
    df_processed_data_month.to_csv(filenames.filename_percent_corrected_month, sep=';', index=False)
    df_processed_data_date.to_csv(filenames.filename_percent_corrected_date, sep=';', index=False)

process_data(filenames.filename_rozliczenie_miesieczne, filenames.filename_folder,)