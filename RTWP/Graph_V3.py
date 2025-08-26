import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, asksaveasfilename


# Function to merge selected CSV files, filter specific columns, and filter AOI values
def merge_csv_to_excel():
    # List of columns to keep
    columns_to_keep = [
        "Timestamp", "Region", "AOI", "Cluster Name", "Site Name", "RU IP",
        "RTWP N70/71 Ant-A Car-0", "RTWP N70/71 Ant-B Car-0", "RTWP N70/71 Ant-C Car-0", "RTWP N70/71 Ant-D Car-0",
        "RTWP N66/26 Ant-A Car-0", "RTWP N66/26 Ant-A Car-1", "RTWP N66/26 Ant-B Car-0", "RTWP N66/26 Ant-B Car-1",
        "RTWP N66/26 Ant-C Car-0", "RTWP N66/26 Ant-C Car-1", "RTWP N66/26 Ant-D Car-0", "RTWP N66/26 Ant-D Car-1",
        "RTWP N29 Ant-A Car-0", "RTWP N29 Ant-B Car-0", "RTWP N29 Ant-C Car-0", "RTWP N29 Ant-D Car-0"
    ]

    # AOI values to keep
    aoi_values_to_keep = ["CHS", "CLT", "FAY", "GSP", "RDU", "AVL", "CAE"]

    # Hide the main tkinter window
    Tk().withdraw()

    # Open file dialog to select multiple CSV files
    csv_files = askopenfilenames(filetypes=[("CSV files", "*.csv")], title="Select CSV Files to Merge")

    # Open save dialog to specify where to save the merged Excel file
    output_excel_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save Merged Excel File As")

    if not csv_files or not output_excel_path:
        print("No files selected or no save location chosen. Exiting...")
        return

    # List to hold DataFrames
    dataframes = []

    # Loop through selected CSV files and read them into DataFrames
    for file in csv_files:
        df = pd.read_csv(file)

        # Keep only the specified columns
        df_filtered = df[columns_to_keep]

        # Print the unique values in AOI before cleaning
        print("Unique AOI values before cleaning:", df_filtered["AOI"].unique())

        # Clean AOI column (strip spaces and standardize case)
        df_filtered["AOI"] = df_filtered["AOI"].str.strip().str.upper()


        # Filter the AOI column to include only the specified AOI values
        df_filtered = df_filtered[df_filtered["AOI"].isin([aoi.upper() for aoi in aoi_values_to_keep])]

        # Print the DataFrame after filtering to see if it contains the correct AOI values
        

        dataframes.append(df_filtered)

    # Merge all DataFrames row-wise
    df = pd.concat(dataframes, ignore_index=True)

    # # Save the merged DataFrame to an Excel file
    # df.to_excel(output_excel_path, index=False)


    try:
        
        if df is not None:
            # Format the Timestamp column
            df = format_timestamp_column(df)
            # Process all RTWP columns for both N70/71 and N66/26
            rtwp_columns = columns_n70_71 + columns_n66_26 + columns_n66_26_Car1 + columns_N29
            df = process_rtwp_columns(df, rtwp_columns)
            # Create the UI with the loaded data
            create_ui(df)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {str(e)}")

    print(f"Merged file saved as {output_excel_path}")

# Example usage


# List of columns for N70/71 and N66/26
columns_n70_71 = ['RTWP N70/71 Ant-A Car-0', 'RTWP N70/71 Ant-B Car-0', 'RTWP N70/71 Ant-C Car-0', 'RTWP N70/71 Ant-D Car-0']
columns_n66_26 = ['RTWP N66/26 Ant-A Car-0', 'RTWP N66/26 Ant-B Car-0', 'RTWP N66/26 Ant-C Car-0', 'RTWP N66/26 Ant-D Car-0']
columns_n66_26_Car1 = ['RTWP N66/26 Ant-A Car-1', 'RTWP N66/26 Ant-B Car-1', 'RTWP N66/26 Ant-C Car-1', 'RTWP N66/26 Ant-D Car-1']
columns_N29 = ['RTWP N29 Ant-A Car-0', 'RTWP N29 Ant-B Car-0', 'RTWP N29 Ant-C Car-0', 'RTWP N29 Ant-D Car-0']

# Function to format the Timestamp column
def format_timestamp_column(df):
    if 'Timestamp' in df.columns:
        try:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.replace('_', ' '))
        except Exception as e:
            messagebox.showerror("Error", f"Error formatting Timestamp column: {str(e)}")
    else:
        messagebox.showerror("Error", "Timestamp column not found in the data.")
    return df

# Function to process and clean RTWP columns
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
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(compute_average)
        else:
            messagebox.showerror("Error", f"Column '{col}' not found in the data.")
    return df

# Function to plot the graph for selected RU IP and group (N70/71 or N66/26)
def plot_graph(df, ru_ip, group, canvas_frame):
    # Filter data based on selected RU IP
    df_filtered = df[df['RU IP'] == ru_ip]

    # Check if there is data to plot
    if df_filtered.empty:
        messagebox.showerror("Error", f"No data found for RU IP: {ru_ip}")
        return
    
    # Clear previous plots
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create a new figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot the respective group of columns
    if group == 'N70/71':
        columns = columns_n70_71
        labels = ['Ant-A', 'Ant-B', 'Ant-C', 'Ant-D']
    elif group == 'N66/26':
        columns = columns_n66_26
        labels = ['Ant-A', 'Ant-B', 'Ant-C', 'Ant-D']
    elif group == 'N66/26 Car1':
        columns = columns_n66_26_Car1
        labels = ['Ant-A', 'Ant-B', 'Ant-C', 'Ant-D']
    elif group == 'N29':
        columns = columns_N29
        labels = ['Ant-A', 'Ant-B', 'Ant-C', 'Ant-D']
    else:
        return

    # Plot each RTWP column with respective labels
    for col, label in zip(columns, labels):
        ax.plot(df_filtered['Timestamp'], df_filtered[col], label=label)

    # Set plot labels and title
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('RTWP Value')
    ax.set_title(f'{group} Graph for RU IP: {ru_ip}')
    
    # Display the legend
    ax.legend()

    # Embed the plot in the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)

# # Function to handle file opening
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        load_data(file_path)

# Function to load the data and show in tree
def create_ui(df):
    root = Tk()
    root.title("RU IP Selector")

    # Full-screen and no resizable window
    root.state('zoomed')
    root.resizable(False, False)

    # Create a menu for file operations
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    # menu_bar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu_bar)

    # Create a frame for the left-side tree view
    left_frame = Frame(root)
    left_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a frame for the right-side graph
    right_frame = Frame(root)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Create a tree view for Main Region -> AOI -> Cluster Name -> Site Name -> RU IP -> (N70/71, N66/26)
    tree = ttk.Treeview(left_frame)
    tree.pack(expand=True, fill=BOTH)

    # Create tree structure
    unique_main_regions = df['Region'].unique()
    for main_region in unique_main_regions:
        main_region_node = tree.insert('', 'end', text=main_region)
        aois = df[df['Region'] == main_region]['AOI'].unique()
        for aoi in aois:
            aoi_node = tree.insert(main_region_node, 'end', text=aoi)
            sites = df[df['AOI'] == aoi]['Site Name'].unique()
            for site in sites:
                site_node = tree.insert(aoi_node, 'end', text=site)
                ru_ips = df[df['Site Name'] == site]['RU IP'].unique()
                for ru_ip in ru_ips:
                    ru_ip_node = tree.insert(site_node, 'end', text=ru_ip, values=(ru_ip,))
                    tree.insert(ru_ip_node, 'end', text='N70/71', values=(ru_ip, 'N70/71'))
                    tree.insert(ru_ip_node, 'end', text='N66/26', values=(ru_ip, 'N66/26'))
                    tree.insert(ru_ip_node, 'end', text='N66/26 Car1', values=(ru_ip, 'N66/26 Car1'))
                    tree.insert(ru_ip_node, 'end', text='N29', values=(ru_ip, 'N29'))

    # Function to handle selection in the tree
    def on_tree_select(event):
        selected_item = tree.focus()
        selected_values = tree.item(selected_item, 'values')
        if selected_values and len(selected_values) == 2:  # Check if it's a group selection (N70/71 or N66/26)
            ru_ip, group = selected_values
            plot_graph(df, ru_ip, group, right_frame)

    # Bind tree selection event
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    # Start the UI loop
    root.mainloop()

# Function to load the data and process it
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        if df is not None:
            # Format the Timestamp column
            df = format_timestamp_column(df)
            # Process all RTWP columns for both N70/71 and N66/26
            rtwp_columns = columns_n70_71 + columns_n66_26 + columns_n66_26_Car1 + columns_N29
            df = process_rtwp_columns(df, rtwp_columns)
            # Create the UI with the loaded data
            create_ui(df)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {str(e)}")

# Main function to start the application
def main():
    # Start the application with an open file dialog
    merge_csv_to_excel()


if __name__ == "__main__":
    main()
