import os
import shutil
from tkinter import filedialog
import zipfile

# Replace 'path/to/source/files' with the path to the folder containing your files
source_folder = filedialog.askdirectory()

# Replace 'path/to/destination/archive' with the path to the destination archive folder

destination_Zipped = source_folder + "\Zipped_Folder"


isExist1 = os.path.exists(destination_Zipped)



if not isExist1:
    # Create a new directory because it does not exist 
    os.makedirs(destination_Zipped)

for filename in os.listdir(source_folder):
    if os.path.isfile(os.path.join(source_folder, filename)):
        # Create a folder with the file's name (without extension) in the destination folder
        folder_name = os.path.splitext(filename)[0]
        destination_folder = os.path.join(destination_Zipped, folder_name)
        os.makedirs(destination_folder, exist_ok=True)
        
        # Copy the file to the destination folder
        shutil.copy(os.path.join(source_folder, filename), destination_folder)
        
        # Create a zip file for the folder's contents
        zip_filename = os.path.join(destination_Zipped, f'{folder_name}.zip')
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(destination_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, destination_folder)
                    zipf.write(file_path, arcname)

print("Files moved to separate archive folders.")