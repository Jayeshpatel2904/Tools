import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def main():
    # Setup UI
    root = tk.Tk()
    root.withdraw()

    # Step 1: Choose reference file
    messagebox.showinfo("Step 1", "Select the REFERENCE Excel file")
    reference_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not reference_file:
        print("Reference file not selected.")
        return
    reference_data = pd.read_excel(reference_file, sheet_name=None, header=None)

    # Step 2: Choose folder with Excel files to process
    messagebox.showinfo("Step 2", "Select the FOLDER containing Excel files to process")
    source_folder = filedialog.askdirectory()
    if not source_folder:
        print("Source folder not selected.")
        return

    # Step 3: Choose destination folder
    messagebox.showinfo("Step 3", "Select the FOLDER to SAVE updated files")
    save_folder = filedialog.askdirectory()
    if not save_folder:
        print("Save folder not selected.")
        return

    # Step 4: Process each file
    for filename in os.listdir(source_folder):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            file_path = os.path.join(source_folder, filename)
            try:
                original_data = pd.read_excel(file_path, sheet_name=None, header=None)
                updated_data = {}

                for sheet_name in original_data:
                    orig_df = original_data[sheet_name]
                    if sheet_name in reference_data:
                        ref_df = reference_data[sheet_name]

                        # First 3 rows from original
                        top_rows = orig_df.iloc[:3, :]
                        # From 4th row onward from reference
                        new_rows = ref_df.iloc[3:, :].reset_index(drop=True)

                        # Combine and store
                        final_df = pd.concat([top_rows, new_rows], ignore_index=True)
                        updated_data[sheet_name] = final_df
                    else:
                        # Keep sheet unchanged if not found in reference
                        updated_data[sheet_name] = orig_df

                # Save updated file
                new_filename = os.path.splitext(filename)[0] + "_Changed.xlsx"
                save_path = os.path.join(save_folder, new_filename)

                with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                    for sheet_name, df in updated_data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

                print(f"Saved: {new_filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    messagebox.showinfo("Done", "All files processed successfully!")

if __name__ == "__main__":
    main()
