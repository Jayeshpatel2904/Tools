import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load Excel data and process it
def load_excel_file():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not filepath:
        return None

    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(filepath)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file: {str(e)}")
        return None

# List of columns to plot
columns_to_plot = [
    'RTWP N70/71 Ant-A Car-0', 'RTWP N70/71 Ant-B Car-0', 
    'RTWP N70/71 Ant-C Car-0', 'RTWP N70/71 Ant-D Car-0'
]

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

# Function to plot the graph for selected RU IP
def plot_graph(df, ru_ip, canvas_frame):
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
    
    # Plot each RTWP column with respective labels
    ax.plot(df_filtered['Timestamp'], df_filtered['RTWP N70/71 Ant-A Car-0'], label='Ant-A', color='blue')
    ax.plot(df_filtered['Timestamp'], df_filtered['RTWP N70/71 Ant-B Car-0'], label='Ant-B', color='green')
    ax.plot(df_filtered['Timestamp'], df_filtered['RTWP N70/71 Ant-C Car-0'], label='Ant-C', color='red')
    ax.plot(df_filtered['Timestamp'], df_filtered['RTWP N70/71 Ant-D Car-0'], label='Ant-D', color='orange')

    # Set plot labels and title
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('RTWP Value')
    ax.set_title(f'RTWP N70/71 Graph for RU IP: {ru_ip}')
    
    # Display the legend
    ax.legend()

    # Embed the plot in the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)

# Function to load the data and show in tree
def create_ui(df):
    root = Tk()
    root.title("RU IP Selector")

    # Create a frame for the left-side tree view
    left_frame = Frame(root)
    left_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a frame for the right-side graph
    right_frame = Frame(root)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Create a tree view for Site Name and RU IP
    tree = ttk.Treeview(left_frame)
    tree.pack(expand=True, fill=BOTH)

    # Create tree structure for Site Name -> RU IP
    unique_sites = df['Site Name'].unique()
    for site in unique_sites:
        site_node = tree.insert('', 'end', text=site)
        ru_ips = df[df['Site Name'] == site]['RU IP'].unique()
        for ru_ip in ru_ips:
            tree.insert(site_node, 'end', text=ru_ip, values=(ru_ip,))

    # Function to handle selection in the tree
    def on_tree_select(event):
        selected_item = tree.focus()
        selected_ru_ip = tree.item(selected_item, 'values')
        if selected_ru_ip:
            plot_graph(df, selected_ru_ip[0], right_frame)

    # Bind tree selection event
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    # Start the UI loop
    root.mainloop()

# Main function to load the Excel file and start the UI
def main():
    # Load the Excel file (adjust path or use a file dialog)
    df = load_excel_file()

    if df is not None:
        # Format the Timestamp column
        df = format_timestamp_column(df)
        # Process all RTWP columns
        rtwp_columns = columns_to_plot
        df = process_rtwp_columns(df, rtwp_columns)
        # Create UI with the data
        create_ui(df)

if __name__ == "__main__":
    main()
