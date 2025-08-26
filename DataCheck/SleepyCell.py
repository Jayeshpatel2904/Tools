from openpyxl.drawing.image import Image
from openpyxl.chart import BarChart, Reference, LineChart
import pandas as pd
from openpyxl import Workbook, load_workbook
from tkinter import filedialog
import os
import tkinter as tk
import datetime
import openpyxl
import PySimpleGUI as sg


time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Load data from the first Excel file (Sheet1)
excel_file1 = filedialog.askopenfilename()
excel_file2 = filedialog.askopenfilename()

# columns_to_keep2 = ['timestamp','Custom: NR_Cell_Global_Id','RRC_ConnEstabAtt_Sum','rlc_vol_dl']
sheet1 = pd.read_csv(excel_file1)

filtered_df = sheet1[sheet1['label_aoi'].isin(['RDU', 'CLT'])]

filtered_df.rename(columns={'nrcgi': 'Custom: NR_Cell_Global_Id'}, inplace=True)

# print(filtered_df)

# Load data from the second Excel file (specific tab and column)
# excel_file2 = filedialog.askopenfilename()
sheet2_tab = 'Sectors'  # Change to the name of the tab in file2.xlsx
column_to_join_from_sheet2 = 'Custom: NR_Cell_Global_Id'  # Change to the column name in sheet2.xlsx

columns_to_keep1 = ['Custom: NR_Cell_Global_Id', 'Custom: NR_Cell_Name','DUID']

# Read only the specified column from the second Excel file
sheet2_column = pd.read_excel(excel_file2, sheet_name=sheet2_tab, usecols=columns_to_keep1)


# merged_data = sheet1.merge(sheet2_column, left_on='Custom: NR_Cell_Global_Id', right_index=True)

result = pd.merge(filtered_df, sheet2_column, on='Custom: NR_Cell_Global_Id', how='inner')

result['Custom: NR_Cell_Global_Id'] = "x" + result['Custom: NR_Cell_Global_Id'].astype(str).str[0:]

directory_path = os.path.dirname(excel_file1)

# pivot_table = pd.DataFrame(sheet1)


# Create a new Excel file using XlsxWriter
excel_output_path = directory_path + '/SleepyCell_' + time + '.xlsx'
result.to_excel(excel_output_path, index=False)

sg.popup('File Saved')   