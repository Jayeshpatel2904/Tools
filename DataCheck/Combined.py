import pandas as pd
from tkinter import filedialog
import os


main_excel_path = filedialog.askopenfilename()

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

directory_path = os.path.dirname(main_excel_path)

# pivot_table = pd.DataFrame(sheet1)


# Create a new Excel file using XlsxWriter
excel_output_path = directory_path + '/Asset_Export_Unique_5.xlsx'
excel_output_path1 = directory_path + '/Asset_Export_Unique_6.xlsx'
merged_df.to_excel(excel_output_path, index=False)
Unique_df.to_excel(excel_output_path1, index=False)