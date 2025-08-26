import pandas as pd
from openpyxl import Workbook, load_workbook
from tkinter import filedialog
import os
import tkinter as tk
import datetime
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill

time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Load data from the first Excel file (Planet Export)
excel_file1 = filedialog.askopenfilename()


# columns_to_keep2 = ['timestamp','Custom: NR_Cell_Global_Id','RRC_ConnEstabAtt_Sum','rlc_vol_dl']

sites_sheet = pd.read_excel(excel_file1, sheet_name= "NRCellRelation")

# def From_KEY(raw):

#     raw['Mapping'] = raw['Mapping'][13:]



#     return (raw['Mapping'][0])


sites_sheet['NMapping'] = sites_sheet['Mapping'].str.slice(13)


sites_sheet['NMapping'] = sites_sheet['NMapping'].str.replace(' ', '')

sites_sheet['Source_to_Target'] = sites_sheet['NMapping'].str.split('>').str[0] + ">" + sites_sheet['NMapping'].str.split('>').str[1]
sites_sheet['Target_to_Source'] = sites_sheet['NMapping'].str.split('>').str[1] + ">" + sites_sheet['NMapping'].str.split('>').str[0]


directory_path = os.path.dirname(excel_file1)

excel_output_path = directory_path + '/NBRS_' + time + '.xlsx'
writer = pd.ExcelWriter(excel_output_path, engine='openpyxl')




Source_target = pd.DataFrame(sites_sheet['Target_to_Source'].copy())

Source_target.rename(columns={'Target_to_Source': 'Source_to_Target'}, inplace=True)

Source_target['Status'] = "BOTHWAY"

final = pd.merge(sites_sheet, Source_target, on='Source_to_Target', how='left')

final.drop(columns=['NMapping'], inplace=True)

final['Status'] = final['Status'].fillna('ONEWAY')

# Write the table to the Excel file
final.to_excel(writer, sheet_name='NBRS', index=False)


# Access the XlsxWriter workbook and worksheet objects
workbook = writer.book
worksheet = writer.sheets['NBRS']
writer.close()
