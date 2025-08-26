import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from tkinter import filedialog
import os
import tkinter as tk
import datetime
import matplotlib.pyplot as plt

time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Load data from the first Excel file (Sheet1)
excel_file1 = filedialog.askopenfilename()
sheet1 = pd.read_excel(excel_file1)

directory_path = os.path.dirname(excel_file1)

# if sheet1['timestamp'].str.len() == 10:
sheet1['timestamp'] = sheet1['timestamp'].astype(str).str[4:5] + '/' + sheet1['timestamp'].astype(str).str[:2] + '/' + sheet1['timestamp'].astype(str).str[6:]

# else:
#     sheet1['timestamp'] = sheet1['timestamp'].astype(str).str[4:5] + '/' + sheet1['timestamp'].astype(str).str[:2] + '/' + sheet1['timestamp'].astype(str).str[6:] + " " + sheet1['timestamp'].astype(str).str[13]

# sheet1['timestamp'] = sheet1['timestamp'].str.replace('.', '/', regex=False)
# sheet1['timestamp'] = pd.to_datetime(sheet1['timestamp'], format='%d/%m%Y').dt.strftime('%m%d%Y')



sheet1.rename(columns={'label.NRCGI': 'Custom: NR_Cell_Global_Id'}, inplace=True)

print("Sheet1 DataFrame:")


# Load data from the second Excel file (specific tab and column)
excel_file2 = filedialog.askopenfilename()
sheet2_tab = 'Sectors'  # Change to the name of the tab in file2.xlsx
column_to_join_from_sheet2 = 'Custom: NR_Cell_Global_Id'  # Change to the column name in sheet2.xlsx



# Read only the specified column from the second Excel file
sheet2_column = pd.read_excel(excel_file2, sheet_name=sheet2_tab)

columns_to_keep = ['Custom: NR_Cell_Global_Id', 'Custom: NR_Cell_Name']

# Merge the data

# merged_data = sheet1.merge(sheet2_column, left_on='Custom: NR_Cell_Global_Id', right_index=True)

result = pd.merge(sheet1, sheet2_column[columns_to_keep], on='Custom: NR_Cell_Global_Id', how='inner')

# Display or manipulate the merged_data as needed

df = pd.DataFrame(result)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create a plot with secondary y-axis
fig, ax1 = plt.subplots()

# Plot the first set of data using the primary y-axis
df.plot(x='timestamp', y='RRC_ConnEstabAtt_Sum', ax=ax1, color='blue', label='RRC_ConnEstabAtt_Sum')
ax1.set_xlabel('timestamp')
ax1.set_ylabel('RRC_ConnEstabAtt_Sum', color='blue')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of data using the secondary y-axis
df.plot(x='timestamp', y='rlc_vol_dl', ax=ax2, color='orange', label='rlc_vol_dl')
ax2.set_ylabel('rlc_vol_dl', color='orange')

# Combine the legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

# Show the plot
plt.show()

# # Save the merged data to a new Excel file
# merged_output = directory_path + '\merged_output_' + time + '.xlsx'
# result.to_excel(merged_output, index=False)