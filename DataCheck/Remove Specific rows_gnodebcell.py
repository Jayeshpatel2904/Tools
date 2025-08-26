import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import load_workbook

def select_reference_file():
    return filedialog.askopenfilename(title="Select Reference Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])

def select_excel_folder():
    return filedialog.askdirectory(title="Select Folder Containing Excel Files")

def select_output_folder():
    return filedialog.askdirectory(title="Select Output Folder")

def process_excel_files(reference_path, folder_path, save_path):
    try:
        # Load reference sheet (normal read)
        ref_df = pd.read_excel(reference_path)
        ref_gnodeb_ids = set(ref_df['gnb-cu-cp-function-entries/gnodeb-id'].astype(str))
        ref_cell_ids = set(ref_df['gutran-cu-cell-entries/cell-identity'].astype(str))

        for filename in os.listdir(folder_path):
            if filename.endswith(".xlsx") or filename.endswith(".xls"):
                file_path = os.path.join(folder_path, filename)
                print(f"Processing: {filename}")

                excel = pd.ExcelFile(file_path)
                writer = pd.ExcelWriter(os.path.join(save_path, f"{os.path.splitext(filename)[0]}_Changed.xlsx"), engine='openpyxl')

                for sheet_name in excel.sheet_names:
                    try:
                        # Skip first 2 rows (i.e., start from third row)
                        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)

                        # Proceed only if required columns are present
                        if 'gnb-cu-cp-function-entries/gnodeb-id' in df.columns and 'gutran-cu-cell-entries/cell-identity' in df.columns:
                            df = df[
                                df['gnb-cu-cp-function-entries/gnodeb-id'].astype(str).isin(ref_gnodeb_ids) &
                                df['gutran-cu-cell-entries/cell-identity'].astype(str).isin(ref_cell_ids)
                            ]
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as sheet_err:
                        print(f"  Skipped sheet '{sheet_name}' in {filename}: {sheet_err}")

                writer.close()

        messagebox.showinfo("Done", "All Excel files processed successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    ref_file = select_reference_file()
    if not ref_file:
        messagebox.showwarning("Input Required", "Please select a reference file.")
        return

    excel_folder = select_excel_folder()
    if not excel_folder:
        messagebox.showwarning("Input Required", "Please select the folder with Excel files.")
        return

    output_folder = select_output_folder()
    if not output_folder:
        messagebox.showwarning("Input Required", "Please select a folder to save the output.")
        return

    process_excel_files(ref_file, excel_folder, output_folder)

if __name__ == "__main__":
    main()
