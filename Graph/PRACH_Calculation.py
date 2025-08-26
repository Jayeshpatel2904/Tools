import pandas as pd
import tkinter as tk
from tkinter import filedialog
from geopy.distance import geodesic

# Open file dialog to select Excel file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xlsx *.xls")])

if not file_path:
    print("No file selected. Exiting...")
    exit()

# Load the Excel sheets
df_sites = pd.read_excel(file_path, sheet_name="Sites")
df_nrs = pd.read_excel(file_path, sheet_name="NR_Sector_Carriers")


# Merge Latitude and Longitude from Sites into NR_Sector_Carriers
df_merged = df_nrs.merge(df_sites[['Site ID', 'Latitude', 'Longitude']], on='Site ID', how='left')


columns_to_keep = ["Site ID", "Sector ID", "Physical Cell ID", "First Zadoff Chu Sequence", "Latitude", "Longitude"]
df_merged = df_merged[columns_to_keep]

print(df_merged)

# Function to find the closest site with the same "First Zadoff Chu Sequence"
def find_closest_site(row, df_merged):
    same_zadoff = df_merged[df_merged['First Zadoff Chu Sequence'] == row['First Zadoff Chu Sequence']]
    if same_zadoff.empty:
        return None, None
    
    current_location = (row['Latitude'], row['Longitude'])
    min_distance = float('inf')
    closest_site_id = None
    
    for _, site in same_zadoff.iterrows():
        site_location = (site['Latitude'], site['Longitude'])
        distance = geodesic(current_location, site_location).km
        if distance > 0 and distance < min_distance:
            min_distance = distance
            closest_site_id = site['Site ID']
    
    return closest_site_id, min_distance

# Apply function to find closest site
df_merged[['Closest Site ID', 'Distance']] = df_merged.apply(lambda row: pd.Series(find_closest_site(row, df_merged)), axis=1)

# Save the updated data to a new Excel file
output_file = file_path.replace(".xlsx", "_updated.xlsx")
df_merged.to_excel(output_file, index=False)

print(f"Updated Excel file saved as: {output_file}")
