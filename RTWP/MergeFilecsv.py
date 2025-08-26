import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, asksaveasfilename

# Function to merge selected CSV files, filter specific columns, and filter AOI values
def merge_csv_to_excel():
    # List of columns to keep
    columns_to_keep = [
        "Timestamp", "Region", "AOI", "Cluster Name", "Site Name", "RU IP",
        "RTWP N70/71 Ant-A Car-0", "RTWP N70/71 Ant-B Car-0", "RTWP N70/71 Ant-C Car-0", "RTWP N70/71 Ant-D Car-0",
        "RTWP N66/26 Ant-A Car-0", "RTWP N66/26 Ant-A Car-1", "RTWP N66/26 Ant-B Car-0", "RTWP N66/26 Ant-B Car-1",
        "RTWP N66/26 Ant-C Car-0", "RTWP N66/26 Ant-C Car-1", "RTWP N66/26 Ant-D Car-0", "RTWP N66/26 Ant-D Car-1",
        "RTWP N29 Ant-A Car-0", "RTWP N29 Ant-B Car-0", "RTWP N29 Ant-C Car-0", "RTWP N29 Ant-D Car-0"
    ]

    # AOI values to keep
    aoi_values_to_keep = ["CHS", "CLT", "FAY", "GSP", "RDU", "AVL", "CAE"]

    # Hide the main tkinter window
    Tk().withdraw()

    # Open file dialog to select multiple CSV files
    csv_files = askopenfilenames(filetypes=[("CSV files", "*.csv")], title="Select CSV Files to Merge")

    # Open save dialog to specify where to save the merged Excel file
    output_excel_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save Merged Excel File As")

    if not csv_files or not output_excel_path:
        print("No files selected or no save location chosen. Exiting...")
        return

    # List to hold DataFrames
    dataframes = []

    # Loop through selected CSV files and read them into DataFrames
    for file in csv_files:
        df = pd.read_csv(file)

        # Keep only the specified columns
        df_filtered = df[columns_to_keep]

        # Print the unique values in AOI before cleaning
        print("Unique AOI values before cleaning:", df_filtered["AOI"].unique())

        # Clean AOI column (strip spaces and standardize case)
        df_filtered["AOI"] = df_filtered["AOI"].str.strip().str.upper()


        # Filter the AOI column to include only the specified AOI values
        df_filtered = df_filtered[df_filtered["AOI"].isin([aoi.upper() for aoi in aoi_values_to_keep])]

        # Print the DataFrame after filtering to see if it contains the correct AOI values
        

        dataframes.append(df_filtered)

    # Merge all DataFrames row-wise
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save the merged DataFrame to an Excel file
    merged_df.to_excel(output_excel_path, index=False)

    print(f"Merged file saved as {output_excel_path}")

# Example usage
merge_csv_to_excel()
