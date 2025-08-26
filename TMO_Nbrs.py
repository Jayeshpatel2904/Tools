
import pandas as pd
from openpyxl import Workbook, load_workbook
from tkinter import filedialog, messagebox
import os
import tkinter as tk
import datetime
from openpyxl.styles import PatternFill

file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])

# # Load the Excel file
# file_path = "FAY_TMO NBrs Relation.xlsx"  # Update with the correct path if needed
xls = pd.ExcelFile(file_path)

# Read both sheets
sheet1 = xls.parse("Sheet1")
sheet2 = xls.parse("Sheet2")

# Merge using 'sitename' as the key
combined_df = pd.merge(sheet1, sheet2, on='sitename', how='inner')


# Convert all boolean values to lowercase strings
def lowercase_bools(df):
    for col in df.columns:
        if df[col].dtype == bool or df[col].astype(str).isin(["True", "False"]).any():
            df[col] = df[col].apply(lambda x: str(x).lower() if str(x) in ["True", "False"] else x)
    return df

combined_df = lowercase_bools(combined_df)

# Optional: Save to a new Excel file
time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
directory_path = os.path.dirname(file_path)
excel_output_path = directory_path + '/TMO_N26_NBRS_' + time + '.xlsx'
combined_df.to_excel(excel_output_path, index=False)


print(f"Combined file saved as: {excel_output_path}")
