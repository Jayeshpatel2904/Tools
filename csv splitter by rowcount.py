import pandas as pd
import os

def split_csv_by_rows(input_csv_path, output_folder, rows_per_file=5000):
    """
    Splits a large CSV file into smaller CSV files, each containing a specified number of rows.

    Args:
        input_csv_path (str): The path to the input CSV file.
        output_folder (str): The path to the folder where the split CSV files will be saved.
        rows_per_file (int): The number of rows for each split file (default is 5000).
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Get the base name of the input CSV file (without extension)
    base_filename = os.path.splitext(os.path.basename(input_csv_path))[0]

    try:
        # Read the CSV file in chunks
        # The 'chunksize' parameter returns an iterator, allowing processing without loading the entire file into memory
        chunk_iterator = pd.read_csv(input_csv_path, chunksize=rows_per_file)

        file_count = 0
        for i, chunk in enumerate(chunk_iterator):
            file_count += 1
            # Construct the output file name
            output_filename = f"{base_filename}_part_{file_count}.csv"
            output_filepath = os.path.join(output_folder, output_filename)

            # Save the current chunk to a new CSV file
            # index=False prevents pandas from writing the DataFrame index as a column in the CSV
            chunk.to_csv(output_filepath, index=False)
            print(f"Saved {output_filepath} with {len(chunk)} rows.")

        if file_count == 0:
            print(f"No data found in {input_csv_path} or file is empty.")
        else:
            print(f"\nSuccessfully split '{input_csv_path}' into {file_count} files in '{output_folder}'.")

    except FileNotFoundError:
        print(f"Error: Input CSV file not found at '{input_csv_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # Define the path to your input CSV file
    # IMPORTANT: Replace 'your_input_file.csv' with the actual path to your CSV file
    input_csv = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/2024-05-30 1_10pm (2).csv'

    # Define the folder where you want to save the split files
    # IMPORTANT: Replace 'output_csv_files' with your desired output folder name
    output_directory = 'C:/ProgramData\MySQL/MySQL Server 8.0/Uploads/Multiple'

    # Call the function to split the CSV
    split_csv_by_rows(input_csv, output_directory, rows_per_file=50000)

    # Example with a different chunk size (e.g., 10000 rows per file)
    # split_csv_by_rows(input_csv, 'output_10k_rows', rows_per_file=10000)