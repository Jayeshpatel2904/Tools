import glob
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import os
from tkinter import filedialog
from tkinter import *
import pandas as pd
import shutil
import os


root = Tk()
root.withdraw()
# folder_selected = filedialog.askdirectory()

# folderpath = folder_selected


# column_to_be_centered = [  [sg.ProgressBar(1, orientation='h',size=(100, 20), key='progress')],
#         [sg.Button('START')]]


layout = [[sg.T("")], 
        [sg.Text("                  Choose a Source folder: ",font=('Helvetica', 12, 'bold')), sg.InputText(key="-IN-",size=(100, None)),sg.FolderBrowse(key="-IN-",font=('Helvetica', 12, 'bold'))], [sg.T("")],
         [sg.Text("Choose excel sheet with filename: ",font=('Helvetica', 12, 'bold')), sg.InputText(key='Filename_List',size=(100, None)), sg.FileBrowse(font=('Helvetica', 12, 'bold'))], [sg.T("")],
        [sg.Text("                                    CycleNumber: ",font=('Helvetica', 12, 'bold')), sg.InputText(key='-Cycle-',size=(112, None))],
        [sg.T("")],
        [sg.T("")],
        [sg.Text('PROGRESS',font=('Helvetica', 12, 'bold'))],
        [sg.ProgressBar(1, orientation='h',size=(100, 20), key='progress')],
        [sg.T("")],
        [sg.Column(layout=[[sg.Button('START',font=('Helvetica', 12, 'bold'), size=(15, 1))]], justification='center')],
        ]


# layout = [
#         [sg.ProgressBar(1, orientation='h',size=(100, 20), key='progress')],
#         [sg.Button('START')]
        
#      ]

# layout = [[sg.VPush()],
#               [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
#               [sg.VPush()]]
# window = sg.Window('My new window', layout,
#                    size=(500, 100), grab_anywhere=True)


# layout = [sg.Button('START','center',size=(100,1))]
window = sg.Window('AOF FILE PICKER V1.5', layout)
progress_bar = window.FindElement('progress')


try:

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "START":
            excel_file_path = values["Filename_List"]
            source_folder = values["-IN-"]
            Cycle = values["-Cycle-"]
            window["Filename_List"].update('')
            window["-IN-"].update('')
            window["-Cycle-"].update('')

            # source_folder = filedialog.askdirectory()
            # excel_file_path = filedialog.askopenfilename()


            destination_folder = source_folder + "\Final"


            isExist1 = os.path.exists(destination_folder)



            if not isExist1:
                # Create a new directory because it does not exist 
                os.makedirs(destination_folder)

            # Paths
            sheet_name = 'Sheet1'  # Update with the name of your sheet containing filenames

            i = 0
            j = 0

            # Get list of filenames from the Excel column (assuming the column name is 'Filename')
            if excel_file_path != "":
                df = pd.read_excel(excel_file_path, sheet_name=0)
                progress_bar.UpdateBar(0, i)
                df.rename(columns={df.columns[0]:'Log filename'}, inplace=True)
                filenames = df['Log filename'].tolist()
                filenames.sort()

            else:
                file_names = [file for file in os.listdir(source_folder) if file.endswith('.aof')]
                # filenames = os.listdir(source_folder)
                data = {'Log filename': file_names}
                df = pd.DataFrame(data)
                df['Log filename'] = df['Log filename'].str[:14]
                unique_values = df['Log filename'].unique()
                filenames = unique_values.tolist()
                filenames.sort()
                print(filenames)


            # Count files
            for filename in filenames:
                first_14_chars = filename[:14]
                matching_files = [file for file in os.listdir(source_folder) if file.startswith(first_14_chars) and "-M5_" not in file and "-M6_" not in file ]
                i = i + 1
            
            # Copy files
            print(i)
            for filename in filenames:
                first_14_chars = filename[:14]
                matching_files = [file for file in os.listdir(source_folder) if file.startswith(first_14_chars) and "-M5_" not in file and "-M6_" not in file ]
                j = j + 1 
                print(j)
                progress_bar.UpdateBar(j, i)

                for matching_file in matching_files:
                    source_path = os.path.join(source_folder, matching_file)

                    matching_file_number = (matching_file.rsplit("_",1)[0]) + ".aof"
                    matching_file_number = (matching_file_number.split("_"))[6]


                    if j == i:
                        matching_file_New = matching_file.replace("_" + str(matching_file_number) + "_" , "_Comp-" + str(j) + "_")
                    else:
                        matching_file_New = matching_file.replace("_" + str(matching_file_number) + "_" , "_Inprog-" + str(j) + "_")

                    if Cycle != "":
                        matching_file_New = matching_file_New.replace("_" + str((matching_file_New.split("_"))[5]) + "_" , "_" + Cycle + "_")

                    matching_file_New = matching_file_New.replace(".aof", "")
                    matching_file_New = (matching_file_New.split("_"))
                    matching_file_New = "_".join(matching_file_New[:9])
                    matching_file_New = str(matching_file_New) + ".aof"
                    # matching_file_New = (matching_file_New.rsplit("_",1)[0]) + ".aof"
                    matching_file_New = matching_file_New.replace("Pre", "Post")
                    destination_path = os.path.join(destination_folder, matching_file_New)

                    # Check if the source file exists before copying
                    if os.path.exists(source_path):
                        shutil.copy(source_path, destination_path)
                        print(f"Copied {matching_file} :::::::::::::: {matching_file_New}")
                    else:
                        print(f"{matching_file} not found in {source_folder}")

            print(str(i*5) + "File copying process completed.")
            progress_bar.UpdateBar(0, i)

            

except ValueError as v:
    sg.popup(
        f'An error occured.Few of the possilble reasons: Your file might not have the columns in the right format. ', v, title="Error!")
    exit()
except Exception as e:
    tb = traceback.format_exc()
    sg.popup(f'An error occured.  Here is the info:', e, title="Error!")
    exit()