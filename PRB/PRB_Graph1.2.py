import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

THRESHOLD = 0.8  # 80% threshold

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

        normal_root = self.treeview.insert("", "end", text="Normal", open=True)
        over_threshold_root = self.treeview.insert("", "end", text="Over Threshold", open=True)

        site_sector_groups = self.df.groupby(['SITEID', 'SECTORID'])
        for (siteid, sectorid), group in site_sector_groups:
            max_util = group['UTL_DL PRB utilization'].max()
            node_text = f"{siteid} / Sector {sectorid}"
            parent = over_threshold_root if max_util > THRESHOLD else normal_root
            self.treeview.insert(parent, "end", text=node_text, open=False)

    def on_tree_click(self, event):
        selected = self.treeview.selection()
        if not selected:
            return

        item_text = self.treeview.item(selected[0], 'text')
        if '/' not in item_text:
            return

        try:
            siteid, sector_text = item_text.split(" / ")
            sectorid = sector_text.replace("Sector ", "")
        except Exception:
            messagebox.showerror("Error", "Invalid tree item format.")
            return

        sector_data = self.df[(self.df['SITEID'] == siteid) & (self.df['SECTORID'] == sectorid)]
        if sector_data.empty:
            messagebox.showerror("Error", f"No data found for {item_text}")
            return

        self.plot_charts(sector_data)

    def plot_charts(self, data):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        data = data.dropna(subset=['DATETIME', 'UTL_DL PRB utilization'])
        data['BAND'] = data['BAND'].fillna('Unknown')
        bands = data['BAND'].unique()

        if len(bands) == 0:
            messagebox.showinfo("Info", "No bands available for selected sector.")
            return

        fig, axs = plt.subplots(len(bands), 1, figsize=(10, 4 * len(bands)))
        if len(bands) == 1:
            axs = [axs]

        for ax, band in zip(axs, bands):
            band_data = data[data['BAND'] == band]
            if band_data.empty:
                continue
            avg_util_by_time = band_data.groupby('DATETIME')['UTL_DL PRB utilization'].mean()
            ax.plot(avg_util_by_time.index, avg_util_by_time.values, label=f"{band}", marker='o')
            ax.set_title(f"Band: {band}")
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
