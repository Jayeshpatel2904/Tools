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

sg.theme('DarkAmber')
layout = [
       
        [sg.Button('START', size=(300, 300))]
     ]


# window = sg.Window('My new window', layout,
#                    size=(500, 100), grab_anywhere=True)


# layout = [sg.Button('START','center',size=(100,1))]
window = sg.Window('AOF PARSER', layout, size=(500, 100))

try:

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break

        elif event == "START":
            root = Tk()
            root.withdraw()
            folder_selected = filedialog.askdirectory()

            directory = folder_selected
            print(folder_selected)

            filenew = open(directory + "\\DriveRoute.kml", "w")


            filenew.write("<?xml version='1.0' encoding='UTF-8'?>")
            filenew.write("\n")
            filenew.write("<kml xmlns='http://www.opengis.net/kml/2.2' xmlns:gx='http://www.google.com/kml/ext/2.2' xmlns:kml='http://www.opengis.net/kml/2.2' xmlns:atom='http://www.w3.org/2005/Atom'>")
            filenew.write("\n")
            filenew.write("<Document><name>DriveTest</name>")
            filenew.write("\n")
            filenew.write("<Style id='inline'><LineStyle><color>ff00ffff</color><width>4</width></LineStyle></Style>")
            filenew.write("\n")
            filenew.write("<Style id='inline1'><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>")
            filenew.write("\n")
            filenew.write("<StyleMap id='inline0'><Pair><key>normal</key><styleUrl>#inline1</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#inline</styleUrl></Pair></StyleMap>")
            filenew.write("\n")

            with open(directory + '\\Miles.csv', 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(["Log filename", "Log Miles", "miles"])


            with open(directory + '\\CALLSTAT.csv', 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(["Log filename", "CALL Result", "Cause"])

            j = 1
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                # checking if it is a file
                
                if os.path.isfile(f):
                    if ".aof" in f:
                        print(f)
                        filenew.write("<Placemark><name>" + filename + "</name>")
                        filenew.write("<styleUrl>#inline0</styleUrl><LineString><tessellate>1</tessellate><coordinates>")
                        
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
                                        filenew.write("\n")
                                        filenew.write(str(x[2]) + "," + str(x[3]) + "," + "0")
                                        GPS2 = (float(x[3]),float(x[2]))
                                        # print(str(GPS1) + "," + str(GPS2))
                                        mile2 = geopy.distance.geodesic(GPS1, GPS2).miles
                                        GPS1 = GPS2
                                        mile = mile + mile2
                                        logmile = logmile + mile2
                                        

                                        
                                if x[0]=="CALLSTAT":
                                    if "MtoM Org" in line:
                                        with open(directory + '\\CALLSTAT.csv','a') as callstatfile:
                                            callstatfile.write(filename + "," +  x[7] + "," +  x[6])
                                            callstatfile.write("\n") 
                                        
                                            
                            filenew.write("\n")              
                            filenew.write("</coordinates></LineString></Placemark>")              
                            j = j + 1
                            with open(directory + '\\Miles.csv','a') as file:
                                file.write(filename + "," +  str(logmile) + "," +  str(mile))
                                file.write("\n")
            print(mile)
            filenew.write("</Document></kml>")
            sg.popup('AOF File Parsed and Created MILE, CALLSTAT and KML Files in Folder')                


except ValueError as v:
    sg.popup(
        f'An error occured.Few of the possilble reasons: Your file might not have the columns in the right format. ', v, title="Error!")
    exit()
except Exception as e:
    tb = traceback.format_exc()
    sg.popup(f'An error occured.  Here is the info:', e, title="Error!")
    exit()