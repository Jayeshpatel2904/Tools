import pandas as pd
import requests
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Step 1: Open file dialog to select the Excel file
def open_file_dialog():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx")], title="Select Excel File with URLs")
    return file_path

# Step 2: Open save file dialog to select where to save the combined output
def save_file_dialog():
    root = Tk()
    root.withdraw()  # Hide the root window
    save_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save Combined Output As")
    return save_path

# Function to process the dataframe
def process_dataframe(df):
    if 'Owner Name' in df.columns:
        # Concatenate "Owner Name" column rows with " || "
        owner_name_combined = ' || '.join(df['Owner Name'].dropna().astype(str).unique())
        df['Owner Name'] = owner_name_combined  # Replace entire column with concatenated value
    
    if 'Mailing Address' in df.columns:
        # Concatenate "Mailing Address" values if they are different, otherwise keep just one
        mailing_address_unique = df['Mailing Address'].dropna().astype(str).unique()
        if len(mailing_address_unique) > 1:
            mailing_address_combined = ' || '.join(mailing_address_unique)
        else:
            mailing_address_combined = mailing_address_unique[0]  # Only one unique value, keep it
        
        df['Mailing Address'] = mailing_address_combined  # Replace entire column with the concatenated value or single address

    # if 'Value' in df.columns:

    #     df['Value'] = df['Value'][1]  # Only one unique value, keep it


    # if 'Sale Date' in df.columns:

    #     df['Sale Date'] = df['Sale Date'][0]  # Only one unique value, keep it
        
    # if 'Sale Price' in df.columns:

    #     df['Sale Price'] = df['Sale Price'][0]  # Only one unique value, keep it

    # Return the processed dataframe with just one row for "Owner Name" and "Mailing Address"
    return df.iloc[[0]]  # Only keep the first row of the DataFrame after processing


# Select the Excel file with multiple URLs
excel_path = open_file_dialog()

if not excel_path:
    print("No file selected.")
else:
    # Read the URLs from the Excel file
    df_urls = pd.read_excel(excel_path)

    # Assuming the URLs are in the first column
    urls = df_urls.iloc[:, 0]

    # Initialize an empty list to store the processed data from all URLs
    all_data = []

    for url in urls:
        print(url)
        try:
            # Fetch the table from the website
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract all tables from the webpage
            tables = pd.read_html(str(soup))


            # # Select specific tables: 1-3, 6, and 8 (indexing starts from 0)
            # selected_tables = [tables[i] for i in [0, 1, 2, 5, 7] if i < len(tables)]

            if tables:
                # Concatenate the first 3 tables side by side (along columns)
                tables_to_append = tables[:3]  # Take the first 3 tables
                #  # Step 3: Concatenate **all** tables side by side (along columns)
                # combined_table = pd.concat(tables, axis=1)  # Combine all tables side by side

                combined_table = pd.concat(tables_to_append, axis=1)  # Combine tables side by side

                # Process the combined table for "Owner Name" and "Mailing Address"
                processed_table = process_dataframe(combined_table)

                # Append the processed table to the list
                all_data.append(processed_table)

                print(all_data)
            else:
                print(f"No tables found on {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    # for url in urls:
    #     try:
    #         # Fetch the table from the website
    #         response = requests.get(url)
    #         soup = BeautifulSoup(response.content, 'lxml')

    #         # Extract all tables from the webpage
    #         tables = pd.read_html(str(soup))

    #         # Select specific tables: 1-3, 6, and 8 (indexing starts from 0)
    #         selected_tables = [tables[i] for i in [0, 1, 2, 5, 7] if i < len(tables)]

    #         if selected_tables:
    #             # Concatenate the selected tables side by side (along columns)
    #             combined_table = pd.concat(tables, axis=1)  # Combine tables side by side

    #             # Process the combined table for "Owner Name" and "Mailing Address"
    #             processed_table = process_dataframe(combined_table)

    #             print(processed_table)

    #             # Append the processed table to the list
    #             all_data.append(processed_table)
    #         else:
    #             print(f"No tables found on {url}")
    #     except Exception as e:
    #         print(f"Error processing {url}: {e}")

    # If data was collected, concatenate all processed tables into one DataFrame
    if all_data:
        final_combined_data = pd.concat(all_data, ignore_index=True)

        # Open the save file dialog to select where to save the final combined output
        output_excel_path = save_file_dialog()

        if output_excel_path:
            # Save the final combined table to the chosen Excel file
            final_combined_data.to_excel(output_excel_path, index=False)
            print(f"Final combined data successfully saved to {output_excel_path}")
        else:
            print("No save location selected.")
    else:
        print("No data was collected from the URLs.")
