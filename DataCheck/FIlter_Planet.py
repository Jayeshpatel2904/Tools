import pandas as pd

# Assuming your DataFrame is called df and you want to store column 'A' in a new DataFrame
# Create a sample DataFrame
data = {'A': ['foo', 'bar', 'baz']}
df = pd.DataFrame(data)

# Store column 'A' in a new DataFrame with column name
new_df = pd.DataFrame(df['A'].copy())  # Copying to ensure independence
new_df.columns = ['New_Column_Name']  # Rename the column

print(new_df)