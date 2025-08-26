import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET
from tkinter import ttk, filedialog, simpledialog, messagebox

# Load XML

 # Open file dialog to select multiple CSV files
# XML_files = filedialog.askopenfilenames(filetypes=[("XMLfiles", "*.xml")], title="Select xml Files to Merge")

XML_files = filedialog.askopenfilename(filetypes=[("XMLfiles", "*.xml")])


tree = ET.parse(XML_files)  # Replace with your file
root = tree.getroot()

# Create main window
app = tk.Tk()
app.title("XML Tree Viewer")
app.geometry("800x600")

# TreeView for XML structure
tree_frame = ttk.Frame(app)
tree_frame.pack(side='left', fill='y')

tree_view = ttk.Treeview(tree_frame)
tree_view.pack(fill='y', expand=True)

# Table for attributes/tags
table_frame = ttk.Frame(app)
table_frame.pack(side='right', fill='both', expand=True)

table = ttk.Treeview(table_frame, columns=('Attribute', 'Value'), show='headings')
table.heading('Attribute', text='Attribute')
table.heading('Value', text='Value')
table.pack(fill='both', expand=True)


# Recursive function to insert XML into tree view
def insert_node(parent, element):
    node_id = tree_view.insert(parent, 'end', text=element.tag)
    for child in element:
        insert_node(node_id, child)


# When a tree item is clicked
def on_tree_select(event):
    selected_item = tree_view.selection()
    if not selected_item:
        return

    # Find tag path from selection
    def get_element_by_id(item_id, current_element):
        if tree_view.item(item_id, "text") == current_element.tag:
            if not tree_view.get_children(item_id):  # If it's a leaf
                return current_element
            for i, child in enumerate(current_element):
                match = get_element_by_id(tree_view.get_children(item_id)[i], child)
                if match is not None:
                    return match
        return None

    def find_element(tree_ids, element):
        if not tree_ids:
            return element
        next_tag = tree_view.item(tree_ids[0], "text")
        for child in element:
            if child.tag == next_tag:
                return find_element(tree_ids[1:], child)
        return None

    def get_path(item_id):
        path = []
        while item_id:
            path.insert(0, item_id)
            item_id = tree_view.parent(item_id)
        return path

    path_ids = get_path(selected_item[0])
    element = root
    for id_ in path_ids[1:]:
        tag = tree_view.item(id_, 'text')
        for child in element:
            if child.tag == tag:
                element = child
                break

    # Clear previous table content
    for row in table.get_children():
        table.delete(row)

    # Insert attributes
    for key, value in element.attrib.items():
        table.insert('', 'end', values=(key, value))

    # Insert tag text if exists
    if element.text and element.text.strip():
        table.insert('', 'end', values=("Text", element.text.strip()))


# Bind selection
tree_view.bind("<<TreeviewSelect>>", on_tree_select)

# Fill tree view
insert_node('', root)

app.mainloop()
