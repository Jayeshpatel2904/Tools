import pandas as pd
import xlsxwriter
from tkinter import filedialog

folder_selected = filedialog.askdirectory()

# Generate pivot_table (replace this with your actual pivot table)
data = {
    'Year': [2021, 2022, 2023],
    'Value1_A': [100, 150, 120],
    'Value1_B': [200, 180, 130],
    'Value2_A': [500, 550, 600],
    'Value2_B': [600, 580, 650]
}

pivot_table = pd.DataFrame(data)

# Create a new Excel file using XlsxWriter
excel_output_path = folder_selected + '/chart_with_secondary_axis.xlsx'
writer = pd.ExcelWriter(excel_output_path, engine='xlsxwriter')

# Write the pivot_table to the Excel file
pivot_table.to_excel(writer, sheet_name='Sheet1', index=False)

# Access the XlsxWriter workbook and worksheet objects
workbook = writer.book
worksheet = writer.sheets['Sheet1']

# Create a chart object
chart = workbook.add_chart({'type': 'line'})

# Configure the first series (Value1_A)
chart.add_series({
    'name': ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, len(pivot_table), 0],
    'values': ['Sheet1', 1, 2, len(pivot_table), 2],
})

# Configure the second series (Value2_A) with a secondary axis
chart.add_series({
    'name': ['Sheet1', 0, 4],
    'categories': ['Sheet1', 1, 0, len(pivot_table), 0],
    'values': ['Sheet1', 1, 4, len(pivot_table), 4],
    'y2_axis': True,  # Create a secondary axis for this series
})

# Configure the chart axes and labels
chart.set_x_axis({'name': 'Year'})
chart.set_y_axis({'name': 'Value1 and Value2'})
chart.set_y2_axis({'name': 'Value2'})

# Insert the chart into the worksheet
worksheet.insert_chart('G2', chart)

# Close the Pandas Excel writer and output the Excel file
writer.save()