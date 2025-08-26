# For issues contact Niyati Joshi. Email:niyati.joshi@dish.com
import pandas as pd
import PySimpleGUI as sg
import traceback
import pandas as pd
import numpy as np
import datetime
import geopy.distance

time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

layout = [[sg.T("")], [sg.Text("Choose excel sheet with planet export: "), sg.Input(), sg.FileBrowse(key="-IN-")], [sg.T("")],
          [sg.T("")], [sg.Text("Choose input template sheet: "),
                       sg.Input(), sg.FileBrowse(key="-IN2-")], [sg.T("")],
          [sg.Text("Choose a destination folder: "), sg.Input(),
           sg.FolderBrowse(key="-OUT-")], [sg.T("")],
          [sg.Button("Submit")], [sg.T("")],
          [sg.Text('PROGRESS')],
          [sg.ProgressBar(1, orientation='h',
                          size=(100, 20), key='progress')]
          ]
window = sg.Window('Integiry Check', layout, size=(800, 400))
progress_bar = window.FindElement('progress')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Submit":
        path = values["-IN-"]
        dest_path = values["-OUT-"]
        dest = dest_path + "/validation_output-{}.xlsx".format(time)
        if dest_path == '':
            raise Exception("You did not select the destination folder. ")

        progress_bar.UpdateBar(1, 5)
        progress_bar.UpdateBar(2, 5)
        progress_bar.UpdateBar(3, 5)


        def BinaryToDecimal(bSum):
            decimal = 0
            for digit in bSum:
                decimal = decimal*2 + int(digit)
            return decimal

        def get_NR_Cell_Id(raw):
            if raw['Custom: gNodeB_Id'].find("FALSE") == -1 and raw['Custom: Local_Cell_Id'].find("FALSE") == -1:
                a = int(raw['Custom: gNodeB_Id'])
                a2 = bin(a)
                a3 = str(a2)[2:]
                a4 = 24-len(a3)
                a5 = "0"*a4 + a3
                b = int(raw['Custom: Local_Cell_Id'])
                b2 = bin(b)
                b3 = str(b2)[2:]
                b4 = 12-len(b3)
                b5 = "0"*b4 + b3
                c = a5 + b5
                return(str(int(BinaryToDecimal(c))))

   

        Siteinfo = pd.read_excel(path, sheet_name="Sites", keep_default_na=False, dtype=object)
        sitelist = Siteinfo[["Site ID", "Latitude", 'Longitude']]

        # coords_1 = (33.2296756, -77.0122287)
        # coords_2 = (33.406374, -78.9251681)

        sitelist.insert(3, "Latlong Calculation", geopy.distance.geodesic(33.2296756,-77.0122287, 33.406374, -78.9251681).miles)

        print(sitelist)



    


        # for sites in sitelist:

        #     sitelist.insert(0, "Calculation", sitelist["Band Name"] + "_" + final["Custom: NR_ARFCN_DL"].astype(str) + "_" +
        #                 final["Custom: NR_ARFCN_UL"].astype(str) + "_" + final["Custom: SSB_ARFCN"].astype(str) + "_" + final["Custom: absoluteFreqPointA"].astype(str) + "_" + final["Custom: Carrier_Bandwidth_UL_MHz"].astype(str) + "_" + final["Custom: MIMO"].astype(str) + "_" + final["PA Power (dBm)"].astype(str))
    

        
        # final = final.astype(str)
        
       
        # final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'] = np.where(final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'].str.lower().isin(
        #     final, final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'], "FALSE - The value does not match with the reference template  "+final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'])
        
       
        progress_bar.UpdateBar(5, 5)

        window.close()

tb = traceback.format_exc()

exit()
