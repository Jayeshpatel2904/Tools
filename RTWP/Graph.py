import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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

# Build the treeview structure
def populate_tree(tree, df):
    tree.delete(*tree.get_children())  # Clear the tree
    unique_sites = df['Site Name'].unique()  # Get unique Site Names

    # Create tree items for each Site Name and its corresponding RU IPs
    for site in unique_sites:
        site_id = tree.insert('', 'end', text=site, open=True)
        site_data = df[df['Site Name'] == site]  # Filter rows for the current site
        unique_rus = site_data['RU IP'].unique()  # Get unique RU IPs for the site

        for ru in unique_rus:
            tree.insert(site_id, 'end', text=ru, open=True)

# Show table data in the right-side view when a Site Name is selected
def show_site_data(site_name, df, table):
    # Filter the data for the selected site
    site_data = df[df['Site Name'] == site_name]

    # Clear the table view
    for row in table.get_children():
        table.delete(row)

    # Add data to the table
    for _, row in site_data.iterrows():
        table.insert('', 'end', values=list(row))

# When a tree item (Site Name or RU IP) is selected, display corresponding data
def on_tree_select(event, tree, df, table, canvas_frame):
    selected_item = tree.selection()

    if selected_item:
        # Get the text of the selected item (Site Name or RU IP)
        item_text = tree.item(selected_item, 'text')
        
        # If the selected item is a Site Name, display the data for that site
        if item_text in df['Site Name'].values:
            show_site_data(item_text, df, table)
        # If it's an RU IP, filter the data by both Site Name and RU IP and show the graph
        else:
            parent_item = tree.parent(selected_item)
            if parent_item:  # Get the parent (Site Name) of the selected RU IP
                parent_text = tree.item(parent_item, 'text')
                site_data = df[(df['Site Name'] == parent_text) & (df['RU IP'] == item_text)]
                show_site_data(parent_text, df, table)
                plot_graph(site_data, canvas_frame)

# Function to plot the line graph for the selected RU IP
def plot_graph(site_data, canvas_frame):
    # Check if the required columns are present
    if "Timestamp" not in site_data.columns or "RTWP N70/71 Ant-A Car-0" not in site_data.columns:
        messagebox.showerror("Error", "Required columns are not present in the data")
        return

    # Convert 'Timestamp' to datetime if necessary
    site_data['Timestamp'] = pd.to_datetime(site_data['Timestamp'], errors='coerce')

    # Sort data by Timestamp
    site_data = site_data.sort_values(by='Timestamp')

    # Clear previous plot
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create a new figure and plot the data
    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot the line graph: 'RTWP N70/71 Ant-A Car-0' vs 'Timestamp'
    ax.plot(site_data['Timestamp'], site_data['RTWP N70/71 Ant-A Car-0'], marker='o', linestyle='-')

    # Customize the plot
    ax.set_title('RTWP N70/71 Ant-A Car-0 over Time')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('RTWP N70/71 Ant-A Car-0')
    ax.grid(True)

    # Embed the plot in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# Create the main window
def create_ui(df):
    root = Tk()
    root.title("Excel Data Viewer with Graph")
    root.geometry("1200x600")

    # Split the window into sections: Tree on the left, Table and Graph on the right
    left_frame = Frame(root)
    left_frame.pack(side=LEFT, fill=Y)
    right_frame = Frame(root)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Create TreeView for Site Name and RU IP on the left
    tree = ttk.Treeview(left_frame)
    tree.heading('#0', text='Sites and RU IPs')
    tree.pack(fill=Y, expand=True)

    # Create Table for showing Excel data on the right (top)
    table_frame = Frame(right_frame)
    table_frame.pack(fill=BOTH, expand=True)
    
    table = ttk.Treeview(table_frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        table.heading(col, text=col)
        table.column(col, width=100)
    table.pack(fill=BOTH, expand=True)

    # Create Canvas frame for plotting graphs (bottom)
    canvas_frame = Frame(right_frame)
    canvas_frame.pack(fill=BOTH, expand=True)

    # Populate the tree with Site Name and RU IP
    populate_tree(tree, df)

    # Bind selection event to the tree
    tree.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tree, df, table, canvas_frame))

    root.mainloop()

# Function to correct the 'Timestamp' format
def format_timestamp_column(df):
    # Assuming the Timestamp column contains strings like 'YYYY-MM-DD_HH:MM:SS'
    if 'Timestamp' in df.columns:
        try:
            # Split the column into date and time, remove the underscore, and reformat it
            df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.replace('_', ' '))
        except Exception as e:
            messagebox.showerror("Error", f"Error formatting Timestamp column: {str(e)}")
    else:
        messagebox.showerror("Error", "Timestamp column not found in the data.")
    return df

# Function to process the 'RTWP N70/71 Ant-A Car-0' column
def process_rtwp_column(df):
    if 'RTWP N70/71 Ant-A Car-0' in df.columns:
        def compute_average(value):
            # Split by ':::', and replace '-NA-' or blank with 0
            values = [v if v not in ['-NA-', '', None] else '0' for v in str(value).split(':::')]
            
            # Convert values to floats for numeric calculations
            numeric_values = []
            for v in values:
                try:
                    numeric_values.append(float(v))
                except ValueError:
                    numeric_values.append(0)  # Handle non-numeric cases
                
            # Calculate the average if numeric values exist, otherwise return 0
            return sum(numeric_values) / len(numeric_values) if numeric_values else 0

        # Apply the function to each row in the column
        df['RTWP N70/71 Ant-A Car-0'] = df['RTWP N70/71 Ant-A Car-0'].apply(compute_average)
    else:
        messagebox.showerror("Error", "RTWP N70/71 Ant-A Car-0 column not found in the data.")
    
    return df

# Main function to load the Excel file and start the UI
def main():
    df = load_excel_file()
    if df is not None:
        # Format the Timestamp column
        df = format_timestamp_column(df)
        # Process the 'RTWP N70/71 Ant-A Car-0' column
        df = process_rtwp_column(df)
        # Launch the UI with the formatted data
        create_ui(df)

if __name__ == "__main__":
    main()

