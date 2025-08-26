import pandas as pd
import openpyxl
import requests
from tkinter import filedialog
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os

# Your Bing Maps API Key
api_key = 'Aj17tYf3PnRmnNvtbSO9QzwZ3BX_bfnSX5bt3r58dYovFzeiLdyltq0stFHqAh1M'

# Define the Excel file path
excel_file_path = 'locations.xlsx'  # Replace with your Excel file path
excel_file_path = filedialog.askopenfilename()

directory_path = os.path.dirname(excel_file_path)

# Load the Excel file into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name='Locations')


df = df[df['Region'] == "Central"]

print(df)

# Function to perform reverse geocoding
def reverse_geocode(lat, lon):
    url = f'https://dev.virtualearth.net/REST/v1/Locations/{lat},{lon}?o=json&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'resourceSets' in data and len(data['resourceSets']) > 0:
            resources = data['resourceSets'][0]['resources']
            if len(resources) > 0:
                return resources[0]['address']['formattedAddress']
    return None

# Apply reverse geocoding to each row in the DataFrame
df['Bing Address'] = df.apply(lambda row: reverse_geocode(row['Latitude'], row['Longitude']), axis=1)

print(df)


workbook = Workbook()
sheet = workbook.active  # By default, this will create a new sheet named 'Sheet'

# Optionally, you can rename the sheet
sheet.title = 'NewSheet'

# Write the pandas DataFrame to the sheet
for row in dataframe_to_rows(df, index=False, header=True):
    sheet.append(row)

# Save the workbook to a new Excel file
excel_file_path = directory_path + '/PEA_Reverse_Geocode.xlsx'  # Specify the path and filename
workbook.save(excel_file_path)



# # Save the updated DataFrame back to the Excel file
# with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
#     writer.book = openpyxl.load_workbook(excel_file_path)
#     df.to_excel(writer, sheet_name='Locations', index=False)

print("Reverse geocoding completed and addresses added to the Excel file.")