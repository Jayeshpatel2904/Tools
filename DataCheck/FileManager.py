import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import datetime

class FileSearcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Searcher Tool")

        # Make window full screen by default
        self.state('zoomed')

        # Default file type and action choice
        self.file_type = tk.StringVar(value="All")
        self.action_choice = tk.StringVar(value="Details")

        # Configure grid to expand
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Source Folder Selection
        source_folder_label = tk.Label(self, text="Source Folder:")
        source_folder_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.source_folder_entry = tk.Entry(self, width=60)
        self.source_folder_entry.grid(row=0, column=1, sticky="we", padx=10, pady=10)
        
        source_folder_button = tk.Button(self, text="Browse", command=self.select_source_folder)
        source_folder_button.grid(row=0, column=2, padx=10, pady=10)

        # File Type Selection
        file_type_label = tk.Label(self, text="Select File Type:")
        file_type_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        file_type_menu = ttk.Combobox(self, textvariable=self.file_type, values=["All", "Excel", "PDF", "TXT", "Images", "Audio", "Video"])
        file_type_menu.grid(row=1, column=1, sticky="we", padx=10, pady=10)
        file_type_menu.current(0)

        # Search in Subfolders Option
        self.search_subfolders = tk.BooleanVar()
        search_subfolders_check = tk.Checkbutton(self, text="Include Subfolders", variable=self.search_subfolders)
        search_subfolders_check.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Search Specific Text in File Name
        specific_text_label = tk.Label(self, text="Search for Text in File Name:")
        specific_text_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.specific_text_entry = tk.Entry(self, width=60)
        self.specific_text_entry.grid(row=3, column=1, sticky="we", padx=10, pady=10)

        # Action Selection (All in One Line: Copy, Details, Rename, Rename and Copy, Move)
        action_label = tk.Label(self, text="Choose Action:")
        action_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)

        action_frame = tk.Frame(self)
        action_frame.grid(row=4, column=1, columnspan=2, sticky="w")

        action_copy = tk.Radiobutton(action_frame, text="Copy Files", variable=self.action_choice, value="Copy")
        action_copy.pack(side="left", padx=10, pady=5)

        action_details = tk.Radiobutton(action_frame, text="Get Details", variable=self.action_choice, value="Details")
        action_details.pack(side="left", padx=10, pady=5)

        action_rename = tk.Radiobutton(action_frame, text="Rename Files", variable=self.action_choice, value="Rename")
        action_rename.pack(side="left", padx=10, pady=5)

        action_rename_copy = tk.Radiobutton(action_frame, text="Rename & Copy", variable=self.action_choice, value="Rename and Copy")
        action_rename_copy.pack(side="left", padx=10, pady=5)

        action_move = tk.Radiobutton(action_frame, text="Move Files", variable=self.action_choice, value="Move")
        action_move.pack(side="left", padx=10, pady=5)

        # Rename Text Fields (Visible only if Rename or Rename & Copy is selected)
        rename_label = tk.Label(self, text="Replace Text:")
        rename_label.grid(row=8, column=0, sticky="w", padx=10, pady=10)
        self.replace_text_entry = tk.Entry(self, width=20)
        self.replace_text_entry.grid(row=8, column=1, sticky="we", padx=10, pady=10)

        rename_new_label = tk.Label(self, text="With New Text:")
        rename_new_label.grid(row=9, column=0, sticky="w", padx=10, pady=10)
        self.new_text_entry = tk.Entry(self, width=20)
        self.new_text_entry.grid(row=9, column=1, sticky="we", padx=10, pady=10)

        # Destination Folder Selection for Copy, Move, and Rename & Copy
        destination_folder_label = tk.Label(self, text="Destination Folder (for Copy, Move, Rename & Copy):")
        destination_folder_label.grid(row=10, column=0, sticky="w", padx=10, pady=10)
        
        self.destination_folder_entry = tk.Entry(self, width=60)
        self.destination_folder_entry.grid(row=10, column=1, sticky="we", padx=10, pady=10)
        
        destination_folder_button = tk.Button(self, text="Browse", command=self.select_destination_folder)
        destination_folder_button.grid(row=10, column=2, padx=10, pady=10)

        # Search Button
        search_button = tk.Button(self, text="Start Action", command=self.perform_action)
        search_button.grid(row=11, column=1, padx=10, pady=10)

        # Table for displaying results
        self.create_table()

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=12, column=0, columnspan=3, sticky="we", padx=10, pady=10)

    def create_table(self):
        # Table (Treeview) to display the file details
        columns = ('File Name', 'File Path', 'Size (bytes)', 'Modified Time')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col == 'File Name' else 200, anchor='w')

        self.tree.grid(row=11, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=11, column=3, sticky='ns', padx=(0, 10), pady=10)

    def clear_table(self):
        # This will remove all items from the table
        for row in self.tree.get_children():
            self.tree.delete(row)

    def select_source_folder(self):
        folder_selected = filedialog.askdirectory()
        self.source_folder_entry.delete(0, tk.END)
        self.source_folder_entry.insert(0, folder_selected)

    def select_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        self.destination_folder_entry.delete(0, tk.END)
        self.destination_folder_entry.insert(0, folder_selected)

    def search_files(self):
        source_folder = self.source_folder_entry.get()
        if not source_folder:
            messagebox.showerror("Error", "Please select a source folder.")
            return []
        
        file_type = self.file_type.get()
        search_subfolders = self.search_subfolders.get()
        specific_text = self.specific_text_entry.get().lower()

        # Determine file extensions based on selected file type
        if file_type == "Excel":
            file_extensions = [".xls", ".xlsx"]
        elif file_type == "PDF":
            file_extensions = [".pdf"]
        elif file_type == "TXT":
            file_extensions = [".txt"]
        elif file_type == "Images":
            file_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
        elif file_type == "Audio":
            file_extensions = [".mp3", ".wav", ".aac"]
        elif file_type == "Video":
            file_extensions = [".mp4", ".avi", ".mkv"]
        else:
            file_extensions = None  # For 'All', we don't filter by extension

        files_found = []
        # Start searching files
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                if file_extensions is None or any(file.lower().endswith(ext) for ext in file_extensions):
                    if specific_text in file.lower():
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

                        # Store file details for later processing
                        files_found.append((file, file_path, file_size, file_mod_time))

            if not search_subfolders:
                break  # If not searching subfolders, stop after the first iteration

        return files_found

    def perform_action(self):
        # Clear table before displaying new search results
        self.clear_table()

        action = self.action_choice.get()
        files = self.search_files()

        if not files:
            messagebox.showerror("Error", "No files found!")
            return

        # Set progress bar length to the number of files found
        self.progress_bar["maximum"] = len(files)
        self.progress_bar["value"] = 0

        if action == "Copy":
            self.copy_files(files)
        elif action == "Details":
            messagebox.showinfo("Info", f"File details are displayed in the table.\nTotal files found: {len(files)}")
        elif action == "Rename":
            self.rename_files(files)
        elif action == "Rename and Copy":
            self.rename_and_copy_files(files)
        elif action == "Move":
            self.move_files(files)

    def copy_files(self, files):
        destination_folder = self.destination_folder_entry.get()
        if not destination_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        for idx, file_info in enumerate(files, start=1):
            file_name, file_path, _, _ = file_info
            destination_path = os.path.join(destination_folder, file_name)
            shutil.copy2(file_path, destination_path)

            # Update the progress bar
            self.progress_bar["value"] = idx
            self.update_idletasks()

        messagebox.showinfo("Success", f"{len(files)} files copied successfully!")

    def rename_files(self, files):
        replace_text = self.replace_text_entry.get()
        new_text = self.new_text_entry.get()

        if not replace_text or not new_text:
            messagebox.showerror("Error", "Please provide text to replace and new text.")
            return

        renamed_count = 0
        for idx, file_info in enumerate(files, start=1):
            file_name, file_path, _, _ = file_info
            new_file_name = file_name.replace(replace_text, new_text)
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

            os.rename(file_path, new_file_path)
            renamed_count += 1

            # Update the progress bar
            self.progress_bar["value"] = idx
            self.update_idletasks()

        messagebox.showinfo("Success", f"{renamed_count} files renamed successfully!")

    def rename_and_copy_files(self, files):
        replace_text = self.replace_text_entry.get()
        new_text = self.new_text_entry.get()
        destination_folder = self.destination_folder_entry.get()

        if not replace_text or not new_text:
            messagebox.showerror("Error", "Please provide text to replace and new text.")
            return

        if not destination_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        renamed_copied_count = 0
        for idx, file_info in enumerate(files, start=1):
            file_name, file_path, _, _ = file_info
            new_file_name = file_name.replace(replace_text, new_text)
            destination_path = os.path.join(destination_folder, new_file_name)
            
            shutil.copy2(file_path, destination_path)
            renamed_copied_count += 1

            # Update the progress bar
            self.progress_bar["value"] = idx
            self.update_idletasks()

        messagebox.showinfo("Success", f"{renamed_copied_count} files renamed and copied successfully!")

    def move_files(self, files):
        destination_folder = self.destination_folder_entry.get()
        if not destination_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        moved_count = 0
        for idx, file_info in enumerate(files, start=1):
            file_name, file_path, _, _ = file_info
            destination_path = os.path.join(destination_folder, file_name)
            shutil.move(file_path, destination_path)
            moved_count += 1

            # Update the progress bar
            self.progress_bar["value"] = idx
            self.update_idletasks()

        messagebox.showinfo("Success", f"{moved_count} files moved successfully!")

if __name__ == "__main__":
    app = FileSearcherApp()
    app.mainloop()
