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
    # Read the source Excel file
    df = pd.read_excel(source_file)
    
    # Get the unique values from the specified column
    unique_values = df[column_name].unique()
    
    # For each unique value, create a new file with filtered rows
    for value in unique_values:
        # Filter the dataframe for rows with the current value
        filtered_df = df[df[column_name] == value]
        
        # Define the file name based on the column value
        file_name = f"{value}.xlsx"
        file_path = os.path.join(target_folder, file_name)
        
        # Save the filtered data to the target folder
        filtered_df.to_excel(file_path, index=False)
        print(f"File created: {file_path}")

def main():
    # Prompt the user to select the source Excel file
    source_file = select_source_file()
    
    # Read the Excel file to display column names
    df = pd.read_excel(source_file)
    print("Available columns:", df.columns.tolist())
    
    # Ask the user to input the column name to split by
    column_name = input("Enter the column name to split the file by: ")

    # Prompt the user to select the target folder to save the individual files
    target_folder = select_target_folder()
    
    # Split the file based on the column value and save files
    split_files_by_column(source_file, column_name, target_folder)

if __name__ == "__main__":
    main()
