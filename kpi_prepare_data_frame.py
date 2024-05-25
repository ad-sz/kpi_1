"""Kpi analysis - create charts"""
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

def process_data():
    # create list of excel files with data rozliczenie_miesieczne
    filename_paths = glob.glob(os.path.join(filenames.filename_folder, filenames.filename_rozliczenie_miesieczne))

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
    # last_index_rozliczenie_miesieczne = df_rozliczenie_miesieczne['NR.PRODUKCYJNY'].last_valid_index()

    # cut the DataFrame obiect on last fulfill element
    # df_rozliczenie_miesieczne = df_rozliczenie_miesieczne.iloc[:last_index_rozliczenie_miesieczne + 1, :36]


    # designation columns which are needed for df_rozliczenie_miesieczne
    # df_rozliczenie_miesieczne_needed_columns_for_kpi = [0, 10, 18, 23, 25]
    df_rozliczenie_miesieczne_needed_columns_for_kpi = ['Lp', 'ilość ko-\nryg.mixów', 'NR.PRODUKCYJNY', 'INDEX', 'KONEC PRODUCJI']

    # create DataFrame obiect with collums needed for kpi analysis
    df_rozliczenie_miesieczne = df_rozliczenie_miesieczne.loc[:, df_rozliczenie_miesieczne_needed_columns_for_kpi]

    # change data type for date in column 3
    df_rozliczenie_miesieczne.iloc[:, 4] = pd.to_datetime(df_rozliczenie_miesieczne.iloc[:, 4],dayfirst=True)

    # setting value of quantity correction mixers for 1 if value is higher than 1
    df_rozliczenie_miesieczne.iloc[:, 1] = df_rozliczenie_miesieczne.iloc[:, 1].apply(lambda x: x if x <= 1 else 1)

    # removing blank characters from column with index and batch number
    df_rozliczenie_miesieczne.iloc[:, 2] = df_rozliczenie_miesieczne.iloc[:, 2].apply(lambda x: str(x).strip())
    df_rozliczenie_miesieczne.iloc[:, 2] = df_rozliczenie_miesieczne.iloc[:, 2].apply(lambda x: str(x).strip()[-3:])
    df_rozliczenie_miesieczne.iloc[:, 3] = df_rozliczenie_miesieczne.iloc[:, 3].apply(lambda x: str(x).strip())
    df_rozliczenie_miesieczne.iloc[:, 3] = df_rozliczenie_miesieczne.iloc[:, 3].apply(lambda x: str(x).upper())


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

    # change data type for date in column 2
    df_korekty.iloc[:, 2] = pd.to_datetime(df_korekty.iloc[:, 2],dayfirst=True)

    # removing blank characters from column with index and batch number
    df_korekty.iloc[:, 1] = df_korekty.iloc[:, 1].apply(lambda x: str(x).strip())
    df_korekty.iloc[:, 1] = df_korekty.iloc[:, 1].apply(lambda x: str(x).strip()[-3:])
    df_korekty.iloc[:, 0] = df_korekty.iloc[:, 0].apply(lambda x: str(x).strip())
    df_korekty.iloc[:, 0] = df_korekty.iloc[:, 0].apply(lambda x: str(x).upper())


    # merge data frames df_rozliczenie_miesieczne and df_korekty by index and batch, save all rows from df_korekty (how='right')
    df_rozliczenie_miesieczne_df_korekty = pd.merge(df_rozliczenie_miesieczne, df_korekty, left_on=["INDEX", "NR.PRODUKCYJNY"], right_on=["index", "Nr partii"], how='right')


    # rename collumns
    df_rozliczenie_miesieczne_df_korekty.rename(columns={
        'Lp': 'no',
        'ilość ko-\nryg.mixów': 'if_corrected_on_the_extruder',
        'NR.PRODUKCYJNY': 'batch_production',
        'INDEX': 'index_production',
        'KONEC PRODUCJI' : 'date_production',
        'index': 'index_correction',
        'Nr partii': 'batch_correction',
        'Data kontroli': 'date_correction'
    }, inplace=True)

    # save ready dataframe to csv file
    df_rozliczenie_miesieczne_df_korekty.to_csv(filenames.filename_processed_data, sep=';', index=False)