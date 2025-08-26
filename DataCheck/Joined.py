import pandas as pd
import numpy as np

# Example DataFrame
data = {'column_name': [np.nan, np.nan, 3.0, 4.0]}
df = pd.DataFrame(data)

# Check if the column is empty or contains only NaN values
column_values = df['column_name']
if isinstance(column_values, pd.Series) and column_values.isnull().all():
    print("Column is empty or contains only NaN values")
elif isinstance(column_values, pd.Series) and not column_values.isnull().any():
    print("Column is not empty and does not contain any NaN values")
else:
    print("Column is not empty and contains NaN values along with other values")
