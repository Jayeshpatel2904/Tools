import os
import pandas as pd
from tkinter import filedialog
import tkinter as tk


def merge_specific_sheet(folder_path, sheets_to_merge, output_file):
    # Initialize an empty DataFrame to store the merged data
    merged_data = pd.DataFrame()

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):  # Assuming the files are in Excel format
            file_path = os.path.join(folder_path, filename)
            print(file_path)

            # Read the specific sheet from each file
            for sheet_name in sheets_to_merge:
                try:
                    sheet_data = pd.read_excel(file_path, sheet_name)
                    sheet_data['File'] = filename  # Add a column to track the source file
                    merged_data = pd.concat([merged_data, sheet_data], ignore_index=True)
                except Exception as e:
                    print(f"Error reading sheet '{sheet_name}' from file '{filename}': {e}")

    # Write the merged data to a new Excel file
    merged_data.to_excel(output_file, index=False)
    print(f'Merged data saved to {output_file}')

# Example usage
folder_path = filedialog.askdirectory(title="Select Source Folder")
sheets_to_merge = ['eutra-fa-information','meas-object-eutra-entries']  # List the sheet names you want to merge
output_file = folder_path + '/merged_output.xlsx'
merge_specific_sheet(folder_path, sheets_to_merge, output_file)