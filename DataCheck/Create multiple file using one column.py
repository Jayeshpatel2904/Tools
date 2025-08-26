import pandas as pd
import os
from tkinter import Tk, filedialog

def select_source_file():
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()
    # Open file dialog and prompt user to select an Excel file
    file_path = filedialog.askopenfilename(title="Select Source Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])
    return file_path

def select_target_folder():
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()
    # Open folder dialog and prompt user to select a target folder
    folder_path = filedialog.askdirectory(title="Select Target Folder to Save Files")
    return folder_path

def get_unique_Batch_values(sheets_data, column_name):
    # Get unique "Batch" values from all sheets and return the combined unique values
    unique_values = set()
    for sheet_name, df in sheets_data.items():
        if column_name in df.columns:
            unique_values.update(df[column_name].unique())
    return unique_values
    
def convert_booleans_to_lowercase(df):
    # Convert boolean True/False to lowercase 'true'/'false' strings
    return df.applymap(lambda x: 'true' if x is True else ('false' if x is False else x))

def split_and_save_by_Batch(source_file, column_name, target_folder):
    # Read the entire Excel file with multiple sheets
    excel_file = pd.read_excel(source_file, sheet_name=None)  # Load all sheets into a dictionary
    
    # Get all unique values from the "Batch" column across all sheets
    unique_Batch_values = get_unique_Batch_values(excel_file, column_name)
    
    # For each unique value in "Batch", filter both sheets and create a new Excel file
    for Batch_value in unique_Batch_values:
        with pd.ExcelWriter(os.path.join(target_folder, f'Batch_{Batch_value}.xlsx'), engine='openpyxl') as writer:
            # Iterate over each sheet and filter by the current "Batch" value
            for sheet_name, df in excel_file.items():
                if column_name in df.columns:
                    filtered_df = df[df[column_name] == Batch_value]

                    # Remove the specified columns
                    columns_to_remove = ["Site ID", "Batch"]
                    filtered_df = filtered_df.drop(columns=[col for col in columns_to_remove if col in filtered_df.columns])


                    filtered_df = convert_booleans_to_lowercase(filtered_df)
                    
                    filtered_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)
                    
                    print(f"Filtered data for Batch '{Batch_value}' saved in sheet '{sheet_name}' with custom header.")
                else:
                    print(f"Column '{column_name}' not found in sheet '{sheet_name}'")
                    
        print(f"Excel file created: Batch_{Batch_value}.xlsx with filtered data")

def main():
    # Prompt the user to select the source Excel file
    source_file = select_source_file()
    
    # Read the Excel file to check available columns from one of the sheets
    excel_file = pd.read_excel(source_file, sheet_name=None)
    sample_sheet = list(excel_file.keys())[0]
    sample_df = excel_file[sample_sheet]
    print("Available columns from the first sheet:", sample_df.columns.tolist())
    
    # Ask the user to input the column name to filter by (e.g., "Batch")
    column_name = "Batch"

    # Prompt the user to select the target folder to save the individual files
    target_folder = select_target_folder()
    
    # Split the file based on the column value and save files for each unique "Batch"
    split_and_save_by_Batch(source_file, column_name, target_folder)

if __name__ == "__main__":
    main()
