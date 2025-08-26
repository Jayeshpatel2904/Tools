import os
import pandas as pd
from tkinter import filedialog
import tkinter as tk

# Create a Tkinter root window (it will remain hidden)
root = tk.Tk()
root.withdraw()

# Ask the user to select the source folder
source_folder = filedialog.askdirectory(title="Select Source Folder")

# Exit if the user cancels the selection
if not source_folder:
    print("Source folder selection canceled.")
    exit()

# Read the Excel list containing values to be removed
values_excel_path = filedialog.askopenfilename()
values_df = pd.read_excel(values_excel_path)

# Specify the column name in both DataFrames
main_column_name = 'Site ID'
values_column_name = 'Site ID'

# Iterate through each file in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(source_folder, filename)
        
        # Read the main DataFrame
        main_xls = pd.ExcelFile(file_path)
        main_sheet_names = main_xls.sheet_names
        
        # Create a dictionary to store modified DataFrames
        modified_dfs = {}
        
        # Iterate through each sheet in the main Excel file
        for sheet_name in main_sheet_names:
            try:
                main_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Check if the specified column is present in the sheet
                if main_column_name not in main_df.columns:
                    print(f"Column '{main_column_name}' not found in '{filename}' - '{sheet_name}'. Skipping...")
                    continue
                
                # Filter out rows where the specific column value matches values in the list
                filtered_df = main_df[~main_df[main_column_name].isin(values_df[values_column_name])]
                
                # Store the modified DataFrame in the dictionary
                modified_dfs[sheet_name] = filtered_df
            except pd.errors.EmptyDataError:
                print(f"No data found in '{filename}' - '{sheet_name}'. Skipping...")
        
        # Save the modified DataFrames to separate Excel files
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        os.makedirs(output_folder, exist_ok=True)
        
        for sheet_name, df in modified_dfs.items():
            output_file_path = os.path.join(output_folder, f'{filename}_{sheet_name}_output.xlsx')
            df.to_excel(output_file_path, index=False)
