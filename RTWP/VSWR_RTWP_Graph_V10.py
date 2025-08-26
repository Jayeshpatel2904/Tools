import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog, simpledialog, messagebox
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from easygui import *

 

def gettask():

    # message / information to be displayed on the screen
    message = "Do you want to Run for VSWR or RTWP?"
    
    # title of the window
    title = "Select one of the option which you want?"
    
    # choices for yes and no button
    choices = ["RTWP", "VSWR"]
    
    # creating a yes no box
    output = ynbox(message, title, choices)
    
    
    # if user pressed yes
    if output:

        # Define the RTWP columns for each group
        gettask.columns_n70_71 = ['RTWP N70/71 Ant-A Car-0', 'RTWP N70/71 Ant-B Car-0', 'RTWP N70/71 Ant-C Car-0', 'RTWP N70/71 Ant-D Car-0']
        gettask.columns_n66_26 = ['RTWP N66/26 Ant-A Car-0', 'RTWP N66/26 Ant-B Car-0', 'RTWP N66/26 Ant-C Car-0', 'RTWP N66/26 Ant-D Car-0']
        gettask.columns_n66_26_Car1 = ['RTWP N66/26 Ant-A Car-1', 'RTWP N66/26 Ant-B Car-1', 'RTWP N66/26 Ant-C Car-1', 'RTWP N66/26 Ant-D Car-1']
        gettask.columns_N29 = ['RTWP N29 Ant-A Car-0', 'RTWP N29 Ant-B Car-0', 'RTWP N29 Ant-C Car-0', 'RTWP N29 Ant-D Car-0']
        gettask.Task = "RTWP Threshould : "
    # if user pressed No
    else:
        
        # Define the VSWR columns for each group
        gettask.columns_n70_71 = ['VSWR N70/N71 Path-A','VSWR N70/N71 Path-B','VSWR N70/N71 Path-C','VSWR N70/N71 Path-D']
        gettask.columns_n66_26 = ['VSWR N66/N26 Path-E','VSWR N66/N26 Path-F','VSWR N66/N26 Path-G','VSWR N66/N26 Path-H']
        gettask.columns_n66_26_Car1 = ['RTWP N66/26 Ant-A Car-1', 'RTWP N66/26 Ant-B Car-1', 'RTWP N66/26 Ant-C Car-1', 'RTWP N66/26 Ant-D Car-1']
        gettask.columns_N29 = ['VSWR N29 Path-I','VSWR N29 Path-J','VSWR N29 Path-K','VSWR N29 Path-L']
        gettask.Task = "VSWR Threshould : "



# Function to merge selected CSV files and filter specific columns and AOI values
def merge_csv_to_excel():
    # List of columns to keep
    columns_to_keep = [
        "Timestamp", "Region", "AOI", "Cluster Name", "Site Name", "RU IP","RU ID",
        "RTWP N70/71 Ant-A Car-0", "RTWP N70/71 Ant-B Car-0", "RTWP N70/71 Ant-C Car-0", "RTWP N70/71 Ant-D Car-0",
        "RTWP N66/26 Ant-A Car-0", "RTWP N66/26 Ant-A Car-1", "RTWP N66/26 Ant-B Car-0", "RTWP N66/26 Ant-B Car-1",
        "RTWP N66/26 Ant-C Car-0", "RTWP N66/26 Ant-C Car-1", "RTWP N66/26 Ant-D Car-0", "RTWP N66/26 Ant-D Car-1",
        "RTWP N29 Ant-A Car-0", "RTWP N29 Ant-B Car-0", "RTWP N29 Ant-C Car-0", "RTWP N29 Ant-D Car-0",
        "VSWR N70/N71 Path-A","VSWR N70/N71 Path-B","VSWR N70/N71 Path-C","VSWR N70/N71 Path-D",
        "VSWR N66/N26 Path-E","VSWR N66/N26 Path-F","VSWR N66/N26 Path-G","VSWR N66/N26 Path-H",
        "VSWR N29 Path-I","VSWR N29 Path-J","VSWR N29 Path-K","VSWR N29 Path-L"]

    
    # Open file dialog to select multiple CSV files
    csv_files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")], title="Select CSV Files to Merge")
    if not csv_files:
        print("No files selected.")
        return None
    

    # List to hold DataFrames
    dataframes = []


    aoi_values_to_keep = open_file.aoi_values_to_keep

    print(aoi_values_to_keep)

    # Loop through selected CSV files and read them into DataFrames
    for file in csv_files:
        df = pd.read_csv(file)

        # Keep only the specified columns
        df_filtered = df[columns_to_keep]

        # Clean AOI column (strip spaces and standardize case)
        df_filtered["AOI"] = df_filtered["AOI"].str.strip().str.upper()

        # Filter the AOI column to include only the specified AOI values
        df_filtered = df_filtered[df_filtered["AOI"].isin([aoi.upper() for aoi in aoi_values_to_keep])]

        dataframes.append(df_filtered)

    # Merge all DataFrames row-wise
    df = pd.concat(dataframes, ignore_index=True)

    def KEY(raw):
        raw['RU IP'] = (str(raw['RU IP']) + "[" + str(raw['RU ID']) + "]")
        return (raw['RU IP'])


    df['RU IP'] = df.apply(KEY, axis=1)
    df = df.sort_values(by='RU IP')

    return df


# Function to compute average RTWP values
def compute_average(value):
    values = [v if v not in ['-NA-', '', None] else '0' for v in str(value).split(':::')]
    numeric_values = []
    for v in values:
        try:
            numeric_values.append(float(v))
        except ValueError:
            numeric_values.append(0)
    return sum(numeric_values) / len(numeric_values) if numeric_values else 0

# Function to process RTWP columns
def process_rtwp_columns(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(compute_average)
        else:
            messagebox.showerror("Error", f"Column '{col}' not found in the data.")
    return df

# Function to format the Timestamp column
def format_timestamp_column(df):
    if 'Timestamp' in df.columns:
        try:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.replace('_', ' '))
        except Exception as e:
            messagebox.showerror("Error", f"Error formatting Timestamp column: {str(e)}")
    return df

# Function to check if any values in columns_n70_71 are above -90
def is_above_threshold(df_row):
    for col in gettask.columns_n70_71:
        if (df_row[col] > open_file.var and df_row[col] < 0) :
            return True
    return False

def plot_graph(df, ru_ip, canvas_frame):
    # Filter data based on selected RU IP
    df_filtered = df[df['RU IP'] == ru_ip]

    # Clear previous plots
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Dictionary of groups and their corresponding columns
    groups = {
        'N70/71': gettask.columns_n70_71,
        'N66/26': gettask.columns_n66_26,
        'N66/26 Car1': gettask.columns_n66_26_Car1,
        'N29': gettask.columns_N29
    }

    # Titles for each subplot
    titles = ['N70/71', 'N66/26', 'N66/26 Car1', 'N29']

    # Iterate over the groups and plot in each subplot
    for idx, (group, columns) in enumerate(groups.items()):
        ax = axs[idx // 2, idx % 2]  # Determine the position in 2x2 grid

        for col in columns:
            ax.plot(df_filtered['Timestamp'], df_filtered[col], label=col)

        ax.set_xlabel('Timestamp')
        ax.set_ylabel('RTWP Value')
        ax.set_title(f'{titles[idx]} Graph for RU IP: {ru_ip}')
        ax.legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Embed the plot in the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)


# Function to display the progress popup
def show_progress_popup(message):
    progress_popup = Toplevel(root)
    progress_popup.title("Processing")
    progress_popup.geometry("300x100")
    progress_popup.resizable(False, False)

    # Add label and progress bar
    Label(progress_popup, text=message).pack(pady=10)
    progress_bar = ttk.Progressbar(progress_popup, orient=HORIZONTAL, length=250, mode='indeterminate')
    progress_bar.pack(pady=10)
    progress_bar.start()

    return progress_popup, progress_bar

# Function to safely close the progress popup
def close_progress_popup(progress_popup, progress_bar):
    if progress_popup and progress_bar:
        try:
            progress_bar.stop()
            progress_popup.destroy()
        except TclError:
            pass  # Ignore if popup was already closed

# Open file function with threshold input and progress popup
def open_file():

    gettask()

    threshold_value = simpledialog.askfloat("Input Threshold", "Enter the threshold value (e.g., -90):", initialvalue=-90)

    AOI_value = simpledialog.askstring("Input Your AOI", "Enter the AOI Name separate by Comma (e.g., FAY, CLT, RDU):", initialvalue='CHS, CLT, FAY, GSP, RDU, AVL, CAE')

    AOI_value= AOI_value.replace(" ", "")

    open_file.aoi_values_to_keep = AOI_value.split(",")


    df = merge_csv_to_excel()
    
    open_file.var = threshold_value
    if df is not None:
        # Format and process data
        df = format_timestamp_column(df)
        df = df.sort_values(by='Timestamp')
        rtwp_columns = gettask.columns_n70_71 + gettask.columns_n66_26 + gettask.columns_n66_26_Car1 + gettask.columns_N29
        df = process_rtwp_columns(df, rtwp_columns)

        progress_popup, progress_bar = show_progress_popup("Loading and Processing Data...")
        
        # Start processing in a separate thread
        threading.Thread(target=load_and_process_data, args=(df, progress_popup, progress_bar)).start()

# Data loading and UI creation function
def load_and_process_data(df, progress_popup, progress_bar):
    # Set the chunk size
    chunk_size = 1000

    # Process each chunk and store it in a list
    chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
    try:
        
        # Process each chunk and store it in a list
        dfchunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
        
        # df = pd.read_csv(file_path, chunksize=10000)  # Read in chunks for large files
        total_rows = 0


        # Initialize empty DataFrame to collect chunks
        data = pd.DataFrame()

        # Process each chunk
        for idx, chunk in enumerate(dfchunks):
            data = pd.concat([data, chunk], ignore_index=True)
            total_rows += len(chunk)
            
            # Update progress in the footer every 10% of the chunks
            if idx % 10 == 0:
                row_status.set(f"Loading... {total_rows} rows loaded")
                root.update_idletasks()

        row_status.set("Ready")
        root.after(0, create_ui, root, data)  # Create UI after processing
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        root.after(0, close_progress_popup, progress_popup, progress_bar)  # Ensure popup closes

# Function to create UI with threshold input
def create_ui(root, df):
    # Clear previous widgets (if any)
    for widget in root.winfo_children():
        widget.destroy()

    # Show a new progress popup for tree processing
    progress_popup, progress_bar = show_progress_popup("Processing Tree Structure...")

    # Schedule tree creation to happen in a new thread
    threading.Thread(target=create_tree_structure, args=(root, df, progress_popup, progress_bar)).start()

    # Add footer label
    footer_frame = Frame(root)
    footer_frame.pack(side=BOTTOM, fill=X)
    Label(footer_frame, textvariable=row_status, anchor=W, fg="blue").pack(side=LEFT, padx=10, pady=5)

# Function to populate the tree structure
def create_tree_structure(root, df, progress_popup, progress_bar):
    row_status.set("Building Tree Structure...")

    # Example tree creation logic (insert your tree generation code here)
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Add "File" menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", font=('Helvetica', 12, 'bold'), menu=file_menu)
    file_menu.add_command(label="Open CSV", command=lambda: open_file())
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Create a frame for the left-side tree view
    left_frame = Frame(root)
    left_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a frame for the right-side graphs
    right_frame = Frame(root)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Create a search bar to filter nodes
    search_frame = Frame(left_frame)
    search_frame.pack(fill=X)
    search_label = Label(search_frame, text=gettask.Task + str(open_file.var), font=('Helvetica', 12, 'bold'))
    search_label.pack(side=LEFT, padx=10)
    search_entry = Entry(search_frame)
    search_entry.pack(side=LEFT, padx=10, fill=X, expand=True)
    search_entry.pack_forget()
    

    # Create a tree view for Region -> AOI -> Site Name -> RU IP (Main Tree)
    tree_frame = Frame(left_frame)
    tree_frame.pack(expand=True, fill=BOTH)

    tree = ttk.Treeview(tree_frame)
    tree.pack(expand=True, side=LEFT, fill=BOTH)

    # Add scrollbar to the main tree
    scrollbar = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # Define a tag for the red color
    tree.tag_configure('red', foreground='red')

    # Function to recursively set parent nodes to red
    def set_parent_red(node):
        parent = tree.parent(node)
        if parent:
            tree.item(parent, tags=('red',))
            set_parent_red(parent)

    # Function to populate the red-tagged nodes under "Red Tagged Nodes" in the main tree
    def populate_red_tree():
        # Add a new top-level region for red-tagged nodes
        red_tag_region = tree.insert('', 'end', text='Nodes with Issue', tags=('red',))

        unique_regions = df['Region'].unique()
        for region in unique_regions:
            aois = df[df['Region'] == region]['AOI'].unique()
            for aoi in aois:
                sites = df[df['AOI'] == aoi]['Site Name'].unique()
                for site in sites:
                    ru_ips = df[df['Site Name'] == site]['RU IP'].unique()
                    for ru_ip in ru_ips:
                        # Check if any of the N70/71 columns exceed the threshold
                        df_filtered = df[df['RU IP'] == ru_ip]
                        if not df_filtered.empty and df_filtered.apply(is_above_threshold, axis=1).any():
                            # Add entry under "Red Tagged Nodes" in the format "AOI_SiteName_RUIP"
                            tree.insert(red_tag_region, 'end', text=f"{site}_{ru_ip}", values=(ru_ip,), tags=('red',))

    # Function to populate the main tree with all nodes initially
    def populate_tree():
        for item in tree.get_children():
            tree.delete(item)  # Clear tree before populating

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
                        # Check if any of the N70/71 columns exceed the threshold
                        df_filtered = df[df['RU IP'] == ru_ip]
                        if not df_filtered.empty and df_filtered.apply(is_above_threshold, axis=1).any():
                            # Add _Red suffix to the RU IP text if above threshold
                            ru_ip_text = f"{ru_ip}_Red"
                            # Insert RU IP with red color and the _Red suffix
                            ru_id_node = tree.insert(site_node, 'end', text=ru_ip_text, values=(ru_ip,), tags=('red',))
                            set_parent_red(ru_id_node)  # Recursively mark parents as red
                        else:
                            # Insert normally if not above threshold
                            tree.insert(site_node, 'end', text=ru_ip, values=(ru_ip,))

        # Populate the red-tagged nodes under "Red Tagged Nodes"
        populate_red_tree()

    # Populate the main tree and red-tagged nodes initially
    populate_tree()

    # Function to handle filtering by search input
    def filter_tree(filter_text):
        # Perform case-insensitive filtering on Region, AOI, Site Name, and RU IP
        for item in tree.get_children():
            tree.delete(item)  # Clear all items before filtering

        unique_regions = df['Region'].unique()
        for region in unique_regions:
            region_matches = filter_text.lower() in region.lower()
            region_node = None
            aois = df[df['Region'] == region]['AOI'].unique()
            for aoi in aois:
                aoi_matches = filter_text.lower() in aoi.lower()
                aoi_node = None
                sites = df[df['AOI'] == aoi]['Site Name'].unique()
                for site in sites:
                    site_matches = filter_text.lower() in site.lower()
                    site_node = None
                    ru_ips = df[df['Site Name'] == site]['RU IP'].unique()
                    for ru_ip in ru_ips:
                        ru_ip_matches = filter_text.lower() in ru_ip.lower()

                        if region_matches or aoi_matches or site_matches or ru_ip_matches:
                            # Create the parent nodes if they don't exist yet
                            if not region_node:
                                region_node = tree.insert('', 'end', text=region)
                            if not aoi_node:
                                aoi_node = tree.insert(region_node, 'end', text=aoi)
                            if not site_node:
                                site_node = tree.insert(aoi_node, 'end', text=site)
                            
                            # Check if any of the N70/71 columns exceed the threshold
                            df_filtered = df[df['RU IP'] == ru_ip]
                            if not df_filtered.empty and df_filtered.apply(is_above_threshold, axis=1).any():
                                # Add _Red suffix to the RU IP text if above threshold
                                ru_ip_text = f"{ru_ip}_Red"
                                # Insert RU IP with red color and the _Red suffix
                                ru_id_node = tree.insert(site_node, 'end', text=ru_ip_text, values=(ru_ip,), tags=('red',))
                                set_parent_red(ru_id_node)  # Recursively mark parents as red
                            else:
                                # Insert normally if not above threshold
                                tree.insert(site_node, 'end', text=ru_ip, values=(ru_ip,))

        # Repopulate the red-tagged tree under "Red Tagged Nodes"
        populate_red_tree()

    # Function to handle filtering by any text on pressing Enter
    def filter_site_names(event):
        filter_text = search_entry.get()
        if filter_text.strip() == "":
            populate_tree()  # If search text is empty, repopulate full tree
        else:
            filter_tree(filter_text)

    # Bind the Entry field to trigger the filter function on hitting "Enter"
    search_entry.bind('<Return>', filter_site_names)

    # Function to handle selection in the tree and plot the graph
    def on_tree_select(event):
        selected_item = tree.focus()
        selected_values = tree.item(selected_item, 'values')
        if selected_values:  # If an RU IP is selected, plot all 4 graphs
            ru_ip = selected_values[0]
            plot_graph(df, ru_ip, right_frame)

    # Bind tree selection event to both the main and red-tagged nodes
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    for index, row in df.iterrows():
        # Simulate processing for each row to populate the tree view
        pass  # Insert your tree creation logic

        # Update progress in the footer every 10%
        if index % (len(df) // 10) == 0:
            row_status.set(f"Processing Tree... {index} rows added")
            root.update_idletasks()

    row_status.set("Ready")
    root.after(0, close_progress_popup, progress_popup, progress_bar)  # Close popup after tree is built

# Main application function
def run_app():
    global root, row_status
    root = Tk()
    root.title('RTWP Data Graph Viewer')
    root.state('zoomed')
    root.resizable(True, True)

    # Initialize row status
    row_status = StringVar()
    row_status.set("")

    # Menu setup
    menu = Menu(root)
    root.config(menu=menu)
    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=open_file)

    # Footer frame and label for row loading status
    footer_frame = Frame(root)
    footer_frame.pack(side=BOTTOM, fill=X)
    Label(footer_frame, textvariable=row_status, anchor=W, fg="blue").pack(side=LEFT, padx=10, pady=5)

    root.mainloop()

# Run main application
run_app()
