# Import the required libraries
from tkinter import *
from tkinter import ttk, filedialog
import numpy
import pandas as pd

from tkinter import *
 
# creating tkinter window
root = Tk()
 
# getting screen's height in pixels
height = root.winfo_screenheight()
 
# getting screen's width in pixels
width = root.winfo_screenwidth()

# Create an instance of tkinter frame

# Set the size of the tkinter window
root.geometry("%dx%d" % (width, height))


# Create an object of Style widget
style = ttk.Style()
style.theme_use('clam')

# Create a Frame
frame = Frame(root)
frame.pack(pady=20)
# Define a function for opening the file
def open_file():
	filename = filedialog.askopenfilename(title="Open a File", filetype=(("Excel files", ".*xlsx"),("All Files", "*.")))

	if filename:
		try:
			filename = r"{}".format(filename)
			df = pd.read_excel(filename)
		except ValueError:
			label.config(text="File could not be opened")
		except FileNotFoundError:
			label.config(text="File Not Found")

	# Clear all the previous data in tree
	clear_treeview()

	# Add new data in Treeview widget
	tree["column"] = list(df.columns)
	tree["show"] = "headings"

	# For Headings iterate over the columns
	for col in tree["column"]:
		tree.heading(col, text=col)

	# Put Data in Rows
	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		tree.insert("", "end", values=row)

	tree.pack()

# Clear the Treeview Widget
def clear_treeview():
	tree.delete(*tree.get_children())

# Create a Treeview widget
tree = ttk.Treeview(frame)

# Add a Menu
m = Menu(root)
root.config(menu=m)

# Add Menu Dropdown
file_menu = Menu(m, tearoff=False)
m.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Open Spreadsheet", command=open_file)

# Add a Label widget to display the file content
label = Label(root, text='')
label.pack(pady=100)

root.mainloop()