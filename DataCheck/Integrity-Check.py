# For issues contact Niyati Joshi. Email:niyati.joshi@dish.com
import pandas as pd
import PySimpleGUI as sg
import traceback
import pandas as pd
import numpy as np
import datetime

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

try:

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Submit":
            path = values["-IN-"]
            template_path = values["-IN2-"]
            dest_path = values["-OUT-"]
            dest = dest_path + "/validation_output-{}.xlsx".format(time)
            if dest_path == '':
                raise Exception("You did not select the destination folder. ")
            template = pd.read_excel(template_path)
            CU_BEDC_template = pd.read_excel(
                template_path, sheet_name="Sheet2")
            progress_bar.UpdateBar(1, 5)
            gnb_tac_template = pd.read_excel(
                template_path, sheet_name="Sheet3")
            progress_bar.UpdateBar(2, 5)
            template = template.astype(str)
            CU_BEDC_template = CU_BEDC_template.astype(str)
            gnb_tac_template = gnb_tac_template.astype(str)
            test = template.values.tolist()
            test2 = CU_BEDC_template.values.tolist()
            test3 = gnb_tac_template.values.tolist()
            gnb_start = int(test3[0][1])
            gnb_end = int(test3[0][2])
            tac_start = int(test3[1][1])
            tac_end = int(test3[1][2])
            k8_start = int(test3[2][1])
            k8_end = int(test3[2][2])
            gnb_list = list(range(gnb_start, gnb_end+1))
            tac_list = list(range(tac_start, tac_end+1))
            k8_list = list(range(k8_start, k8_end+1))
            band_list = []
            CU_BEDC_list = []
            gnb_tac = []
            lat_pat = "^\d{2}\.\d{6}$"
            long_pat = "^-\d{2}\.\d{6}$"
            col_pat = "^FALSE"
            pci_list = list(range(2, 918))
            prach_list = list(range(0, 827))
            l = map(lambda x: str(x), pci_list)
            li = map(lambda x: str(x), prach_list)
            l3 = map(lambda x: str(x), gnb_list)
            l4 = map(lambda x: str(x), tac_list)
            l5 = map(lambda x: str(x), k8_list)

            gnb_list = list(l3)
            pci_list = list(l)
            prach_list = list(li)
            tac_list = list(l4)
            k8_list = list(l5)
            for i in test:
                band_list.append("_".join((i)))
            for j in test2:
                CU_BEDC_list.append("_".join(j))
            print(band_list)
            progress_bar.UpdateBar(3, 5)

            def highlight_cells(val):
                if val.startswith("FALSE"):

                    return 'background-color: #F67280'

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

            def get_NR_Cell_Global_Id(raw):
                if raw['Custom: NR_Cell_Id'].find("FALSE") == -1:
                    a = raw['Custom: NR_Cell_Id']
                    b = int(a)
                    e = (hex(int(b)))
                    f = "0"+str(e)[2:]
                    c = "133304" + f
                    d = int(c, 16)
                    return(str((d)))

            def pci_check(vals, final):
                conflict_list = []
                valdict = dict()
                valdict2 = dict()

                for v in vals:
                    if v[0] not in valdict.keys():
                        valdict[v[0]] = v[2]
                        valdict2[v[0]] = v[1], v[2]
                    else:

                        if valdict[v[0]] == v[2]:
                            continue
                        else:
                            x, y = valdict2[v[0]]
                            conflict_list.append([v[0], x, y])
                            conflict_list.append([v[0], v[1], v[2]])
                if conflict_list != []:
                    progress_bar.UpdateBar(4, 5)
                    invalid_pci = pd.DataFrame(conflict_list, columns=[
                        'Site_Id_Sector', 'Band', 'PCI'])
                    invalid_pci.drop_duplicates(inplace=True)

                    with pd.ExcelWriter(dest) as results:
                        invalid_pci.to_excel(
                            results, sheet_name="PCI_DISCREPANCY", index=False)
                        final.style.applymap(highlight_cells).to_excel(
                            results, sheet_name="Sheet1", index=False)
                        return False
                else:
                    progress_bar.UpdateBar(4, 5)
                    with pd.ExcelWriter(dest) as results:
                        final.style.applymap(highlight_cells).to_excel(
                            results, sheet_name="Sheet1", index=False)
                        return True

            def get_NR_Cell_Name(raw):
                f = raw['Site ID'] + "_" + raw['Antenna ID']
                if "DL" in raw['Band Name']:
                    b = raw['Band Name'][:-3]
                    b = b.replace("AWS-4", "AWS4")
                else:
                    b = raw['Band Name']
                    b = b.replace("AWS-4", "AWS4")
                return(str((f+"_"+b)))

            def get_gNodeB_Name(raw):
                return (raw['Site ID'][0:5]+raw['Custom: gNodeB_Id'])

            def get_local_cell_id(raw):
                assignment_id = 50
                N = (raw['Custom: gNodeB_Site_Number'])

                if N == "" or "FALSE" in N:
                    return
                N = int(raw['Custom: gNodeB_Site_Number'])

                if raw['Band Name'].startswith("n26") and raw['Antenna ID'] == "1":
                    assignment_id = 0

                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n26") and raw['Antenna ID'] == "2":
                    assignment_id = 1
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n26") and raw['Antenna ID'] == "3":
                    assignment_id = 2
                    return str(int((N-1)*21 + assignment_id))
                if (raw['Band Name'].startswith("n29") and raw['Antenna ID'] == "1"):
                    assignment_id = 3
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n29") and raw['Antenna ID'] == "2":
                    assignment_id = 4
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n29") and raw['Antenna ID'] == "3":
                    assignment_id = 5
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n71") and raw['Antenna ID'] == "1":
                    assignment_id = 6
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n71") and raw['Antenna ID'] == "2":
                    assignment_id = 7
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n71") and raw['Antenna ID'] == "3":
                    assignment_id = 8
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n66_AWS") and raw['Antenna ID'] == "1":
                    assignment_id = 9
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n66_AWS") and raw['Antenna ID'] == "2":
                    assignment_id = 10
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n66_AWS") and raw['Antenna ID'] == "3":
                    assignment_id = 11

                    return str(int((N-1)*21 + assignment_id))

                if raw['Band Name'].startswith("n70") and raw['Antenna ID'] == "1":
                    assignment_id = 12
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n70") and raw['Antenna ID'] == "2":
                    assignment_id = 13
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n70") and raw['Antenna ID'] == "3":
                    assignment_id = 14
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n66") and raw['Band Name'].find("AWS") == -1 and raw['Antenna ID'] == "1":
                    assignment_id = 15
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n66") and raw['Band Name'].find("AWS") == -1 and raw['Antenna ID'] == "2":
                    assignment_id = 16
                    return str(int((N-1)*21 + assignment_id))
                if raw['Band Name'].startswith("n66") and raw['Band Name'].find("AWS") == -1 and raw['Antenna ID'] == "3":
                    assignment_id = 17
                    return str(int((N-1)*21 + assignment_id))

            sheet_sectors = pd.read_excel(
                path, sheet_name="Sectors", keep_default_na=False, dtype=object)
            sheet_sectors_n = sheet_sectors[["Site ID", "Sector ID", 'Custom: CP_Type', 'Custom: DL_Rank', 'Custom: UL_Rank', 'Custom: NR_ARFCN_DL', 'Custom: arfcnSUL', 'Custom: arfcnSDL', 'Custom: NR_ARFCN_UL', 'Band Name', 'Custom: Carrier_Bandwidth_UL_MHz', 'Custom: Local_Cell_Id',
                                            'Custom: MIMO', 'Custom: NR_Cell_Id', 'Custom: NR_Cell_Name', 'Custom: NR_Cell_Global_Id', 'Custom: nSDL_Bandwidth', 'Custom: Paging_Cycle', 'Sector ID', 'Custom: SSB_ARFCN', 'Custom: Sub_Carrier_Spacing_kHz', 'Custom: absoluteFreqPointA', 'Custom: qRxLevMin']]

            sheet_nr_sectors = pd.read_excel(
                path, sheet_name="NR_Sectors", keep_default_na=False, dtype=object)
            sheet_nr_sectors_n = sheet_nr_sectors[["Site ID", "Sector ID", 'Number Of Selected Downlink Ports',
                                                   'Number Of Selected Uplink Ports', 'PA Power (dBm)', 'Physical Cell ID', 'First Zadoff Chu Sequence']]
            sheet_antenna = pd.read_excel(
                path, sheet_name="Antennas", keep_default_na=False, dtype=object)

            sheet_antenna_n = sheet_antenna[['Site ID', 'Antenna ID', 'Longitude', 'Latitude', 'Antenna File', 'Height (ft)', 'Azimuth', 'Mechanical Tilt'
                                             ]]
            sheet_nr_basestation = pd.read_excel(
                path, sheet_name="NR_Base_Stations", keep_default_na=False, dtype=object)
            sheet_nr_basestation_n = sheet_nr_basestation[[
                'Site ID', 'MCC', 'MNC']]
            sheet_sites = pd.read_excel(
                path, sheet_name="Sites", keep_default_na=False, dtype=object)
            sheet_sites_n = sheet_sites[["Site ID", "Custom: gNodeB_Site_Number", "Custom: Site_Type", "Custom: TAC", 'Custom: BEDC_CU_Number', 'Custom: K8_ID_CUs', 'Custom: K8_ID_DUs',

                                        "Custom: RAN_SW_Vendor", "Custom: gNodeB_Name", "Custom: gNodeB_Id", "Custom: gNodeB_Length"]]
            sheet_sectors_n.insert(


                0, "Combination", sheet_sectors["Site ID"] + "_" + sheet_sectors["Sector ID"])
            sheet_nr_sectors_n.insert(
                0, "Combination", sheet_nr_sectors["Site ID"] + "_" + sheet_nr_sectors["Sector ID"])
            sheet_antenna_n.insert(
                0, "Combination", sheet_antenna_n["Site ID"] + "_" + (sheet_antenna_n["Antenna ID"]).astype(str))

            sector_nr_sector_join = pd.merge(sheet_sectors_n,
                                             sheet_nr_sectors_n,
                                             on='Combination',
                                             how='outer')

            sector_nr_sector_join["Combination"] = sector_nr_sector_join['Combination'].str[:12] + \
                sector_nr_sector_join['Combination'].str[-1]

            antenna_sector_nr_sector_join = pd.merge(sector_nr_sector_join,
                                                     sheet_antenna_n,
                                                     on='Combination',
                                                     how='outer')
            antenna_sector_nr_sector_join = antenna_sector_nr_sector_join.drop(
                columns=["Site ID_x", "Sector ID_x", "Site ID_y", "Sector ID_y"])
            sites_antenna_sector_nr_sector_join = pd.merge(antenna_sector_nr_sector_join,
                                                           sheet_sites_n,
                                                           on='Site ID',
                                                           how='outer')
            sites_antenna_sector_nr_sector_join_nr_base_station = pd.merge(
                sites_antenna_sector_nr_sector_join, sheet_nr_basestation_n, on='Site ID', how='outer')
            final = sites_antenna_sector_nr_sector_join_nr_base_station
            final.insert(0, "Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO", final["Band Name"] + "_" + final["Custom: NR_ARFCN_DL"].astype(str) + "_" +
                         final["Custom: NR_ARFCN_UL"].astype(str) + "_" + final["Custom: SSB_ARFCN"].astype(str) + "_" + final["Custom: absoluteFreqPointA"].astype(str) + "_" + final["Custom: Carrier_Bandwidth_UL_MHz"].astype(str) + "_" + final["Custom: MIMO"].astype(str) + "_" + final["PA Power (dBm)"].astype(str))
            final.insert(0, "Site_ID_CUs_Numbers", final["Site ID"] + "_" + final["Custom: K8_ID_CUs"].astype(
                str) + "_" + final["Custom: BEDC_CU_Number"].astype(str))
            final.drop(columns="Combination", inplace=True)

            final = final[['Site_ID_CUs_Numbers', 'Site ID', 'Custom: K8_ID_CUs', 'Custom: BEDC_CU_Number', 'Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO', 'Band Name', 'Custom: NR_ARFCN_DL', 'Custom: NR_ARFCN_UL', 'Custom: SSB_ARFCN', 'Custom: absoluteFreqPointA', 'Custom: Carrier_Bandwidth_UL_MHz', 'Custom: MIMO', 'PA Power (dBm)', 'Custom: CP_Type', 'Custom: DL_Rank', 'Custom: UL_Rank', 'Custom: arfcnSUL', 'Custom: arfcnSDL',  'Custom: Local_Cell_Id', 'Custom: NR_Cell_Id', 'Custom: NR_Cell_Name', 'Custom: NR_Cell_Global_Id',
                           'Custom: nSDL_Bandwidth', 'Custom: Paging_Cycle', 'Custom: Sub_Carrier_Spacing_kHz', 'Custom: qRxLevMin', 'Number Of Selected Downlink Ports', 'Number Of Selected Uplink Ports', 'Physical Cell ID', 'First Zadoff Chu Sequence', 'Antenna ID', 'Longitude', 'Latitude', 'Antenna File', 'Height (ft)', 'Azimuth', 'Mechanical Tilt', 'Custom: gNodeB_Site_Number', 'Custom: Site_Type', 'Custom: TAC', 'Custom: K8_ID_DUs', 'Custom: RAN_SW_Vendor', 'Custom: gNodeB_Name', 'Custom: gNodeB_Id', 'Custom: gNodeB_Length', 'MCC', 'MNC']]
            final = final.fillna('')
            final = final.astype(str)

            final['Custom: CP_Type'] = np.where(
                final['Custom: CP_Type'] != "Normal", "FALSE - The value should be 'Normal'", final['Custom: CP_Type'])
            final['Site_ID_CUs_Numbers'] = np.where(final['Site_ID_CUs_Numbers'].isin(
                CU_BEDC_list), final['Site_ID_CUs_Numbers'], "FALSE - The value does not match with the reference template")
            final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'] = np.where(final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'].astype(str).isin(
                band_list), final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'], "FALSE - The value does not match with the reference template  "+final['Band_DL_UL_SSB_absfreqA_bandwidth_UL_MIMO'])
            final['Custom: DL_Rank'] = np.where(
                final['Custom: DL_Rank'] == "2", final['Custom: DL_Rank'], "FALSE - The value should be '2'")
            final['Custom: UL_Rank'] = np.where(
                final['Custom: UL_Rank'] == "1", final['Custom: UL_Rank'], "FALSE - The value should be '1'")

            final[['Custom: arfcnSDL', 'Custom: arfcnSDL', 'Custom: nSDL_Bandwidth', 'Mechanical Tilt']] = np.where(
                final[['Custom: arfcnSDL', 'Custom: arfcnSDL', 'Custom: nSDL_Bandwidth', 'Mechanical Tilt']] == "0", final[['Custom: arfcnSDL', 'Custom: arfcnSDL', 'Custom: nSDL_Bandwidth', 'Mechanical Tilt']], "FALSE - The value should be '0'")

            final[['Antenna File', 'Height (ft)', 'Azimuth', 'Custom: gNodeB_Site_Number']] = np.where(final[['Antenna File',
                                                                                                              'Height (ft)', 'Azimuth', 'Custom: gNodeB_Site_Number']] != "", final[['Antenna File', 'Height (ft)', 'Azimuth', 'Custom: gNodeB_Site_Number']], "FALSE - Empty value not allowed")
            final['Physical Cell ID'] = np.where(
                final['Physical Cell ID'].isin(pci_list), final['Physical Cell ID'], 'FALSE - PCI value is empty of out of range. Current value is: ' + final['Physical Cell ID'])
            final['Latitude'] = np.where(final['Latitude'].str.match(
                lat_pat), final['Latitude'], "FALSE - Latitude value should be float with 6 decimal digits. The current value is:" + final['Latitude'])

            final['Longitude'] = np.where(final['Longitude'].str.match(
                long_pat), final['Longitude'], "FALSE - Longitude value should be float with 6 decimal digits. The current value is:" + final['Longitude'])

            final['Custom: Paging_Cycle'] = np.where(
                final['Custom: Paging_Cycle'] == "rf64", final['Custom: Paging_Cycle'], "FALSE - The value should be 'rf64'")

            final['Custom: Sub_Carrier_Spacing_kHz'] = np.where(
                final['Custom: Sub_Carrier_Spacing_kHz'] == "15", final['Custom: Sub_Carrier_Spacing_kHz'], "FALSE - The value should be '15'")
            final['Custom: qRxLevMin'] = np.where(
                final['Custom: qRxLevMin'] == "-62", final['Custom: qRxLevMin'], "FALSE - The value should be '-62'")
            final[['Number Of Selected Downlink Ports', 'Number Of Selected Uplink Ports']] = np.where(final[['Number Of Selected Downlink Ports', 'Number Of Selected Uplink Ports']] == '4', final[[

                'Number Of Selected Downlink Ports', 'Number Of Selected Uplink Ports']], "FALSE - The value should be '4'")
            final['First Zadoff Chu Sequence'] = np.where(final['First Zadoff Chu Sequence'].isin(
                prach_list), final['First Zadoff Chu Sequence'], "FALSE - PRACH shoild be non-empty value in the range[0-827]. The current value: " + final['First Zadoff Chu Sequence'])

            final["Antenna ID"] = np.where(final['Antenna ID'].isin(
                ["1", "2", "3"]), final['Antenna ID'], "FALSE - Anetnna ID should be 1,2 or 3")
            final['Custom: Site_Type'] = np.where(
                final['Custom: Site_Type'] == "Macro", final['Custom: Site_Type'], "FALSE - The value should be 'MACRO'")
            final['Custom: TAC'] = np.where(final['Custom: TAC'].isin(
                tac_list), final['Custom: TAC'], "FALSE - The TAC value is not in the range provided in the reference template. The current value: " + final['Custom: TAC'])
            final['Custom: K8_ID_DUs'] = np.where(final['Custom: K8_ID_DUs'].isin(
                k8_list), final['Custom: K8_ID_DUs'], "FALSE - The K8 value is not in the range provided in the reference template. The current value: " + final['Custom: K8_ID_DUs'])
            final['Custom: gNodeB_Id'] = np.where(final['Custom: gNodeB_Id'].isin(
                gnb_list), final['Custom: gNodeB_Id'], "FALSE - The gNB_ID value is not in the range provided in the reference template. The current value: " + final['Custom: gNodeB_Id'])
            final['Custom: RAN_SW_Vendor'] = np.where(final['Custom: RAN_SW_Vendor'].isin(
                ["Samsung", "Mavenir"]), final['Custom: RAN_SW_Vendor'], "FALSE - The value should be 'Samsung' or 'Mavenir'")
            final['Custom: gNodeB_Length'] = np.where(
                final['Custom: gNodeB_Length'] == "24", final['Custom: gNodeB_Length'], "False - The value should be '24")
            final['MCC'] = np.where(final["MCC"] == "313", final['MCC'],
                                    "FALSE - The value should be '313'")
            final['MNC'] = np.where(final['MNC'] == "340", final['MNC'],
                                    "FALSE - The value should be '340'")

            final["Calculated_Custom: Local_Cell_Id"] = final.apply(
                get_local_cell_id, axis=1)

            final["Calculated_Custom: Local_Cell_Id"] = final["Calculated_Custom: Local_Cell_Id"].astype(
                str)

            final["Custom: Local_Cell_Id"] = np.where(final["Custom: Local_Cell_Id"] == final["Calculated_Custom: Local_Cell_Id"],
                                                      final["Custom: Local_Cell_Id"], "FALSE - The value does not match with the calculated value. The current value: " + final['Custom: Local_Cell_Id']+" the calculated value: " + final['Calculated_Custom: Local_Cell_Id'])
            final['Calculated_Custom: gNodeB_Name'] = final.apply(
                get_gNodeB_Name, axis=1)

            final["Custom: gNodeB_Name"] = np.where(final["Calculated_Custom: gNodeB_Name"] == final["Custom: gNodeB_Name"],
                                                    final["Custom: gNodeB_Name"], "FALSE - The value does not match with the calculated value. The current value: " + final['Custom: gNodeB_Name'] + " the calculated value: " + final['Calculated_Custom: gNodeB_Name'])
            final["Calculated_Custom: NR_Cell_Id"] = final.apply(
                get_NR_Cell_Id, axis=1)
            final['Calculated_Custom: NR_Cell_Id'] = final['Calculated_Custom: NR_Cell_Id'].astype(
                str)

            final["Custom: NR_Cell_Id"] = np.where(final["Custom: NR_Cell_Id"] == final["Calculated_Custom: NR_Cell_Id"],
                                                   final["Custom: NR_Cell_Id"], "FALSE - The value does not match with the calculated value. The current value is: " + final['Custom: NR_Cell_Id'] + " the calculated value: " + final['Calculated_Custom: NR_Cell_Id'])

            final["Calculated_Custom: NR_Cell_Global_Id"] = final.apply(
                get_NR_Cell_Global_Id, axis=1)
            final["Calculated_Custom: NR_Cell_Global_Id"] = final["Calculated_Custom: NR_Cell_Global_Id"].astype(
                str)
            final["Custom: NR_Cell_Global_Id"] = np.where(final['Custom: NR_Cell_Global_Id'] == final["Calculated_Custom: NR_Cell_Global_Id"],
                                                          final["Custom: NR_Cell_Global_Id"], "FALSE - The value does not match with the calculated value. The current value: " + final['Custom: NR_Cell_Global_Id'] + " the calculted value: " + final['Calculated_Custom: NR_Cell_Global_Id'])

            final['Calculated_Custom: NR_Cell_Name'] = final.apply(
                get_NR_Cell_Name, axis=1)
            final["Custom: NR_Cell_Name"] = np.where(final["Custom: NR_Cell_Name"] == final["Calculated_Custom: NR_Cell_Name"],
                                                     final["Custom: NR_Cell_Name"], "FALSE - The value does not match with the calculated value. The current value: " + final['Custom: NR_Cell_Name'] + " the calculated value: " + final['Calculated_Custom: NR_Cell_Name'])
            final['Validation_Result'] = final.apply(lambda x: "Passed" if str(
                x.values).find("FALSE") == -1 else "Failed", axis=1)
            f_column = final.pop('Validation_Result')
            final.insert(0, 'Validation_Result', f_column)
            final['Invalid_Columns'] = final.apply(
                lambda row: row[row.str.match(col_pat)].index.values.tolist(), axis=1)
            final['Invalid_Columns'] = final['Invalid_Columns'].astype(str).replace(
                "[]", "NA")
            I_column = final.pop('Invalid_Columns')
            final.insert(1, 'Invalid_Columns', I_column)

            fc = len(final[final.Validation_Result == "Failed"])

            pci_frame = final[['Site ID', 'Band Name',
                               'Antenna ID', 'Physical Cell ID']]
            pci_frame.insert(0, "SITE_SECTOR",
                             pci_frame['Site ID']+"_"+pci_frame['Antenna ID'])
            pci_frame = pci_frame[['SITE_SECTOR',
                                   'Band Name', 'Physical Cell ID']]
            pci_frame.drop_duplicates(inplace=True)

            vals = pci_frame.values.tolist()
            pc = pci_check(vals, final)

            if pc == False:
                msg = "PCI discrepancies found!"
            else:
                msg = "No PCI discrepancies found!"
            progress_bar.UpdateBar(5, 5)
            sg.popup(
                f'File has been created!.Please check your destination folder:\n{dest_path}\n\n{msg}\n\nThe number of rows with failed validation: {fc}', title="Success!")
            window.close()
except ValueError as v:
    sg.popup(
        f'An error occured.Few of the possilble reasons: Your file might not have the columns in the right format. ', v, title="Error!")
    exit()
except Exception as e:
    tb = traceback.format_exc()
    sg.popup(f'An error occured.  Here is the info:', e, title="Error!")
    exit()
