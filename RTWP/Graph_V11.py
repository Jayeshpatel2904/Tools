import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog, simpledialog, messagebox
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback

# Define the RTWP columns for each group
columns_n70_71 = ['RTWP N70/71 Ant-A Car-0', 'RTWP N70/71 Ant-B Car-0', 'RTWP N70/71 Ant-C Car-0', 'RTWP N70/71 Ant-D Car-0']
columns_n66_26 = ['RTWP N66/26 Ant-A Car-0', 'RTWP N66/26 Ant-B Car-0', 'RTWP N66/26 Ant-C Car-0', 'RTWP N66/26 Ant-D Car-0']
columns_n66_26_Car1 = ['RTWP N66/26 Ant-A Car-1', 'RTWP N66/26 Ant-B Car-1', 'RTWP N66/26 Ant-C Car-1', 'RTWP N66/26 Ant-D Car-1']
columns_N29 = ['RTWP N29 Ant-A Car-0', 'RTWP N29 Ant-B Car-0', 'RTWP N29 Ant-C Car-0', 'RTWP N29 Ant-D Car-0']

# Global variables for root, row_status, progress_bar and the data_frame_container
root = None
row_status = None
load_button = None
main_progress_bar = None
data_frame_container = None
df_global = None # Store the DataFrame globally after loading for easier access/debugging

# --- Functions (no change here, they are called from the thread or main thread as appropriate) ---

def merge_csv_to_excel(aoi_values_to_keep_str): # Now accepts AOI string
    print("merge_csv_to_excel: Starting...")
    columns_to_keep = [
        "Timestamp", "Region", "AOI", "Cluster Name", "Site Name", "RU IP", "RU ID",
        "RTWP N70/71 Ant-A Car-0", "RTWP N70/71 Ant-B Car-0", "RTWP N70/71 Ant-C Car-0", "RTWP N70/71 Ant-D Car-0",
        "RTWP N66/26 Ant-A Car-0", "RTWP N66/26 Ant-A Car-1", "RTWP N66/26 Ant-B Car-0", "RTWP N66/26 Ant-B Car-1",
        "RTWP N66/26 Ant-C Car-0", "RTWP N66/26 Ant-C Car-1", "RTWP N66/26 Ant-D Car-0", "RTWP N66/26 Ant-D Car-1",
        "RTWP N29 Ant-A Car-0", "RTWP N29 Ant-B Car-0", "RTWP N29 Ant-C Car-0", "RTWP N29 Ant-D Car-0"
    ]

    # File dialog MUST be on the main thread. This function is now called from main thread's `open_file_and_process_data`
    csv_files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")], title="Select CSV Files to Merge")
    if not csv_files:
        print("merge_csv_to_excel: No files selected.")
        return None

    dataframes = []

    aoi_values_to_keep = aoi_values_to_keep_str.replace(" ", "").split(",")
    print(f"merge_csv_to_excel: Selected AOIs: {aoi_values_to_keep}")

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df_filtered = df[columns_to_keep]
            df_filtered["AOI"] = df_filtered["AOI"].astype(str).str.strip().str.upper()
            df_filtered = df_filtered[df_filtered["AOI"].isin([aoi.upper() for aoi in aoi_values_to_keep])]
            dataframes.append(df_filtered)
            print(f"merge_csv_to_excel: Processed file {file}, {len(df_filtered)} rows kept.")
        except KeyError as e:
            messagebox.showerror("Error", f"Missing column in {file}: {e}. Please ensure all required columns are present.")
            print(f"Error processing {file}: Missing column {e}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file {file}: {e}")
            print(f"Error reading file {file}: {e}")
            return None

    if not dataframes:
        messagebox.showinfo("No Data", "No valid data found after filtering by AOI in selected files.")
        return None

    df_merged = pd.concat(dataframes, ignore_index=True)

    def KEY(raw):
        ru_ip_str = str(raw['RU IP']) if pd.notna(raw['RU IP']) else "N/A_IP"
        ru_id_str = str(raw['RU ID']) if pd.notna(raw['RU ID']) else "N/A_ID"
        return f"{ru_ip_str}[{ru_id_str}]"

    df_merged['RU IP'] = df_merged.apply(KEY, axis=1)
    df_merged = df_merged.sort_values(by='RU IP')
    print(f"merge_csv_to_excel: Merged DataFrame shape: {df_merged.shape}")
    return df_merged

def compute_average(value):
    values = [v if v not in ['-NA-', '', None] else '0' for v in str(value).split(':::')]
    numeric_values = []
    for v in values:
        try:
            numeric_values.append(float(v))
        except ValueError:
            numeric_values.append(0)
    return sum(numeric_values) / len(numeric_values) if numeric_values else 0

def process_rtwp_columns(df, columns):
    print("process_rtwp_columns: Starting...")
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(compute_average)
            print(f"Column '{col}' processed.")
        else:
            print(f"WARNING: Column '{col}' not found in the data during RTWP processing.")
    print("process_rtwp_columns: Finished.")
    return df

def format_timestamp_column(df):
    print("format_timestamp_column: Starting...")
    if 'Timestamp' in df.columns:
        try:
            df['Timestamp'] = df['Timestamp'].astype(str).str.replace('_', ' ')
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df.dropna(subset=['Timestamp'], inplace=True)
            print("format_timestamp_column: Timestamp column formatted.")
        except Exception as e:
            messagebox.showerror("Error", f"Error formatting Timestamp column: {str(e)}\nTraceback: {traceback.format_exc()}")
            print(f"Error formatting Timestamp column: {str(e)}\nTraceback: {traceback.format_exc()}")
    else:
        print("WARNING: 'Timestamp' column not found.")
    return df

def is_above_threshold(df_row):
    # CORRECTED: Access the threshold from open_file_and_process_data.var
    if not hasattr(open_file_and_process_data, 'var') or not isinstance(open_file_and_process_data.var, (int, float)):
        print("Threshold value (open_file_and_process_data.var) not set or invalid for is_above_threshold.")
        return False
    
    threshold = open_file_and_process_data.var
    for col in columns_n70_71:
        if col in df_row.index and isinstance(df_row[col], (int, float)):
            if (df_row[col] > threshold and df_row[col] < 0): # RTWP is typically negative, so we check for > threshold but still negative
                return True
    return False

def plot_graph(df, ru_ip, canvas_frame):
    df_filtered = df[df['RU IP'] == ru_ip]

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    if df_filtered.empty:
        Label(canvas_frame, text=f"No data to plot for {ru_ip}", font=('Helvetica', 14, 'bold')).pack(pady=20)
        return

    # Get the threshold value
    threshold_value = getattr(open_file_and_process_data, 'var', None)
    if threshold_value is None:
        print("Warning: Threshold value not available for plotting.")

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    groups = {
        'N70/71': columns_n70_71,
        'N66/26': columns_n66_26,
        'N66/26 Car1': columns_n66_26_Car1,
        'N29': columns_N29
    }

    titles = ['N70/71', 'N66/26', 'N66/26 Car1', 'N29']

    for idx, (group, columns) in enumerate(groups.items()):
        ax = axs[idx // 2, idx % 2]
        for col in columns:
            if col in df_filtered.columns:
                if not df_filtered[col].isnull().all() and pd.api.types.is_numeric_dtype(df_filtered[col]):
                    ax.plot(df_filtered['Timestamp'], df_filtered[col], label=col)
                else:
                    print(f"Skipping plot for {col} on {ru_ip} due to non-numeric or all-null data.")
            else:
                print(f"Column {col} not found in filtered data for {ru_ip}.")

        # Add the threshold line only if a valid threshold value exists
        if threshold_value is not None:
            ax.axhline(y=threshold_value, color='red', linestyle='--', label=f'Threshold ({threshold_value})')
            # Adjust y-limits to ensure the threshold line is visible if all data points are far from it
            min_val = min(ax.get_ylim()[0], threshold_value - 5)
            max_val = max(ax.get_ylim()[1], threshold_value + 5)
            ax.set_ylim(min_val, max_val)

        ax.set_xlabel('Timestamp')
        ax.set_ylabel('RTWP Value')
        ax.set_title(f'{titles[idx]} Graph for RU IP: {ru_ip}')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)

# --- Main Thread Function for Initial User Input and Thread Launch ---

def open_file_and_process_data():
    global load_button, df_global, main_progress_bar
    print("open_file_and_process_data: Button clicked.")
    if load_button:
        load_button.config(bg="lightgray") # Reset button color

    # Get threshold input on the main thread
    threshold_value = simpledialog.askfloat("Input Threshold", "Enter the threshold value (e.g., -90):", initialvalue=-90, parent=root)
    if threshold_value is None:
        print("open_file_and_process_data: Threshold input cancelled.")
        if load_button:
            load_button.config(bg="red") # Indicate cancellation
        return
    open_file_and_process_data.var = threshold_value # Store for access in is_above_threshold

    # Get AOI input on the main thread
    aoi_input = simpledialog.askstring("Input Your AOI", "Enter the AOI Name separate by Comma (e.g., FAY, CLT, RDU):",
                                        initialvalue='CHS, CLT, FAY, GSP, RDU, AVL, CAE', parent=root)
    if aoi_input is None:
        print("open_file_and_process_data: AOI input cancelled.")
        if load_button:
            load_button.config(bg="red") # Indicate cancellation
        return
    
    # Start the progress bar (indeterminate mode for general loading)
    if main_progress_bar:
        load_button.config(bg="#3d3d3d", text="Data Loading.....", state="disabled")
        main_progress_bar.config(mode='indeterminate')
        main_progress_bar.start()
        row_status.set("Loading and Processing Data...")

    # Launch the processing in a separate thread, passing inputs
    threading.Thread(target=process_files_in_thread, args=(threshold_value, aoi_input)).start()

# --- Separate Thread Function for Heavy Lifting ---

def process_files_in_thread(threshold_value_thread, aoi_input_thread):
    global df_global, main_progress_bar
    
    try:
        root.after(0, lambda: row_status.set("Merging CSV Files..."))
        # Call merge_csv_to_excel with the AOI input received from the main thread
        df = merge_csv_to_excel(aoi_input_thread)
        
        if df is None or df.empty:
            root.after(0, lambda: messagebox.showinfo("No Data", "No data loaded or processed from CSV files."))
            root.after(0, lambda: load_button.config(bg="red")) # Indicate failure
            root.after(0, lambda: row_status.set("Ready")) # Ensure status is reset
            return

        root.after(0, lambda: row_status.set("Formatting and Processing Data..."))
        df = format_timestamp_column(df)
        df = df.sort_values(by='Timestamp')
        rtwp_columns = columns_n70_71 + columns_n66_26 + columns_n66_26_Car1 + columns_N29
        df = process_rtwp_columns(df, rtwp_columns)
        
        df_global = df # Store the processed DataFrame globally

        # Call create_data_ui on the main Tkinter thread
        root.after(0, lambda: create_data_ui(root, df_global))

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Processing Error", f"An error occurred during data processing: {str(e)}\nTraceback: {traceback.format_exc()}"))
        print(f"An unexpected error occurred in process_files_in_thread: {e}\n{traceback.format_exc()}")
        root.after(0, lambda: load_button.config(bg="red")) # Indicate failure
    finally:
        pass # Remove the old finally block logic here

# Function to create the data-dependent UI (treeview and graph)
def create_data_ui(root_widget, df):
    global data_frame_container
    print("create_data_ui: Starting UI creation.")

    if data_frame_container:
        for widget in data_frame_container.winfo_children():
            widget.destroy()
        data_frame_container.destroy()

    data_frame_container = Frame(root_widget, bd=2, relief="groove")
    data_frame_container.pack(fill=BOTH, expand=True, padx=10, pady=5)

    threading.Thread(target=create_tree_structure, args=(data_frame_container, df)).start()


# Function to populate the tree structure (no change, already on separate thread)
def create_tree_structure(parent_frame, df):
    global main_progress_bar, load_button, row_status
    print("create_tree_structure: Starting tree building.")
    root.after(0, lambda: row_status.set("Building Tree Structure..."))
    
    left_frame = Frame(parent_frame, bd=1, relief="solid")
    left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    right_frame = Frame(parent_frame, bd=1, relief="solid")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
    
    tree_frame = Frame(left_frame)
    tree_frame.pack(expand=True, fill=BOTH, padx=5, pady=5)

    tree = ttk.Treeview(tree_frame)
    tree.pack(expand=True, side=LEFT, fill=BOTH)

    scrollbar = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.tag_configure('red', foreground='red')

    def set_parent_red(node_id):
        parent = tree.parent(node_id)
        if parent:
            current_tags = tree.item(parent, 'tags')
            if 'red' not in current_tags:
                tree.item(parent, tags=(*current_tags, 'red'))
            set_parent_red(parent)

    def populate_red_tree():
        print("populate_red_tree: Starting.")
        red_tag_region = tree.insert('', 'end', text='Nodes with Issue', tags=('red',))

        problematic_ru_ips = set()
        for index, row in df.iterrows():
            if is_above_threshold(row): # This uses open_file_and_process_data.var internally
                problematic_ru_ips.add(row['RU IP'])
        
        for ru_ip in sorted(list(problematic_ru_ips)):
            site_name = df[df['RU IP'] == ru_ip]['Site Name'].iloc[0] if not df[df['RU IP'] == ru_ip].empty else "Unknown Site"
            tree.insert(red_tag_region, 'end', text=f"{site_name}_{ru_ip}", values=(ru_ip,), tags=('red',))
        print("populate_red_tree: Finished.")

    def populate_tree():
        print("populate_tree: Starting full tree population.")
        for item in tree.get_children():
            tree.delete(item)

        unique_regions = df['Region'].unique()
        for region in unique_regions:
            region_node = tree.insert('', 'end', text=region)
            aois = df[df['Region'] == region]['AOI'].unique()
            for aoi in aois:
                aoi_node = tree.insert(region_node, 'end', text=aoi)
                sites = df[df['AOI'] == aoi]['Site Name'].unique()
                for site in sites:
                    site_node = tree.insert(aoi_node, 'end', text=site)
                    ru_ips = df[df['Site Name'] == site]['RU IP'].unique()
                    for ru_ip in ru_ips:
                        df_filtered_ru = df[df['RU IP'] == ru_ip]
                        if not df_filtered_ru.empty and df_filtered_ru.apply(is_above_threshold, axis=1).any():
                            ru_ip_text = f"{ru_ip}_Red"
                            ru_id_node = tree.insert(site_node, 'end', text=ru_ip_text, values=(ru_ip,), tags=('red',))
                            set_parent_red(ru_id_node)
                        else:
                            tree.insert(site_node, 'end', text=ru_ip, values=(ru_ip,))
        populate_red_tree()
        print("populate_tree: Finished full tree population.")
    
    def on_tree_select(event):
        selected_item = tree.focus()
        selected_values = tree.item(selected_item, 'values')
        if selected_values:
            ru_ip = selected_values[0]
            print(f"Plotting graph for RU IP: {ru_ip}")
            plot_graph(df, ru_ip, right_frame)
        else:
            print("No RU IP selected or invalid selection.")

    tree.bind('<<TreeviewSelect>>', on_tree_select)

    populate_tree()

    # --- PROGRESS BAR FINAL STOP AND UI UPDATE ---
    # This block ensures the progress bar stops AFTER tree is fully loaded
    if main_progress_bar:
        root.after(0, main_progress_bar.stop)
        root.after(0, lambda: main_progress_bar.config(mode='determinate', value=0)) # Reset to determinate and 0
    root.after(0, lambda: load_button.config(bg="#058d10", text="Data Loaded", state="normal")) # Set button green on completion
    root.after(0, lambda: row_status.set("Ready"))
    print("create_tree_structure: Tree building finished.")
    root.state('zoomed')

# Main application function (no change here)
def run_app():
    global root, row_status, load_button, main_progress_bar, data_frame_container
    root = Tk()
    root.title('RTWP Data Graph Viewer')
    # root.state('zoomed')
    root.geometry("800x500")
    root.resizable(True, True)

    row_status = StringVar()
    row_status.set("Waiting to load data...")

    button_frame = Frame(root)
    button_frame.pack(side=TOP, fill=X)

    load_button = Button(button_frame, text="Load Data File", bg="#599ACF", fg="white", font=('Arial', 12, 'bold'),command=open_file_and_process_data)
    load_button.pack(side=TOP, padx=10, pady=5, fill=X, expand=True)

    data_frame_container = Frame(root)
    data_frame_container.pack(fill=BOTH, expand=True)

    footer_frame = Frame(root, bd=1, relief="groove")
    footer_frame.pack(side=BOTTOM, fill=X)
    
    Label(footer_frame, textvariable=row_status, anchor=W, fg="blue").pack(side=LEFT, padx=10, pady=5)
    
    main_progress_bar = ttk.Progressbar(footer_frame, orient=HORIZONTAL, length=200, mode='determinate')
    main_progress_bar.pack(side=LEFT, padx=10, pady=5, fill=X, expand=True)
    
    Label(footer_frame, text="Support email: Jayeshkumar.patel@dish.com", anchor=E, fg="red", font=('Helvetica', 10, 'bold', 'italic')).pack(side=RIGHT, padx=10, pady=5)

    root.mainloop()

# Run main application
run_app()