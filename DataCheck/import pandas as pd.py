import openpyxl
import matplotlib.pyplot as plt
from tkinter import filedialog

# Load Excel file
excel_file_path = filedialog.askopenfilename()
workbook = openpyxl.load_workbook(excel_file_path)
sheet = workbook.active

# Assuming data is in columns A and B
data = []
for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming headers in first row
    data.append(row)

# Extract data from columns
x_labels = [row[0] for row in data]
y_values = [row[1] for row in data]

# Create a bar chart
plt.bar(x_labels, y_values)
plt.xlabel('X Axis Label')
plt.ylabel('Y Axis Label')
plt.title('Bar Chart Example')

# Display the chart
plt.show()