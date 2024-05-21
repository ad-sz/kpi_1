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

# import kpi_create_charts

"""create DataFrame obiect from excel files and prepare data for analysis"""

# path to the excel files with data
filename_rozliczenie_miesieczne = "D:/python_data/projekt/kpi/kpi_data/rozliczenie_miesieczne.xlsx"
filename_korekty = "D:/python_data/projekt/kpi/kpi_data/korekty.xlsx"

# upload "dane" sheet from rozliczenie_miesieczne excel file to DatFrame object
# changing colums "NR.PRODUKCYJNY" on strings (dtype={'NR.PRODUKCYJNY': str})
# remove first row from excel because have not needed informations (skiprows=1)
df_rozliczenie_miesieczne = pd.read_excel(filename_rozliczenie_miesieczne, sheet_name="dane",dtype={'NR.PRODUKCYJNY': str} ,skiprows=1)

# searching last fulfill element in collumn "NR.PRODUKCYJNY"
last_index_rozliczenie_miesieczne = df_rozliczenie_miesieczne['NR.PRODUKCYJNY'].last_valid_index()

# cut the DataFrame obiect on last fulfill element
df_rozliczenie_miesieczne = df_rozliczenie_miesieczne.iloc[:last_index_rozliczenie_miesieczne + 1, :36]

# designation columns which are needed for df_rozliczenie_miesieczne
df_rozliczenie_miesieczne_needed_columns_for_kpi = [0, 10, 23, 25]

# create DataFrame obiect with collums needed for kpi analysis
df_rozliczenie_miesieczne = df_rozliczenie_miesieczne.iloc[:, df_rozliczenie_miesieczne_needed_columns_for_kpi]

# change data type for date in column 3
df_rozliczenie_miesieczne.iloc[:, 3] = pd.to_datetime(df_rozliczenie_miesieczne.iloc[:, 3],dayfirst=True)

# setting value of quantity correction mixers for 1 if value is higher than 1
df_rozliczenie_miesieczne.iloc[:, 1] = df_rozliczenie_miesieczne.iloc[:, 1].apply(lambda x: x if x <= 1 else 1)


# upload "Premix" sheet from korekty excel file to DatFrame object
# remove first row from excel because have not needed informations (skiprows=1)
df_korekty = pd.read_excel(filename_korekty, sheet_name="Premix",skiprows=1)

# searching last fulfill element in collumn "index"
last_index_korekty = df_korekty['index'].last_valid_index()

# cut the DataFrame obiect on last fulfill element
df_korekty = df_korekty.iloc[:last_index_korekty + 1, :18]

# designation columns which are needed for df_korekty
df_korekty_needed_columns_for_kpi = [2, 4]

# create DataFrame obiect with collums needed for kpi analysis
df_korekty = df_korekty.iloc[:, df_korekty_needed_columns_for_kpi]

# change data type for date in column 2
df_korekty.iloc[:, 1] = pd.to_datetime(df_korekty.iloc[:, 1],dayfirst=True)

print(df_rozliczenie_miesieczne.head())
print("")
print(df_korekty.head())





# #setting value of looses for 0 if value is less than 0
# df_dane_losses.iloc[:, 3] = df_dane_losses.iloc[:, 3].apply(lambda x: max(x, 0))


# """create chart showing looses in % by weeks"""
# def_looses_weeks.looses_weeks(df_dane_losses)

# """create chart showing looses in % by weeks for each line"""
# def_looses_weeks_lines.looses_weeks_lines(df_dane_losses)





# #wyświetlanie indeksów kolumn
# def display_column_indices(df):
#     """
#     Wyświetla indeksy i nazwy kolumn w DataFrame.
    
#     Parametry:
#     df (pd.DataFrame): Obiekt DataFrame, którego kolumny chcemy wyświetlić.
    
#     Zwraca:
#     None
#     """
#     for idx, col in enumerate(df.columns):
#         print(f"Indeks: {idx}, Kolumna: {col}")


# display_column_indices(df_korekty)
# print("")
# print("")
# display_column_indices(df_rozliczenie_miesieczne)