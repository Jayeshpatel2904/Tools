import pandas as pd
from tkinter import filedialog
import os


# Read the main Excel file into a dictionary of DataFrames, where keys are sheet names
main_excel_path = filedialog.askopenfilename()
main_xls = pd.ExcelFile(main_excel_path)
main_sheet_names = main_xls.sheet_names

directory_path = os.path.dirname(main_excel_path)

excel_output_path = directory_path + '/Output.xlsx'

# Read the Excel list containing values to be removed
values_excel_path = filedialog.askopenfilename()
values_df = pd.read_excel(values_excel_path)

# Specify the column name in both DataFrames
main_column_name = 'Site ID'
values_column_name = 'Site ID'

# Create a dictionary to store modified DataFrames
modified_dfs = {}

# Iterate through each sheet in the main Excel file
for sheet_name in main_sheet_names:

    if sheet_name.lower() == 'summary':
            continue

    # Read the main DataFrame
    main_df = pd.read_excel(main_excel_path, sheet_name=sheet_name)
    
    # Filter out rows where the specific column value matches values in the list
    filtered_df = main_df[~main_df[main_column_name].isin(values_df[values_column_name])]
    
    # Store the modified DataFrame in the dictionary
    modified_dfs[sheet_name] = filtered_df

# Save the modified DataFrames back to the Excel file
with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
    for sheet_name, df in modified_dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)