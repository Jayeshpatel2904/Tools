import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Scrollbar
from tkinter import ttk

def select_source_folder():
    folder_path = filedialog.askdirectory(title="Select Source Folder with Files")
    source_folder_entry.delete(0, 'end')  # Clear any existing path
    source_folder_entry.insert(0, folder_path)
    populate_file_table()  # Update the table when a source folder is selected

def select_destination_folder():
    folder_path = filedialog.askdirectory(title="Select Destination Folder to Save Renamed Files")
    destination_folder_entry.delete(0, 'end')  # Clear any existing path
    destination_folder_entry.insert(0, folder_path)

def populate_file_table():
    # Clear the existing data in the table
    for row in file_table.get_children():
        file_table.delete(row)

    source_folder = source_folder_entry.get()
    old_text = old_text_entry.get()
    new_text = new_text_entry.get()

    if not source_folder:
        return  # Do nothing if no source folder is selected

    try:
        # List only files (exclude directories)
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        for filename in files:
            # Show current file name and the new name (if old_text and new_text are set)
            new_name = filename.replace(old_text, new_text) if old_text and new_text else ""
            file_table.insert("", "end", values=(filename, new_name))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def rename_files():
    source_folder = source_folder_entry.get()
    destination_folder = destination_folder_entry.get()
    old_text = old_text_entry.get()
    new_text = new_text_entry.get()

    if not source_folder:
        messagebox.showerror("Error", "Please select a source folder.")
        return
    if not destination_folder:
        messagebox.showerror("Error", "Please select a destination folder.")
        return
    if not old_text:
        messagebox.showerror("Error", "Please enter the text to replace.")
        return
    if not new_text:
        messagebox.showerror("Error", "Please enter the new text.")
        return

    try:
        # List only files (exclude directories)
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        renamed_files_count = 0
        for filename in files:
            if old_text in filename:
                # Replace the old text with new text in the filename
                new_name = filename.replace(old_text, new_text)
                
                source_path = os.path.join(source_folder, filename)
                destination_path = os.path.join(destination_folder, new_name)
                
                # Rename the file and move it to the destination folder
                os.rename(source_path, destination_path)
                renamed_files_count += 1

        messagebox.showinfo("Success", f"Renamed {renamed_files_count} files successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    global source_folder_entry, destination_folder_entry, old_text_entry, new_text_entry, file_table

    # Create the main window
    root = Tk()
    root.title("Bulk File Renamer")
    root.state('zoomed')  # Start maximized (shows minimize and close buttons)

    # Create layout frames
    input_frame = ttk.Frame(root, padding="10")
    input_frame.pack(fill="x", pady=10)

    # Grid layout for side-by-side arrangement

    # Select Source Folder and Destination Folder side by side
    Label(input_frame, font=('Arial', 12, 'bold'), text="Select Source Folder:").grid(row=0, column=0, sticky="w", padx=5)
    source_folder_entry = Entry(input_frame, width=40)
    source_folder_entry.grid(row=0, column=1, padx=5)
    Button(input_frame, text="Browse", font=('Arial', 12, 'bold'),command=select_source_folder).grid(row=0, column=2, padx=5)

    Label(input_frame, font=('Arial', 12, 'bold'), text="Select Destination Folder:").grid(row=0, column=3, sticky="w", padx=5)
    destination_folder_entry = Entry(input_frame, width=40)
    destination_folder_entry.grid(row=0, column=4, padx=5)
    Button(input_frame, text="Browse", font=('Arial', 12, 'bold'),command=select_destination_folder).grid(row=0, column=5, padx=5)

    # Text to Replace and New Text side by side
    Label(input_frame, font=('Arial', 12, 'bold'), text="Text to Replace:").grid(row=1, column=0, sticky="w", padx=5)
    old_text_entry = Entry(input_frame, width=40)
    old_text_entry.grid(row=1, column=1, padx=5)

    Label(input_frame, font=('Arial', 12, 'bold'), text="New Text:").grid(row=1, column=3, sticky="w", padx=5)
    new_text_entry = Entry(input_frame, width=40)
    new_text_entry.grid(row=1, column=4, padx=5)

    # Button to Preview the changes
    Button(input_frame, text="Preview Changes", font=('Arial', 12, 'bold'), command=populate_file_table).grid(row=2, column=1, columnspan=4, pady=10)

    # Create a Treeview (table) to show files
    table_frame = ttk.Frame(root, padding="10")
    table_frame.pack(fill="both", expand=True)

    # Scrollbar for the table
    scrollbar = Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # Define the table columns and Treeview with grid lines
    style = ttk.Style()
    style.configure("Treeview", rowheight=25, borderwidth=1)
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.map("Treeview", background=[('selected', '#ececec')])
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    file_table = ttk.Treeview(table_frame, columns=("Current File Name", "New File Name"), show="headings", yscrollcommand=scrollbar.set)
    file_table.heading("Current File Name", text="Current File Name")
    file_table.heading("New File Name", text="New File Name")
    file_table.column("Current File Name", anchor="w", width=400)
    file_table.column("New File Name", anchor="w", width=400)
    file_table.pack(fill="both", expand=True)
    scrollbar.config(command=file_table.yview)

    # Alternating row colors for better readability
    file_table.tag_configure('oddrow', background='#f0f0f0')
    file_table.tag_configure('evenrow', background='#ffffff')

    # Button to Rename files
    Button(root, text="Rename Files", font=('Arial', 12, 'bold'), command=rename_files, bg="green", fg="white").pack(pady=20)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
