import pandas as pd
import PySimpleGUI as sg
import traceback
import pandas as pd
import numpy as np
import datetime
import geopy.distance
import os
from tkinter import filedialog
from tkinter import *
import csv


time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# sg.theme('DarkAmber')


column_to_be_centered = [ [sg.Text("Choose a Source folder: ",font=('Helvetica', 12, 'bold')), sg.InputText(key='-NEWIN-',size=(100, None)),sg.FolderBrowse(key="-IN-",font=('Helvetica', 12, 'bold'))], [sg.T("")],
                        [sg.T("")],
                        [sg.Text("Phone type M1/M5: ",font=('Helvetica', 12, 'bold')), sg.InputText(key='-Type-',size=(118, None))],
                        [sg.T("")],
                        [sg.Text('PROGRESS',font=('Helvetica', 12, 'bold'))],
                        [sg.ProgressBar(1, orientation='h',size=(100, 20), key='progress')],
                        [sg.T("")],
                            [sg.Button('START',font=('Helvetica', 12, 'bold'))]]


# layout = [
#         [sg.ProgressBar(1, orientation='h',size=(100, 20), key='progress')],
#         [sg.Button('START')]
        
#      ]

layout = [[sg.VPush()],
              [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
              [sg.VPush()]]
# window = sg.Window('My new window', layout,
#                    size=(500, 100), grab_anywhere=True)


# layout = [sg.Button('START','center',size=(100,1))]
window = sg.Window('AOF PARSER', layout)
progress_bar = window.FindElement('progress')
try:

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        elif event == "START":
            root = Tk()
            root.withdraw()
            folder_selected = values["-NEWIN-"]
            MOType = "-" + values["-Type-"]
            window['-NEWIN-'].update('')
            window['-Type-'].update('')
            # folder_selected = filedialog.askdirectory()
            
            if MOType == "-":
                 MOType = "-M1"

            print(MOType)
                 
            directory = folder_selected

            if directory == "":
                sg.popup(f'Folder Not selected', title="Error!")
                
            filecount = 0
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                # checking if it is a file
                
                if os.path.isfile(f):
                    if ".aof" in f and "_Auto_C2-" in f and MOType in f:
                         filecount = filecount + 1
                         clustername = (f.split("_"))[7]

            if filecount != 0:
                filenew = open(directory + "\\DriveRoute_" + clustername + MOType + ".kml", "w")


                filenew.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                filenew.write("<kml xmlns='http://www.opengis.net/kml/2.2' xmlns:gx='http://www.google.com/kml/ext/2.2' xmlns:kml='http://www.opengis.net/kml/2.2' xmlns:atom='http://www.w3.org/2005/Atom'>\n")
                filenew.write("\t<Document><name>DriveTest" + clustername + MOType + "</name>\n")
                filenew.write("\t\t<Style id='inline'><LineStyle><color>ff00ffff</color><width>8</width></LineStyle></Style>\n")
                filenew.write("\t\t<Style id='inline1'><LineStyle><color>ffff0000</color><width>6</width></LineStyle></Style>\n")
                filenew.write("\t\t<StyleMap id='inline0'><Pair><key>normal</key><styleUrl>#inline1</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#inline</styleUrl></Pair></StyleMap>\n")
            

                with open(directory + '\\Miles_' + clustername + MOType + '.csv', 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Log filename", "Log Miles", "miles"])


                with open(directory + '\\CALLSTAT_' + clustername + MOType + '.csv', 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Log filename", "Success", "Setup Fail","Drop"])
                
                progress_bar.UpdateBar(0, filecount)
                j = 1
                Totaldrop = 0
                TotalSuccess = 0
                Totalsetupfail = 0

                for filename in os.listdir(directory):
                    f = os.path.join(directory, filename)
                    # checking if it is a file
                    Drop = 0
                    SetupFail = 0
                    Success = 0
                    if os.path.isfile(f):
                        if ".aof" in f and "_Auto_C2-" in f and MOType in f:
                            # print(f)
                            filenew.write("\t\t\t<Placemark><name>" + filename + "</name>\n")
                            filenew.write("\t\t\t<styleUrl>#inline0</styleUrl><LineString><tessellate>1</tessellate><coordinates>\n")
                            
                            with open(f,'r+') as file:
                                i = 1
                                
                                for line in file:
                                    x = line.split("|")
                                    if x[0]=="GPS":
                                        if i == 1 and j == 1 and "Time" not in line and "tim" not in line:
                                            x = line.split("|")
                                            GPS1 = (float(x[3]),float(x[2]))
                                            mile = 0
                                            logmile = 0
                                            i = 2
                                        if i == 1 and j != 1 and "Time" not in line and "tim" not in line:

                                            x = line.split("|")
                                            GPS1 = (float(x[3]),float(x[2]))
                                            i = 2
                                            logmile = 0

                                        elif i != 1:

                                            
                                            GPS2 = (float(x[3]),float(x[2]))
                                            # print(str(GPS1) + "," + str(GPS2))
                                            mile2 = geopy.distance.geodesic(GPS1, GPS2).miles
                                            GPS1 = GPS2

                                            if mile2 < 0.02:
                                                filenew.write("\t\t\t" + str(x[2]) + "," + str(x[3]) + "," + "0\n")
                                                mile = mile + mile2
                                                logmile = logmile + mile2
                                            
       
                                    if x[0]=="CALLSTAT":
                                        if "MtoM" in line:
                                            if x[7] == "Success":
                                                Success = Success + 1
                                           
                                            elif x[7] == "SetupFail":
                                                
                                                SetupFail = SetupFail + 1
                                               
                                            elif x[7] == "Drop":
                                                Drop = Drop + 1
                                                
                                filenew.write("</coordinates></LineString></Placemark>\n")
                                progress_bar.UpdateBar(j, filecount)             
                                j = j + 1
                                with open(directory + '\\Miles_' + clustername + MOType +  '.csv','a') as file:
                                    file.write(filename + "," +  str(logmile) + "," +  str(mile))
                                    file.write("\n")

                                
                                with open(directory + '\\CALLSTAT_' + clustername + MOType + '.csv','a') as callstatfile:
                                    callstatfile.write(filename + "," +  str(Success) + "," +  str(SetupFail) + "," + str(Drop))
                                    callstatfile.write("\n")

                                Totaldrop = Totaldrop + Drop
                                Totalsetupfail = Totalsetupfail + SetupFail
                                TotalSuccess = TotalSuccess + Success

                print(mile)

                
                VoNRAccessibility = (TotalSuccess + Totaldrop)*100/(TotalSuccess + Totaldrop + Totalsetupfail)
                VoNRRetainability = (TotalSuccess - Totaldrop)*100/(TotalSuccess)
                with open(directory + '\\CALLSTAT_' + clustername + MOType + '.csv','a') as callstatfile:
                    callstatfile.write("Total Count" + "," +  str(TotalSuccess) + "," +  str(Totalsetupfail) + "," + str(Totaldrop))
                    callstatfile.write("\n")
                    callstatfile.write("VoNR Accessibility [%]" + "," +  str(VoNRAccessibility))
                    callstatfile.write("\n")
                    callstatfile.write("VoNR Retainability [%]" + "," +  str(VoNRRetainability))
                    callstatfile.write("\n")
                

                filenew.write("</Document></kml>")
                filenew.close()
                sg.popup("AOF File Parsed\n TotalSuccess = " +  str(TotalSuccess) + "\n Totalsetupfail = " +  str(Totalsetupfail) + " \n Totaldrop = " + str(Totaldrop) + "\n VoNR Accessibility [%] = " +  str(VoNRAccessibility) + "\n VoNR Retainability [%] = " +  str(VoNRRetainability))             
                progress_bar.UpdateBar(0, filecount)

                
            else:
                 sg.popup('Files Counts 0 for Mobile' + MOType)
            
except ValueError as v:
    sg.popup(
        f'An error occured.Few of the possilble reasons: Your file might not have the columns in the right format. ', v, title="Error!")
    
except Exception as e:
    tb = traceback.format_exc()
    sg.popup(f'An error occured.  Here is the info:', e, title="Error!")



  