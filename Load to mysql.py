import mysql.connector
import os
import glob

# --- Configuration ---
# Update these settings with your MySQL connection details
db_config = {
    'user': 'your_user',
    'password': 'your_password',
    'host': '127.0.0.1', # Use 'localhost' or your server's IP
    'database': 'data_analytics_bss' # The database name to use
}

# The folder where your CSV files are located
# This MUST be the same folder as your MySQL server's 'secure_file_priv' path
folder_path = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Multiple/'

# The name of the table you are importing data into
table_name = 'raw_voice_cdr_drop_calls_agg'

def import_csv_files():
    """
    Connects to MySQL, finds all CSV files in a folder, and imports them.
    """
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        print("Successfully connected to MySQL database.")

        # Find all .csv files in the specified folder
        # The glob.glob() function returns a list of files that match the pattern
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

        if not csv_files:
            print(f"No CSV files found in the specified folder: {folder_path}")
            return

        for file_path in csv_files:
            # Get the file name for display purposes
            file_name = os.path.basename(file_path)

            # Construct the LOAD DATA INFILE query
            # We use f-strings to safely embed the variables into the query string
            load_query = f"""
                LOAD DATA INFILE '{file_path.replace(os.sep, '/')}'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY ','
                ENCLOSED BY '"'
                LINES TERMINATED BY '\\n'
                IGNORE 1 ROWS;
            """
            
            # Print the query we're about to execute
            print(f"\nImporting '{file_name}'...")
            
            try:
                # Execute the query
                cursor.execute(load_query)
                conn.commit()
                print(f"Successfully imported '{file_name}'. {cursor.rowcount} rows added.")
            except mysql.connector.Error as err:
                print(f"Error importing '{file_name}': {err}")
                conn.rollback() # Rollback the transaction on error

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
    finally:
        # Close the cursor and connection to free up resources
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nMySQL connection is closed.")

if __name__ == '__main__':
    # Run the import process
    import_csv_files()
