import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

THRESHOLD = 0.8  # Will be prompted from user

def extract_parts(cellname):
    siteid = cellname[:11]
    sectorid = cellname[12:13]
    band  = cellname[14:]
    return pd.Series([siteid, sectorid, band])

class ExcelVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cellname Band Utilization Viewer")
        self.tree = None
        self.df = None
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        # Load Button
        load_btn = ttk.Button(frame, text="Load Excel File", command=self.load_file)
        load_btn.pack(pady=10)

        # Progress Label
        self.progress_label = ttk.Label(frame, text="")
        self.progress_label.pack()

        # Treeview
        self.treeview = ttk.Treeview(frame)
        self.treeview.pack(side="left", fill="y")
        self.treeview.bind("<Double-1>", self.on_tree_click)

        # Canvas for Charts
        self.canvas_frame = ttk.Frame(frame)
        self.canvas_frame.pack(side="right", fill="both", expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        # Ask for threshold
        global THRESHOLD
        try:
            threshold_input = simpledialog.askfloat("Threshold", "Enter threshold percentage (e.g. 0.8 for 80%)", minvalue=0.0, maxvalue=1.0)
            if threshold_input is not None:
                THRESHOLD = threshold_input
        except Exception:
            messagebox.showwarning("Warning", "Invalid threshold input. Using default 0.8")

        # Clear UI
        self.treeview.delete(*self.treeview.get_children())
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        threading.Thread(target=self.process_file, args=(file_path,), daemon=True).start()

    def process_file(self, file_path):
        self.update_progress("Loading Excel file...")
        try:
            xls = pd.ExcelFile(file_path)
            self.df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

            # Clean and extract fields
            self.df['CELLNAME'] = self.df['CELLNAME'].astype(str).str.strip()
            self.df['DATETIME'] = pd.to_datetime(self.df['DATETIME'], errors='coerce')
            self.df['UTL_DL PRB utilization'] = pd.to_numeric(self.df['UTL_DL PRB utilization'], errors='coerce')

            self.df[['SITEID', 'SECTORID', 'BAND']] = self.df['CELLNAME'].apply(extract_parts)

            self.populate_tree()
            self.update_progress("File loaded successfully.")
        except Exception as e:
            self.update_progress(f"Error: {e}")

    def update_progress(self, message):
        self.progress_label.config(text=message)

    def populate_tree(self):
        self.treeview.delete(*self.treeview.get_children())

        # Build main tree grouped by SELECTION_0_NAME with children as SITEID / SECTORID
        selection_nodes = {}
        grouped = self.df.groupby(['SELECTION_0_NAME', 'SITEID', 'SECTORID'])

        for (sel_name, siteid, sectorid), group in grouped:
            max_util = group['UTL_DL PRB utilization'].max()

            if sel_name not in selection_nodes:
                selection_nodes[sel_name] = self.treeview.insert("", "end", text=sel_name, open=True)

            parent = self.treeview.insert(selection_nodes[sel_name], "end", text=f"{siteid} / Sector {sectorid}", open=False)

            if max_util > THRESHOLD:
                self.treeview.item(parent, tags=("over",))

        self.treeview.tag_configure("over", background="salmon")

    def on_tree_click(self, event):
        selected = self.treeview.selection()
        if not selected:
            return

        item_text = self.treeview.item(selected[0], 'text')
        parent_item = self.treeview.parent(selected[0])
        if '/' not in item_text or not parent_item:
            return

        try:
            sel_name = self.treeview.item(parent_item, 'text')
            siteid, sector_text = item_text.split(" / ")
            sectorid = sector_text.replace("Sector ", "")
        except Exception:
            messagebox.showerror("Error", "Invalid tree item format.")
            return

        sector_data = self.df[
            (self.df['SELECTION_0_NAME'] == sel_name) &
            (self.df['SITEID'] == siteid) &
            (self.df['SECTORID'] == sectorid)
        ]

        if sector_data.empty:
            messagebox.showerror("Error", f"No data found for {item_text}")
            return

        self.plot_charts(sector_data)

    def plot_charts(self, data):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        data = data.dropna(subset=['DATETIME', 'UTL_DL PRB utilization'])
        cellnames = data['CELLNAME'].unique()

        if len(cellnames) == 0:
            messagebox.showinfo("Info", "No cellnames available for selected sector.")
            return

        fig, axs = plt.subplots(len(cellnames), 1, figsize=(10, 4 * len(cellnames)))
        if len(cellnames) == 1:
            axs = [axs]

        for ax, cell in zip(axs, cellnames):
            cell_data = data[data['CELLNAME'] == cell]
            if cell_data.empty:
                continue
            avg_util_by_time = cell_data.groupby('DATETIME')['UTL_DL PRB utilization'].mean()
            ax.plot(avg_util_by_time.index, avg_util_by_time.values, label=f"{cell}", marker='o')
            ax.set_title(f"CELLNAME: {cell}")
            ax.set_xlabel("Datetime")
            ax.set_ylabel("Utilization")
            ax.legend()
            ax.grid(True)

        plt.subplots_adjust(hspace=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == '__main__':
    root = tk.Tk()
    app = ExcelVisualizer(root)
    root.mainloop()
