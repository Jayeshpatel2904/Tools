import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET
from tkinter import ttk, filedialog, simpledialog, messagebox

# Load your XML file
xml_file = filedialog.askopenfilename(filetypes=[("XMLfiles", "*.xml")])

# Parse XML with namespace handling
tree = ET.parse(xml_file)
root = tree.getroot()
ns = {'ns': root.tag.split('}')[0].strip('{')}  # Extract namespace

# Create the main application window
app = tk.Tk()
app.title("XML Tree Viewer")
app.geometry("1000x600")

# Treeview for XML structure
tree_frame = ttk.Frame(app)
tree_frame.pack(side='left', fill='y')

tree_view = ttk.Treeview(tree_frame)
tree_view.pack(fill='y', expand=True)

# Table for attributes and text
table_frame = ttk.Frame(app)
table_frame.pack(side='right', fill='both', expand=True)

table = ttk.Treeview(table_frame, columns=('Attribute', 'Value'), show='headings')
table.heading('Attribute', text='Attribute')
table.heading('Value', text='Value')
table.pack(fill='both', expand=True)

# Store a reference to the full Element object
item_to_element = {}

# Recursive function to populate tree
def insert_node(parent, element):
    display = element.tag.split('}')[-1]
    node_id = tree_view.insert(parent, 'end', text=display)
    item_to_element[node_id] = element
    for child in element:
        insert_node(node_id, child)

# Event handler for selection
def on_tree_select(event):
    selected_item = tree_view.selection()
    if not selected_item:
        return
    element = item_to_element[selected_item[0]]
    table.delete(*table.get_children())
    for attr, val in element.attrib.items():
        table.insert('', 'end', values=(attr, val))
    text = (element.text or "").strip()
    if text:
        table.insert('', 'end', values=('Text', text))

# Bind event
tree_view.bind("<<TreeviewSelect>>", on_tree_select)

# Populate tree view
insert_node('', root)

app.mainloop()
