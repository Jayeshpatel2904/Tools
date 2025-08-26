import os
import pandas as pd
from tkinter import filedialog
import datetime

time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# Directory containing the Excel files to be merged
input_directory = filedialog.askdirectory()
excel_file2 = filedialog.askopenfilename()

# Get a list of all .xlsx files in the input directory
xlsx_files = [file for file in os.listdir(input_directory) if file.endswith('.xlsx')]

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through each Excel file and merge its data into the merged_data DataFrame
for file in xlsx_files:
    file_path = os.path.join(input_directory, file)
    df = pd.read_excel(file_path)
    merged_data = pd.concat([merged_data, df], ignore_index=True)



sheet1 = merged_data

# if sheet1['timestamp'].str.len() == 10:
sheet1['timestamp'] = sheet1['timestamp'].astype(str).str[4:5] + '/' + sheet1['timestamp'].astype(str).str[:2] + '/' + sheet1['timestamp'].astype(str).str[6:]


sheet1.rename(columns={'label.NRCGI': 'Custom: NR_Cell_Global_Id'}, inplace=True)


# Load data from the second Excel file (specific tab and column)
# excel_file2 = filedialog.askopenfilename()
sheet2_tab = 'Sectors'  # Change to the name of the tab in file2.xlsx
column_to_join_from_sheet2 = 'Custom: NR_Cell_Global_Id'  # Change to the column name in sheet2.xlsx

columns_to_keep1 = ['Custom: NR_Cell_Global_Id', 'Custom: NR_Cell_Name','DUID']

# Read only the specified column from the second Excel file
sheet2_column = pd.read_excel(excel_file2, sheet_name=sheet2_tab, usecols=columns_to_keep1)

print(sheet2_column)

# columns_to_keep1 = ['Custom: NR_Cell_Global_Id', 'Custom: NR_Cell_Name']
columns_to_keep2 = ['timestamp', 'RRC_ConnEstabAtt_Sum','rlc_vol_dl']

# Merge the data

# merged_data = sheet1.merge(sheet2_column, left_on='Custom: NR_Cell_Global_Id', right_index=True)

result = pd.merge(sheet1, sheet2_column, on='Custom: NR_Cell_Global_Id', how='inner')

# Remove selected columns
columns_to_remove = ['Custom: NR_Cell_Global_Id', 'Voice Accessibility %']  # List of column names to remove
df = result.drop(columns=columns_to_remove)

pivot_table = pd.DataFrame(df)


unique_values = df['Custom: NR_Cell_Name'].unique()

# pivot_table = df.pivot_table(index='timestamp',values=['RRC_ConnEstabAtt_Sum', 'rlc_vol_dl'])

excel_output_path = input_directory + '/SleepyCell_Data_' + time + '.xlsx'
writer = pd.ExcelWriter(excel_output_path, engine='xlsxwriter')

# Write the pivot_table to the Excel file
pivot_table.to_excel(writer, sheet_name='Sheet1', index=False)

# Access the XlsxWriter workbook and worksheet objects
workbook = writer.book
worksheet = writer.sheets['Sheet1']

# # Create a chart object
# chart = workbook.add_chart({'type': 'line'})

# # Configure the first series (Value1_A)
# chart.add_series({
#     'name': ['Sheet1', 0, 2],
#     'categories': ['Sheet1', 1, 0, len(pivot_table), 0],
#     'values': ['Sheet1', 1, 2, len(pivot_table), 2],
# })

# # Configure the second series (Value2_A) with a secondary axis
# chart.add_series({
#     'name': ['Sheet1', 0, 5],
#     'categories': ['Sheet1', 1, 0, len(pivot_table), 0],
#     'values': ['Sheet1', 1, 5, len(pivot_table), 5],
#     'y2_axis': True,  # Create a secondary axis for this series
# })

# # Configure the chart axes and labels
# chart.set_x_axis({'name': 'Timestamp'})
# chart.set_y_axis({'name': 'RRC_ConnEstabAtt_Sum'})
# chart.set_y2_axis({'name': 'rlc_vol_dl'})

# # Insert the chart into the worksheet
# worksheet.insert_chart('G2', chart)

# Close the Pandas Excel writer and output the Excel file
writer.save()
