import os
import csv
import argparse
import datetime

def combine_csvs(directory, output_file):
    """
    Combines all CSV files in a directory into a single CSV file.

    Args:
        directory (str): The directory containing the CSV files.
        output_file (str): The name of the output CSV file.
    """
    # Get a list of all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    csv_files.sort()

    if not csv_files:
        print(f"No CSV files found in {directory}")
        return

    # Open the output file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)

        # Process the first file (with header)
        first_file = True
        for filename in csv_files:
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    if first_file:
                        # Write header and all rows for the first file
                        for row in reader:
                            writer.writerow(row)
                        first_file = False
                    else:
                        # Skip header and write remaining rows for subsequent files
                        next(reader, None)  # Skip header
                        for row in reader:
                            writer.writerow(row)
            except Exception as e:
                print(f"Could not read file {filename}. Reason: {e}")


    print(f"Successfully combined {len(csv_files)} CSV files into {output_file}")



if __name__ == "__main__":
    # Define source directory relative to the script location
    source_dir = "csv_files"

    # Check if the source directory exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory not found at '{source_dir}'. Please create it and place your CSV files inside.")
        exit()

    # Proceed with combining CSVs directly from the source directory
    output_filename = "combined_trips.csv"
    print("Starting CSV combination process...")
    combine_csvs(source_dir, output_filename)