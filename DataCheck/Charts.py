from tkinter import filedialog
import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table

# Load the Excel file
excel_file= filedialog.askopenfilename()
xls = pd.ExcelFile(excel_file)

# Get the sheet names
sheet_names = xls.sheet_names

# Create the main application window
app = tk.Tk()
app.title("Excel Tabs Viewer")

# Create a notebook widget to hold multiple tabs
notebook = ttk.Notebook(app)

# Iterate through sheet names and create tabs for each sheet
for sheet_name in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    table_frame = tk.Frame(notebook)

    # Create a Table widget from the pandastable library
    table = Table(table_frame, dataframe=df)
    table.show()

    table_frame.pack(fill="both", expand=True)
    notebook.add(table_frame, text=sheet_name)

notebook.pack(fill="both", expand=True)

# Start the main event loop
app.mainloop()