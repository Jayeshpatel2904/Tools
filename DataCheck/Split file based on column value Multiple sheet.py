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

def split_files_by_column(source_file, column_name, target_folder):
    # Read the entire Excel file with multiple sheets
    excel_file = pd.read_excel(source_file, sheet_name=None)  # Load all sheets into a dictionary
    
    # Iterate over each sheet in the Excel file
    for sheet_name, df in excel_file.items():
        print(f"Processing sheet: {sheet_name}")
        
        # Check if the column exists in the current sheet
        if column_name in df.columns:
            # Get the unique values from the specified column
            unique_values = df[column_name].unique()
            
            # For each unique value, create a new file with filtered rows
            for value in unique_values:
                # Filter the dataframe for rows with the current value
                filtered_df = df[df[column_name] == value]
                
                # Define the file name based on the sheet name and column value
                file_name = f"{sheet_name}_{value}.xlsx"
                file_path = os.path.join(target_folder, file_name)
                
                # Save the filtered data to the target folder
                filtered_df.to_excel(file_path, index=False)
                print(f"File created: {file_path}")
        else:
            print(f"Column '{column_name}' not found in sheet: {sheet_name}")

def main():
    # Prompt the user to select the source Excel file
    source_file = select_source_file()
    
    # Read the Excel file to check available columns from one of the sheets
    excel_file = pd.read_excel(source_file, sheet_name=None)
    sample_sheet = list(excel_file.keys())[0]
    sample_df = excel_file[sample_sheet]
    print("Available columns from the first sheet:", sample_df.columns.tolist())
    
    # Ask the user to input the column name to split by
    column_name = "Rank"

    # Prompt the user to select the target folder to save the individual files
    target_folder = select_target_folder()
    
    # Split the file based on the column value and save files for each sheet
    split_files_by_column(source_file, column_name, target_folder)

if __name__ == "__main__":
    main()
