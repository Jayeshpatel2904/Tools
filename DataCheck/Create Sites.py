import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Function to select Excel file using tkinter
def select_file(title):
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = askopenfilename(title=title, filetypes=[("Excel files", "*.xlsx")])
    return file_path

# Function to save the modified Excel file
def save_file():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = asksaveasfilename(title="Save modified Excel file", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    return file_path

# Select the reference Excel file
reference_file = select_file("Select the reference Excel file")
if not reference_file:
    raise ValueError("No reference file selected!")

# Load the reference Excel file
reference_df = pd.read_excel(reference_file)

# Create a dictionary mapping Site ID to New Site ID, Latitude, and Longitude
site_id_mapping = reference_df.set_index('Site ID').to_dict(orient='index')

# Select the multi-sheet Excel file
multi_sheet_file = select_file("Select the PlanetExport Excel file")
if not multi_sheet_file:
    raise ValueError("No PlanetExport file selected!")

# Load the multi-sheet Excel file
multi_sheet_excel = pd.read_excel(multi_sheet_file, sheet_name=None)

# Process each sheet in the multi-sheet Excel
for sheet_name, sheet_df in multi_sheet_excel.items():
    # Check if the "Site ID" column exists in the current sheet

    # if sheet_name == "Groups":
    #     if (sheet_df['Name'] != "PLAN_3YEAR").all() :
    #         sheet_df.loc[len(sheet_df.index)] = ['PLAN_3YEAR', 'Local']

    if 'Site ID' in sheet_df.columns:
        # Loop through the rows and update Site ID, Latitude, and Longitude
        for idx, row in sheet_df.iterrows():
            site_id = row['Site ID']
            if site_id in site_id_mapping:
                new_values = site_id_mapping[site_id]
                # Update the "Site ID" with the "New Site ID"
                sheet_df.at[idx, 'Site ID'] = new_values['New Site ID']
                # Update the Latitude and Longitude if those columns exist
                if 'Latitude' in sheet_df.columns and 'Longitude' in sheet_df.columns and 'Description' in sheet_df.columns and 'Site Name' in sheet_df.columns and 'Site Name 2' in sheet_df.columns:
                    sheet_df.at[idx, 'Latitude'] = new_values['New Latitude']
                    sheet_df.at[idx, 'Longitude'] = new_values['New Longitude']
                    sheet_df.at[idx, 'Description'] = new_values['New Description']
                    sheet_df.at[idx, 'Site Name'] = new_values['Site Name']
                    sheet_df.at[idx, 'Site Name 2'] = str(new_values['Site Name']) + "-" + str(new_values['RAD'])

                if 'Height (ft)' in sheet_df.columns:
                    sheet_df.at[idx, 'Height (ft)'] = new_values['RAD']

                if 'Latitude' in sheet_df.columns and 'Longitude' in sheet_df.columns:
                    sheet_df.at[idx, 'Latitude'] = new_values['New Latitude']
                    sheet_df.at[idx, 'Longitude'] = new_values['New Longitude']

                    

    if sheet_name == "Sites":
        sheet_df["Custom: gNodeB_Id"] = ""
        sheet_df["Custom: Cluster_ID"] = ""
        sheet_df["Custom: gNodeB_Name"] = ""
        sheet_df["Custom: gNodeB_Site_Number"] = ""
        sheet_df["Custom: MLA_Partner"] = ""   
        sheet_df["Custom: TAC"] = ""
        sheet_df["Custom: BEDC_CU_Number"] = ""
        sheet_df["Custom: K8_ID_CUs"] = "" 
        sheet_df["Site UID"] = "" 


    if sheet_name == "Sectors":
        sheet_df["Custom: Local_Cell_Id"] = ""
        sheet_df["Custom: NR_Cell_Global_Id"] = ""
        sheet_df["Custom: NR_Cell_Id"] = ""
        sheet_df["Custom: NR_Cell_Name"] = ""
        sheet_df["Group: PLAN_3YEAR"] = True  

    if sheet_name == "NR_Base_Stations":
        sheet_df["gNodeB ID"] = ""
          
    if sheet_name == "NR_Sector_Carriers":
        sheet_df["Cell Name"] = ""  
        sheet_df["NCI"] = ""  
        sheet_df["TAC"] = 0
        sheet_df["Cell ID"] = ""

    if sheet_name == "NR_Sectors":
        sheet_df["Physical Cell ID"] = ""  
        sheet_df["First Zadoff Chu Sequence"] = 0  


# Ask the user where to save the modified Excel file
output_file = save_file()
if not output_file:
    raise ValueError("No output file selected!")

# Save the modified Excel file
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, sheet_df in multi_sheet_excel.items():
        sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f'Modified Excel saved as {output_file}')
