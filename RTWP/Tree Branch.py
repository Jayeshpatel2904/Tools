import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox

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
def on_tree_select(event, tree, df, table):
    selected_item = tree.selection()

    if selected_item:
        # Get the text of the selected item (Site Name or RU IP)
        item_text = tree.item(selected_item, 'text')
        
        # If the selected item is a Site Name, display the data for that site
        if item_text in df['Site Name'].values:
            show_site_data(item_text, df, table)
        # If it's an RU IP, filter the data by both Site Name and RU IP
        else:
            parent_item = tree.parent(selected_item)
            if parent_item:  # Get the parent (Site Name) of the selected RU IP
                parent_text = tree.item(parent_item, 'text')
                site_data = df[(df['Site Name'] == parent_text) & (df['RU IP'] == item_text)]
                show_site_data(parent_text, df, table)

# Create the main window
def create_ui(df):
    root = Tk()
    root.title("Excel Data Viewer")
    root.geometry("900x600")

    # Split the window into two sections: Tree on the left, Table on the right
    left_frame = Frame(root)
    left_frame.pack(side=LEFT, fill=Y)
    right_frame = Frame(root)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Create TreeView for Site Name and RU IP on the left
    tree = ttk.Treeview(left_frame)
    tree.heading('#0', text='Sites and RU IPs')
    tree.pack(fill=Y, expand=True)

    # Create Table for showing Excel data on the right
    table = ttk.Treeview(right_frame, columns=list(df.columns), show='headings')
    for col in df.columns:
        table.heading(col, text=col)
        table.column(col, width=100)
    table.pack(fill=BOTH, expand=True)

    # Populate the tree with Site Name and RU IP
    populate_tree(tree, df)

    # Bind selection event to the tree
    tree.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tree, df, table))

    root.mainloop()

# Main function to load the Excel file and start the UI
def main():
    df = load_excel_file()
    if df is not None:
        create_ui(df)

if __name__ == "__main__":
    main()
