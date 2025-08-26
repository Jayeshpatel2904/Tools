import os
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview

class FileMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Merger Application")
        self.root.state('zoomed')  # Full-screen

        # Source folder
        Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.source_var = StringVar()
        self.source_entry = Entry(root, textvariable=self.source_var, width=50)
        self.source_entry.grid(row=0, column=1, padx=10)
        Button(root, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=10)

        # Destination folder
        Label(root, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.destination_var = StringVar()
        self.destination_entry = Entry(root, textvariable=self.destination_var, width=50)
        self.destination_entry.grid(row=1, column=1, padx=10)
        Button(root, text="Browse", command=self.browse_destination).grid(row=1, column=2, padx=10)

        # Checkboxes for CSV and Excel
        self.csv_var = IntVar()
        self.excel_var = IntVar()
        Checkbutton(root, text="CSV", variable=self.csv_var).grid(row=2, column=0, padx=10, sticky='w')
        Checkbutton(root, text="Excel", variable=self.excel_var).grid(row=2, column=1, padx=10, sticky='w')

        # Start button
        Button(root, text="Start", command=self.start_merging).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Treeview (Table) for displaying merged Excel data
        self.table_frame = Frame(root)
        self.table_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.table = Treeview(self.table_frame)
        self.table.grid(row=0, column=0, sticky='nsew')

        # Scrollbars for the table
        self.vsb = Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')

        self.hsb = Scrollbar(self.table_frame, orient="horizontal", command=self.table.xview)
        self.hsb.grid(row=1, column=0, sticky='ew')

        self.table.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Filter Entry widgets for each column
        self.filter_entries = {}

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_var.set(folder)

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_var.set(folder)

    def start_merging(self):
        source_dir = self.source_var.get()
        destination_dir = self.destination_var.get()

        if not source_dir or not destination_dir:
            messagebox.showwarning("Input Error", "Please select both source and destination folders!")
            return

        if self.csv_var.get():
            self.merge_csv_files(source_dir, destination_dir)
        if self.excel_var.get():
            self.merge_excel_files(source_dir, destination_dir)

    def merge_csv_files(self, source_dir, destination_dir):
        files = [f for f in os.listdir(source_dir) if f.endswith(".csv")]
        if not files:
            messagebox.showinfo("No CSV files", "No CSV files found in the selected folder.")
            return

        merged_csv = pd.concat([pd.read_csv(os.path.join(source_dir, f)) for f in files], ignore_index=True)
        output_file = os.path.join(destination_dir, "merged.csv")
        merged_csv.to_csv(output_file, index=False)
        messagebox.showinfo("Success", "CSV files merged successfully!")
        self.display_file_in_table(output_file, is_excel=False)

    def merge_excel_files(self, source_dir, destination_dir):
        files = [f for f in os.listdir(source_dir) if f.endswith(".xlsx")]
        if not files:
            messagebox.showinfo("No Excel files", "No Excel files found in the selected folder.")
            return

        writer = pd.ExcelWriter(os.path.join(destination_dir, "merged.xlsx"), engine='openpyxl')
        for i, file in enumerate(files):
            file_path = os.path.join(source_dir, file)
            workbook = load_workbook(file_path)
            for sheet_name in workbook.sheetnames:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                df.to_excel(writer, sheet_name=f"{file}_{sheet_name}", index=False)

        writer.save()
        output_file = os.path.join(destination_dir, "merged.xlsx")
        messagebox.showinfo("Success", "Excel files merged successfully!")
        self.display_file_in_table(output_file, is_excel=True)

    def display_file_in_table(self, file_path, is_excel):
        try:
            if is_excel:
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            self.table.delete(*self.table.get_children())  # Clear existing data

            # Set the column headers
            self.table["column"] = list(df.columns)
            self.table["show"] = "headings"

            for col in self.table["column"]:
                self.table.heading(col, text=col)
                self.table.column(col, width=150)

            # Insert rows into the table
            for _, row in df.iterrows():
                self.table.insert("", "end", values=list(row))

            self.add_filter_entries(df)

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying file: {str(e)}")

    def add_filter_entries(self, df):
        # Destroy any previous filter entries
        for entry in self.filter_entries.values():
            entry.destroy()

        self.filter_entries.clear()

        # Add filter Entry widgets above the Treeview for each column
        for idx, col in enumerate(df.columns):
            entry = Entry(self.table_frame, width=15)
            entry.grid(row=0, column=idx, padx=5, pady=5, sticky='ew')
            entry.insert(0, f"Filter {col}")
            entry.bind("<KeyRelease>", lambda event, col=col: self.filter_table(event, col))
            self.filter_entries[col] = entry

    def filter_table(self, event, column):
        search_term = self.filter_entries[column].get().lower()
        for item in self.table.get_children():
            row_values = self.table.item(item, "values")
            col_idx = self.table["column"].index(column)
            if search_term in str(row_values[col_idx]).lower():
                self.table.reattach(item, '', 'end')
            else:
                self.table.detach(item)

if __name__ == "__main__":
    root = Tk()
    app = FileMergerApp(root)
    root.mainloop()
