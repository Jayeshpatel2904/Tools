import os
import shutil
import time
from tkinter import filedialog
from tkinter import Tk

def rename_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path!")
        return

    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            # creation_time = os.path.getctime(os.path.join(folder_path, filename))
            modified_time = os.path.getmtime(os.path.join(folder_path, filename))
            # print(creation_time)
            # formatted_ctime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(creation_time))
            formatted_mtime = time.strftime("%Y%m%d_%H%M%S", time.localtime(modified_time))
            # print(formatted_ctime)
            # new_filename = formatted_time + "_" + filename
            x = filename.split(".")

            extension = x[-1]
            new_filename = formatted_mtime + "." + extension
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            print(f"Renamed {filename} to {new_filename}")

def select_folder():
    root = Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Select folder")
    root.destroy()  # Close the hidden main window

    return folder_path

def main():
    folder_path = select_folder()
    if folder_path:
        rename_files_in_folder(folder_path)
        print("All files renamed successfully!")
    else:
        print("No folder selected.")

if __name__ == "__main__":
    main()
