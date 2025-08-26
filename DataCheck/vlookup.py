import pandas as pd

# Sample DataFrames with different lengths
df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5],
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
})

df2 = pd.DataFrame({
    'ID': [1, 2, 3, 9, 10],
    'Age': [25, 30, 35, 45, 50]
})

# Perform the VLOOKUP equivalent using merge
result = df1.merge(df2, on='ID', how='left')

print(result)