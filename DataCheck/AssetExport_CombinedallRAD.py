import pandas as pd
from tkinter import filedialog
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


main_excel_path = filedialog.askopenfilename()

# Function to save the modified Excel file
def save_file():
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = asksaveasfilename(title="Save modified Excel file", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    return file_path

print("Asked to Save file: ")

output_file = save_file()
if not output_file:
    raise ValueError("No output file selected!")


Path = output_file[:-5]

output_file_rooftop = Path + "_Rooftop.xlsx"

print("File will Save: " + output_file_rooftop)
print("File will Save: " + output_file)

df = pd.read_excel(main_excel_path)




df = df.astype(str)

# # Sample DataFrame
# data = {'Category': ['A', 'B', 'A', 'B', 'C'],
#         'Values': ['value1', 'value2', 'value3', 'value4', 'value5']}
# df = pd.DataFrame(data)

# Combine multiple row values for each category
combined_values = df.groupby('Prequal ID')['CLs for RF (Ft)'].agg(lambda x: ', '.join(x)).reset_index()

# Get unique values from the 'Category' column
unique_categories = df['Prequal ID'].unique()

# Print the results
# print("Original DataFrame:")
# print(df)
# print("\nCombined Values:")

merged_df = pd.merge(df[['Prequal ID', 'Lat', 'Long', 'Structure Type']], combined_values, on='Prequal ID', how='right')



Unique_df = merged_df.drop_duplicates()

Rooftop_df = Unique_df[Unique_df['Structure Type'] == 'Rooftop']
NotRooftop_df = Unique_df[Unique_df['Structure Type'] != 'Rooftop']

# directory_path = os.path.dirname(main_excel_path)

# pivot_table = pd.DataFrame(sheet1)

# Create a new Excel file using XlsxWriter
# excel_output_path = directory_path + '/Asset_Export_Unique_5.xlsx'

Rooftop_df.to_excel(output_file_rooftop, index=False)
NotRooftop_df.to_excel(output_file, index=False)
print("Save file: " + output_file_rooftop)
print("Save file: " + output_file)