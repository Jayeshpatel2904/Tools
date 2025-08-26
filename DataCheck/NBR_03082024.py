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

# Load data from the first Excel file (USM EXPORT)
excel_file2 = filedialog.askopenfilename()


# Load data from the first Excel file (PLANET NBRS EXPORT)
excel_file3 = filedialog.askopenfilename()

# columns_to_keep2 = ['timestamp','Custom: NR_Cell_Global_Id','RRC_ConnEstabAtt_Sum','rlc_vol_dl']

sites_sheet = pd.read_excel(excel_file1, sheet_name= "Sites")

sectors_sheet = pd.read_excel(excel_file1, sheet_name="Sectors")

specific_columns = sectors_sheet[['Site ID', 'Custom: Local_Cell_Id', 'Custom: NR_Cell_Name']]

directory_path = os.path.dirname(excel_file2)

Vlookup_Table = pd.merge(specific_columns, sites_sheet[['Site ID', 'Custom: gNodeB_Id']], on='Site ID', how='left')

def KEY(raw):
    return ((str(raw['Custom: gNodeB_Id']) + "_"  + str(raw['Custom: Local_Cell_Id'])))

Vlookup_Table['From_KEY'] = Vlookup_Table.apply(KEY, axis=1)

Vlookup_Table = Vlookup_Table[['From_KEY', 'Custom: NR_Cell_Name']]

def From_KEY(raw):
    return ((str(raw['gnodeb-id']) + "_"  + str(raw['cell-identity'])))

def To_KEY(raw):
    return ((str(raw['neighbor-gnb-id']) + "_"  + str(raw['neighbor-gnb-cell-identity'])))

sheet1 = pd.read_excel(excel_file2)

sheet1['From_KEY'] = sheet1.apply(From_KEY, axis=1)

final_Sheet1 = pd.merge(sheet1, Vlookup_Table, on='From_KEY', how='left')

final_Sheet1.rename(columns={'Custom: NR_Cell_Name': 'From_NR_Cell_Name'}, inplace=True)

excel_output_path = directory_path + '/NBRs_' + time + '.csv'

Vlookup_Table.rename(columns={'From_KEY': 'To_KEY'}, inplace=True)

final_Sheet1['To_KEY'] = final_Sheet1.apply(To_KEY, axis=1)

final_Sheet1 = pd.merge(final_Sheet1, Vlookup_Table, on='To_KEY', how='left')

final_Sheet1.rename(columns={'Custom: NR_Cell_Name': 'To_NR_Cell_Name'}, inplace=True)


excel_output_path1 = directory_path + '/USMNBRs_' + time + '.csv'


final_Sheet2 = pd.merge(final_Sheet1, Vlookup_Table, on='To_KEY', how='left')


def TARGET_NBRS_KEY(raw):
    return ((str(raw['From_NR_Cell_Name']) + "_"  + str(raw['Custom: NR_Cell_Name'])))


final_Sheet2['TARGET_NBRS_KEY'] = final_Sheet2.apply(TARGET_NBRS_KEY, axis=1)


NRNBrs_sheet = pd.read_excel(excel_file3, sheet_name= "NR_NR_Neighbors")


def NR_TARGET_NBRS_KEY(raw):
    return ((str(raw['Server Cell Name']) + "_"  + str(raw['Neighbor Cell Name'])))

NRNBrs_sheet['TARGET_NBRS_KEY'] = NRNBrs_sheet.apply(NR_TARGET_NBRS_KEY, axis=1)


final_Sheet3 = pd.merge(NRNBrs_sheet, final_Sheet2, on='TARGET_NBRS_KEY', how='left')


def MISSING(raw):
    raw['serverid'] = ((str(raw['Server Site ID']) + "_"  + str(raw['Server Carrier ID'])))
    raw['Nbrid'] = ((str(raw['Neighbor Site ID']) + "_"  + str(raw['Neighbor Carrier ID'])))

    if raw['serverid'] == raw['Nbrid'] and pd.isna(raw['gnodeb-id']):
        return ("MISSING")
    
    else:
        return ("AVAILABLE")

final_Sheet3['MISSING'] = final_Sheet3.apply(MISSING, axis=1)


final_Sheet1.to_csv(excel_output_path1, index=False)

final_Sheet3.to_csv(excel_output_path, index=False)
print("Excel file successfully created with data.")