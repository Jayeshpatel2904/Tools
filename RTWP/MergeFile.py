import pandas as pd
import os
from tkinter import Tk, filedialog

# Open file dialog to select files
def open_file_dialog():
    Tk().withdraw()  # Hides the root window
    file_paths = filedialog.askopenfilenames(title="Select Excel Files", filetypes=[("Excel files", "*.xlsx")])
    return list(file_paths)

# Open file dialog to select a folder to save the output
def save_file_dialog():
    Tk().withdraw()
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    return save_path

# Function to combine specific sheets from all files into a single workbook and sheet
def combine_sheets_into_one(specific_sheet_names):
    files = open_file_dialog()
    
    if not files:
        print("No files selected.")
        return

    # Create a new Excel writer object
    save_path = save_file_dialog()
    if not save_path:
        print("No save location selected.")
        return

    combined_data = pd.DataFrame()  # DataFrame to store combined data
    
    for file in files:
        try:
            # Loop through the sheets and append data
            for sheet_name in specific_sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name)
                df['Source File'] = os.path.basename(file)  # Add column to identify the source file
                df['Sheet Name'] = sheet_name  # Add column to identify the sheet name
                combined_data = pd.concat([combined_data, df], ignore_index=True)  # Append the data
        except Exception as e:
            print(f"Error processing {file}: {e}")

    # Write the combined data into one sheet
    with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
        combined_data.to_excel(writer, sheet_name="Combined_Data", index=False)

    print(f"All sheets combined into one and saved to {save_path}")

# Specify the sheet names you want to extract from each file
specific_sheet_names = ["Sectors"]  # Update this list with the desired sheet names

# Run the combination function
combine_sheets_into_one(specific_sheet_names)


