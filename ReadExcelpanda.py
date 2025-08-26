import pandas

datafile = r"C:\Users\jayeshkumar.patel\Documents\Personal\Insurance\Question Answer_Final_03122023.xlsx"

excel_data_df = pandas.read_excel(datafile, sheet_name='Sheet1')

# print whole sheet data
print(excel_data_df)