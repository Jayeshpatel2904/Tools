import pandas as pd

# Sample DataFrames
table1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [10, 20, 30]})
table2 = pd.DataFrame({'A': [2, 3, 1], 'B': [5, 6, 4], 'D': [40, 50, 60]})

# Merge DataFrames based on columns A and B
merged_table = pd.merge(table1[['A', 'B']], table2[['A', 'B', 'D']], on=['A', 'B'])

# Calculate column C based on some operation on columns A and B
merged_table['C'] = merged_table['A'] * merged_table['B']

# Print the merged DataFrame
print(merged_table)