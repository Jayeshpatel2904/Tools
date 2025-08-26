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

# Load data from the first Excel file (Sheet1)
excel_file1 = filedialog.askopenfilename()
# excel_file2 = filedialog.askopenfilename()

# columns_to_keep2 = ['timestamp','Custom: NR_Cell_Global_Id','RRC_ConnEstabAtt_Sum','rlc_vol_dl']
sheet1 = pd.read_excel(excel_file1)
# sheet1 = pd.read_excel(excel_file1)

directory_path = os.path.dirname(excel_file1)

ACDMTable = pd.DataFrame(sheet1)

num_entries = len(ACDMTable)-1
num_entries = ACDMTable.shape[0]-1

num_unique_entries = ACDMTable['PACD ID'].nunique()


counts = ACDMTable['Reason'].value_counts()


# print(table)

print(counts)

print("Number of unique entries in the column:", num_unique_entries - 1)

print("Number of entries:", num_entries)

