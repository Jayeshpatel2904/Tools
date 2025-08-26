import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from matplotlib.backends.backend_pdf import PdfPages

THRESHOLD = 0.8  # Will be prompted from user

def extract_parts(cellname):
    siteid = cellname[:11]
    sectorid = cellname[12:13]
    band  = cellname[14:]
    return pd.Series([siteid, sectorid, band])

class ExcelVisualizer:
    def __init__(self, root):
        self.root = root
        root.state('zoomed')
        self.root.title("Cell Utilization Viewer V1.6")
        self.tree = None
        self.df = None
        self.last_figure = None  # Store last matplotlib figure
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        # Load Button
        self.load_btn = tk.Button(frame, text="Load Data File", bg="#599ACF", fg="white", font=('Arial', 12, 'bold'), command=self.load_file)
        self.load_btn.pack(fill="x", pady=10, padx=10)

        # Export All Button (always available if data is loaded)
        self.export_all_btn = tk.Button(frame, text="Export All Over Threshold Charts", bg="#994400", fg="white", font=('Arial', 11), command=self.export_all_over_threshold, state="disabled")
        self.export_all_btn.pack(fill="x", pady=5, padx=10)

        # Progress Label
        self.progress_label = ttk.Label(frame, text="")
        self.progress_label.pack()

        # Treeview with scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(side="left", fill="y")

        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side="right", fill="y")

        self.treeview = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
        self.treeview.pack(side="left", fill="y")
        tree_scrollbar.config(command=self.treeview.yview)
        self.treeview.bind("<<TreeviewSelect>>", self.on_tree_click)

        # Canvas for Charts
        self.canvas_frame = ttk.Frame(frame)
        self.canvas_frame.pack(side="right", fill="both", expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        global THRESHOLD
        try:
            threshold_input = simpledialog.askfloat("Threshold", "Enter threshold percentage (e.g. 80 for 80%)", minvalue=0.0, maxvalue=100.0,  initialvalue=80)
            if threshold_input is not None:
                THRESHOLD = threshold_input
        except Exception:
            messagebox.showwarning("Warning", "Invalid threshold input. Using default 0.8")

        self.treeview.delete(*self.treeview.get_children())
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.progress_label.config(text="")
        self.export_all_btn.config(state="disabled")

        self.load_btn.config(bg="#3d3d3d", text="Data Loading.....", state="disabled")
        threading.Thread(target=self.process_file, args=(file_path,), daemon=True).start()

    def process_file(self, file_path):
        try:
            xls = pd.ExcelFile(file_path)
            self.df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

            self.df['CELLNAME'] = self.df['CELLNAME'].astype(str).str.strip()
            self.df['DATETIME'] = pd.to_datetime(self.df['DATETIME'], errors='coerce')
            self.df['UTL_DL PRB utilization'] = pd.to_numeric(self.df['UTL_DL PRB utilization'], errors='coerce')
            self.df['UTL_DL PRB utilization'] = self.df['UTL_DL PRB utilization'] * 100

            self.df[['SITEID', 'SECTORID', 'BAND']] = self.df['CELLNAME'].apply(extract_parts)

            self.populate_tree()
            self.load_btn.config(bg="#058d10", text="Data Loaded", state="normal")
            self.export_all_btn.config(state="normal")
        except Exception as e:
            self.progress_label.config(text=f"Error: {e}")
            self.load_btn.config(bg="red", text="Load Failed", state="normal")

    def populate_tree(self):
        self.treeview.delete(*self.treeview.get_children())

        normal_root = self.treeview.insert("", "end", text="Normal", open=True)
        over_root = self.treeview.insert("", "end", text="Over Threshold", open=True)

        normal_selections = {}
        over_selections = {}

        grouped = self.df.groupby(['SELECTION_0_NAME', 'SITEID', 'SECTORID'])

        for (sel_name, siteid, sectorid), group in grouped:
            max_util = group['UTL_DL PRB utilization'].max()
            root_map = over_selections if max_util > THRESHOLD else normal_selections
            top_node = over_root if max_util > THRESHOLD else normal_root

            if sel_name not in root_map:
                root_map[sel_name] = self.treeview.insert(top_node, "end", text=sel_name, open=True)

            self.treeview.insert(root_map[sel_name], "end", text=f"{siteid} / Sector {sectorid}", open=False)

    def on_tree_click(self, event):
        selected = self.treeview.selection()
        if not selected:
            return

        item_text = self.treeview.item(selected[0], 'text')
        parent_item = self.treeview.parent(selected[0])
        grandparent_item = self.treeview.parent(parent_item)

        if '/' not in item_text or not parent_item:
            return

        try:
            sel_name = self.treeview.item(parent_item, 'text')
            if sel_name in ["Normal", "Over Threshold"]:
                return
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
            for i, (x, y) in enumerate(zip(avg_util_by_time.index, avg_util_by_time.values)):
                ax.annotate(x.strftime('%Y-%m-%d %H:%M'), (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, rotation=45)
            ax.set_title(f"CELLNAME: {cell}")
            ax.set_xlabel("Datetime")
            ax.set_ylabel("Utilization")
            ax.legend()
            ax.grid(True)

        plt.subplots_adjust(hspace=0.5)
        self.last_figure = fig
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Add Export button under chart
        export_button = tk.Button(self.canvas_frame, text="Export Chart to PDF", command=self.export_to_pdf, bg="#007A3D", fg="white", font=('Arial', 11, 'bold'))
        export_button.pack(pady=5)

    def export_to_pdf(self):
        if self.last_figure:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                self.last_figure.savefig(file_path, bbox_inches='tight')
                messagebox.showinfo("Export", f"Chart exported to {file_path}")
        else:
            messagebox.showwarning("Warning", "No chart available to export.")

    def export_all_over_threshold(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Save All Over Threshold Charts")
        if not file_path:
            return

        grouped = self.df.groupby(['SELECTION_0_NAME', 'SITEID', 'SECTORID'])
        with PdfPages(file_path) as pdf:
            for (sel_name, siteid, sectorid), group in grouped:
                if group['UTL_DL PRB utilization'].max() <= THRESHOLD:
                    continue
                data = group.dropna(subset=['DATETIME', 'UTL_DL PRB utilization'])
                cellnames = data['CELLNAME'].unique()
                if len(cellnames) == 0:
                    continue

                fig, axs = plt.subplots(len(cellnames), 1, figsize=(10, 4 * len(cellnames)))
                if len(cellnames) == 1:
                    axs = [axs]

                for ax, cell in zip(axs, cellnames):
                    cell_data = data[data['CELLNAME'] == cell]
                    if cell_data.empty:
                        continue
                    avg_util_by_time = cell_data.groupby('DATETIME')['UTL_DL PRB utilization'].mean()
                    ax.plot(avg_util_by_time.index, avg_util_by_time.values, label=f"{cell}", marker='o')
                    for i, (x, y) in enumerate(zip(avg_util_by_time.index, avg_util_by_time.values)):
                        ax.annotate(x.strftime('%Y-%m-%d %H:%M'), (x, y), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, rotation=45)
                    ax.set_title(f"{sel_name} - {siteid} / Sector {sectorid} - CELLNAME: {cell}")
                    ax.set_xlabel("Datetime")
                    ax.set_ylabel("Utilization")
                    ax.legend()
                    ax.grid(True)

                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)

        messagebox.showinfo("Export", f"All charts above threshold exported to {file_path}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ExcelVisualizer(root)
    root.mainloop()
