import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from matplotlib.backends.backend_pdf import PdfPages
import datetime as dt

THRESHOLD = 0.8  # Will be prompted from user

def extract_parts(cellname):
    siteid = cellname[:11]
    sectorid = cellname[12:13]
    band = cellname[14:]
    return pd.Series([siteid, sectorid, band])

class ExcelVisualizer:
    def __init__(self, root):
        self.root = root
        root.state('zoomed')
        self.root.title("Cell Utilization Viewer V1.6 - Pre/Post Charting")
        self.tree = None
        self.df = None # This will now always hold the original, full DataFrame
        self.last_figure = None  # Store last matplotlib figure
        
        # Date entry variables for Pre and Post periods
        self.pre_start_date_var = tk.StringVar()
        self.pre_end_date_var = tk.StringVar()
        self.post_start_date_var = tk.StringVar()
        self.post_end_date_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        # Load Button
        self.load_btn = tk.Button(frame, text="Load Data File", bg="#599ACF", fg="white", font=('Arial', 12, 'bold'), command=self.load_file)
        self.load_btn.pack(fill="x", pady=10, padx=10)

        # Date Range Input for Pre and Post
        date_range_frame = ttk.LabelFrame(frame, text="Define Pre & Post Date Ranges (YYYY-MM-DD)", padding=10)
        date_range_frame.pack(fill="x", pady=5, padx=20)

        # Pre Period
        pre_frame = ttk.Frame(date_range_frame)
        pre_frame.pack(side="top", fill="x", pady=2)
        ttk.Label(pre_frame, text="Pre Start:").pack(side="left", padx=5)
        self.pre_start_entry = ttk.Entry(pre_frame, textvariable=self.pre_start_date_var, width=15)
        self.pre_start_entry.pack(side="left", padx=5)
        # Setting default dates to be relative to the current date for practicality
        self.pre_start_entry.insert(0, (dt.date.today() - dt.timedelta(days=28)).strftime('%Y-%m-%d')) 
        
        ttk.Label(pre_frame, text="Pre End:").pack(side="left", padx=5)
        self.pre_end_entry = ttk.Entry(pre_frame, textvariable=self.pre_end_date_var, width=15)
        self.pre_end_entry.pack(side="left", padx=5)
        self.pre_end_entry.insert(0, (dt.date.today() - dt.timedelta(days=21)).strftime('%Y-%m-%d')) 

        # Post Period
        post_frame = ttk.Frame(date_range_frame)
        post_frame.pack(side="top", fill="x", pady=5)
        ttk.Label(post_frame, text="Post Start:").pack(side="left", padx=5)
        self.post_start_entry = ttk.Entry(post_frame, textvariable=self.post_start_date_var, width=15)
        self.post_start_entry.pack(side="left", padx=5)
        self.post_start_entry.insert(0, (dt.date.today() - dt.timedelta(days=14)).strftime('%Y-%m-%d')) 
        
        ttk.Label(post_frame, text="Post End:").pack(side="left", padx=5)
        self.post_end_entry = ttk.Entry(post_frame, textvariable=self.post_end_date_var, width=15)
        self.post_end_entry.pack(side="left", padx=5)
        self.post_end_entry.insert(0, dt.date.today().strftime('%Y-%m-%d')) # Default to today

        # Button to show pre/post charts (will replace apply_date_filter_btn for selected item)
        self.show_pre_post_btn = tk.Button(date_range_frame, text="Show Pre/Post Charts for Selected", command=self.on_show_pre_post_charts, state="disabled")
        self.show_pre_post_btn.pack(side="left", padx=10)


        # Export All PDF Button (remains global)
        self.export_all_btn = tk.Button(frame, text="Export All Over Threshold Charts", bg="#994400", fg="white", font=('Arial', 11), command=self.export_all_over_threshold, state="disabled")
        self.export_all_btn.pack(fill="x", pady=5, padx=10)

        # Progress Label
        self.progress_label = ttk.Label(frame, text="")
        self.progress_label.pack()

        # Circular Progress Bar
        self.progress_bar = ttk.Progressbar(frame, mode='indeterminate', length=100) 
        self.progress_bar.pack(fill="x", pady=15, padx=10)
        self.progress_bar.pack_forget() # Initially hide it

        # Treeview with scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(side="left", fill="y")

        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side="right", fill="y")

        self.treeview = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
        self.treeview.pack(side="left", fill="y")
        tree_scrollbar.config(command=self.treeview.yview)
        # We will not directly plot on tree click now, but enable the pre/post button
        self.treeview.bind("<<TreeviewSelect>>", self.on_tree_item_select) 

        # Canvas for Charts
        self.canvas_frame = ttk.Frame(frame)
        self.canvas_frame.pack(side="right", fill="both", expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        global THRESHOLD
        try:
            threshold_input = simpledialog.askfloat("Threshold", "Enter threshold percentage (e.g. 80 for 80%)", minvalue=0.0, maxvalue=100.0, initialvalue=80)
            if threshold_input is not None:
                THRESHOLD = threshold_input
        except Exception:
            messagebox.showwarning("Warning", "Invalid threshold input. Using default 0.8")

        self.treeview.delete(*self.treeview.get_children())
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.progress_label.config(text="")
        self.export_all_btn.config(state="disabled")
        self.show_pre_post_btn.config(state="disabled") # Disable until data loaded

        self.load_btn.config(bg="#3d3d3d", text="Data Loading.....", state="disabled")
        self.progress_bar.pack(fill='x', expand=True, padx=10, pady=10)
        self.progress_bar.start()
        threading.Thread(target=self.process_file, args=(file_path,), daemon=True).start()

    def process_file(self, file_path):
        try:
            xls = pd.ExcelFile(file_path)
            self.df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

            self.df['CELLNAME'] = self.df['CELLNAME'].astype(str).str.strip()
            self.df['DATETIME'] = pd.to_datetime(self.df['DATETIME'], errors='coerce')
            self.df['ACC_RRC Connection Setup Failure Rate'] = pd.to_numeric(self.df['ACC_RRC Connection Setup Failure Rate'], errors='coerce')
            self.df['ACC_RRC Connection Setup Failure Rate'] = self.df['ACC_RRC Connection Setup Failure Rate'] * 100

            self.df[['SITEID', 'SECTORID', 'BAND']] = self.df['CELLNAME'].apply(extract_parts)

            self.populate_tree() # Populate tree with the full DF
            self.load_btn.config(bg="#058d10", text="Data Loaded", state="normal")
            self.export_all_btn.config(state="normal")
            self.show_pre_post_btn.config(state="normal") # Enable pre/post button after data loaded
        except Exception as e:
            self.progress_label.config(text=f"Error: {e}")
            self.load_btn.config(bg="red", text="Load Failed", state="normal")
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def populate_tree(self):
        self.treeview.delete(*self.treeview.get_children())

        normal_root = self.treeview.insert("", "end", text="Normal (Below Threshold)", open=True)
        over_root = self.treeview.insert("", "end", text="Over Threshold", open=True)

        normal_selection_nodes = {}
        over_selection_nodes = {}

        # Always use the full DataFrame (self.df) for populating the tree
        grouped = self.df.groupby(['SELECTION_0_NAME', 'SITEID', 'SECTORID'])

        for (sel_name, siteid, sectorid), group in grouped:
            max_util_for_sector = group['ACC_RRC Connection Setup Failure Rate'].max()

            if max_util_for_sector > THRESHOLD:
                if sel_name not in over_selection_nodes:
                    over_selection_nodes[sel_name] = self.treeview.insert(over_root, "end", text=sel_name, open=True)
                self.treeview.insert(over_selection_nodes[sel_name], "end", text=f"{siteid} / Sector {sectorid}", open=False,
                                     values=(sel_name, siteid, sectorid))
            else:
                if sel_name not in normal_selection_nodes:
                    normal_selection_nodes[sel_name] = self.treeview.insert(normal_root, "end", text=sel_name, open=True)
                self.treeview.insert(normal_selection_nodes[sel_name], "end", text=f"{siteid} / Sector {sectorid}", open=False,
                                     values=(sel_name, siteid, sectorid))

    def on_tree_item_select(self, event):
        # When an item is selected, just enable the "Show Pre/Post Charts" button
        selected = self.treeview.selection()
        if selected:
            item_values = self.treeview.item(selected[0], 'values')
            if item_values: # Ensure it's a selectable sector node
                self.show_pre_post_btn.config(state="normal")
            else:
                self.show_pre_post_btn.config(state="disabled") # Disable if a category node is selected
        else:
            self.show_pre_post_btn.config(state="disabled")


    def on_show_pre_post_charts(self):
        selected = self.treeview.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a sector from the treeview first.")
            return

        item = selected[0]
        item_values = self.treeview.item(item, 'values')

        if not item_values: # This ensures only actual sector nodes are processed
            messagebox.showwarning("Invalid Selection", "Please select a specific Site/Sector node to view charts.")
            return

        try:
            sel_name, siteid, sectorid = item_values
        except ValueError:
            messagebox.showerror("Error", "Invalid tree item format for plotting.")
            return
        
        # Get the full data for the selected sector (not date filtered yet)
        sector_data = self.df[
            (self.df['SELECTION_0_NAME'] == sel_name) &
            (self.df['SITEID'] == siteid) &
            (self.df['SECTORID'] == sectorid)
        ].copy() # Use .copy() to avoid SettingWithCopyWarning if you modify it later

        if sector_data.empty:
            messagebox.showerror("Error", f"No data found for {siteid} / Sector {sectorid}.")
            return

        # Parse pre and post date ranges
        try:
            pre_start = pd.to_datetime(self.pre_start_date_var.get())
            pre_end = pd.to_datetime(self.pre_end_date_var.get()) + pd.Timedelta(days=1, seconds=-1)
            post_start = pd.to_datetime(self.post_start_date_var.get())
            post_end = pd.to_datetime(self.post_end_date_var.get()) + pd.Timedelta(days=1, seconds=-1)

            if pre_start > pre_end or post_start > post_end:
                messagebox.showerror("Invalid Date Range", "Start date cannot be after end date for either period.")
                return
            # Optional warning for overlapping dates
            # if post_start <= pre_end:
            #      messagebox.showwarning("Date Overlap", "Post period starts before or on Pre period end. Charts will be distinct but periods overlap.")

        except ValueError:
            messagebox.showerror("Invalid Date Format", "Please enter dates in YYYY-MM-DD format for all date fields.")
            return
        except Exception as e:
            messagebox.showerror("Date Error", f"An error occurred with date inputs: {e}")
            return

        self.plot_pre_post_charts(sector_data, pre_start, pre_end, post_start, post_end)


    def plot_pre_post_charts(self, full_sector_data, pre_start, pre_end, post_start, post_end):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Filter data for pre and post periods
        pre_data = full_sector_data[
            (full_sector_data['DATETIME'] >= pre_start) &
            (full_sector_data['DATETIME'] <= pre_end)
        ].dropna(subset=['DATETIME', 'ACC_RRC Connection Setup Failure Rate'])

        post_data = full_sector_data[
            (full_sector_data['DATETIME'] >= post_start) &
            (full_sector_data['DATETIME'] <= post_end)
        ].dropna(subset=['DATETIME', 'ACC_RRC Connection Setup Failure Rate'])

        # Get all unique cellnames from the combined data for comprehensive plotting
        all_cellnames = sorted(full_sector_data['CELLNAME'].unique())

        if not all_cellnames:
            messagebox.showinfo("Info", "No cellnames available for selected sector.")
            return

        # Create a subplot for each unique CELLNAME
        fig, axs = plt.subplots(len(all_cellnames), 1, figsize=(12, 4 * len(all_cellnames)))
        if len(all_cellnames) == 1:
            axs = [axs] # Ensure axs is iterable even if there's only one subplot

        for i, cell in enumerate(all_cellnames):
            ax = axs[i]
            
            # Plot PRE data
            cell_pre_data = pre_data[pre_data['CELLNAME'] == cell].sort_values(by='DATETIME')
            if not cell_pre_data.empty:
                avg_util_by_time_pre = cell_pre_data.groupby('DATETIME')['ACC_RRC Connection Setup Failure Rate'].mean()
                ax.plot(avg_util_by_time_pre.index, avg_util_by_time_pre.values, 
                        label=f"Pre ({pre_start.strftime('%m/%d')} - {pre_end.strftime('%m/%d')})", 
                        marker='o', markersize=4, linestyle='-', color='blue')
            else:
                ax.text(0.5, 0.5, 'No Pre Data', transform=ax.transAxes, 
                        horizontalalignment='center', verticalalignment='center', color='red', fontsize=12)

            # Plot POST data
            cell_post_data = post_data[post_data['CELLNAME'] == cell].sort_values(by='DATETIME')
            if not cell_post_data.empty:
                avg_util_by_time_post = cell_post_data.groupby('DATETIME')['ACC_RRC Connection Setup Failure Rate'].mean()
                ax.plot(avg_util_by_time_post.index, avg_util_by_time_post.values, 
                        label=f"Post ({post_start.strftime('%m/%d')} - {post_end.strftime('%m/%d')})", 
                        marker='x', markersize=4, linestyle='--', color='green')
            else:
                ax.text(0.5, 0.3, 'No Post Data', transform=ax.transAxes, 
                        horizontalalignment='center', verticalalignment='center', color='red', fontsize=12)


            # Add threshold line
            ax.axhline(y=THRESHOLD, color='red', linestyle=':', label=f'Threshold ({THRESHOLD:.0f}%)')
            
            ax.set_title(f"CELLNAME: {cell}")
            ax.set_xlabel("Datetime")
            ax.set_ylabel("Utilization (%)")
            # ax.set_ylim(0, 100) # Removed this line to auto-adjust Y-axis
            ax.legend(loc='upper right', bbox_to_anchor=(1.05, 1)) # Adjust legend position
            ax.grid(True)
            
        fig.autofmt_xdate(rotation=45, ha='right') # Apply date formatting to the whole figure
        plt.tight_layout(rect=[0, 0, 0.95, 1]) # Adjust layout to make space for legends
        self.last_figure = fig

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)

        export_chart_btn = tk.Button(self.canvas_frame, text="Export Current (Pre/Post) Chart to PDF", bg="#666", fg="white", font=('Arial', 11),
                                     command=self.export_to_pdf)
        export_chart_btn.pack(side=tk.BOTTOM, fill="x", pady=5, padx=10)


    def export_to_pdf(self):
        if self.last_figure:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                try:
                    self.last_figure.savefig(file_path, bbox_inches='tight')
                    messagebox.showinfo("Export", f"Chart exported to {file_path}")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export chart: {e}")
        else:
            messagebox.showwarning("Warning", "No chart available to export.")

    def export_all_over_threshold(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Save All Over Threshold Charts")
        if not file_path:
            return

        self.progress_label.config(text="Exporting all charts...")
        self.progress_bar.pack()
        self.progress_bar.start()

        def _export_in_thread():
            try:
                # Use the full self.df for the "Export All Over Threshold" functionality
                grouped = self.df.groupby(['SELECTION_0_NAME', 'SITEID', 'SECTORID'])
                
                over_threshold_groups = [
                    (sel_name, siteid, sectorid, group)
                    for (sel_name, siteid, sectorid), group in grouped
                    if group['ACC_RRC Connection Setup Failure Rate'].max() > THRESHOLD
                ]

                if not over_threshold_groups:
                    messagebox.showinfo("Export Info", "No sectors found with utilization over threshold to export.")
                    return

                with PdfPages(file_path) as pdf:
                    for i, (sel_name, siteid, sectorid, group) in enumerate(over_threshold_groups):
                        data = group.dropna(subset=['DATETIME', 'ACC_RRC Connection Setup Failure Rate'])
                        cellnames = data['CELLNAME'].unique()
                        
                        if len(cellnames) == 0:
                            continue

                        fig, axs = plt.subplots(len(cellnames), 1, figsize=(10, 4 * len(cellnames)))
                        if len(cellnames) == 1:
                            axs = [axs]

                        for ax, cell in zip(axs, cellnames):
                            cell_data = data[data['CELLNAME'] == cell].sort_values(by='DATETIME')
                            if cell_data.empty:
                                continue
                            
                            avg_util_by_time = cell_data.groupby('DATETIME')['ACC_RRC Connection Setup Failure Rate'].mean()
                            ax.plot(avg_util_by_time.index, avg_util_by_time.values, label=f"{cell}", marker='o')
                            ax.axhline(y=THRESHOLD, color='r', linestyle='--', label=f'Threshold ({THRESHOLD:.0f}%)')
                            ax.set_title(f"{sel_name} - {siteid} / Sector {sectorid} - CELLNAME: {cell}")
                            ax.set_xlabel("Datetime")
                            ax.set_ylabel("Utilization (%)")
                            # ax.set_ylim(0, 100) # Removed this line to auto-adjust Y-axis
                            ax.legend()
                            ax.grid(True)
                        
                        fig.autofmt_xdate(rotation=45, ha='right')
                        plt.tight_layout()
                        pdf.savefig(fig)
                        plt.close(fig)
                        
                        self.root.after(0, lambda i=i, total=len(over_threshold_groups): self.progress_label.config(text=f"Exporting chart {i+1}/{total}..."))


                messagebox.showinfo("Export", f"All charts above threshold exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export charts: {e}")
            finally:
                self.root.after(0, lambda: self.progress_label.config(text=""))
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_bar.pack_forget())

        threading.Thread(target=_export_in_thread, daemon=True).start()


if __name__ == '__main__':
    root = tk.Tk()
    app = ExcelVisualizer(root)
    root.mainloop()