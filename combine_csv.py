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
    # Find all directories in the current path
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    # Filter out hidden directories
    dirs = [d for d in dirs if not d.startswith('.')]

    if not dirs:
        print("No directories found in the current path.")
        exit()

    print("Please choose a directory to process:")
    for i, dirname in enumerate(dirs):
        print(f"{i + 1}: {dirname}")

    choice = -1
    while choice < 1 or choice > len(dirs):
        try:
            choice = int(input(f"Enter a number (1-{len(dirs)}): "))
        except ValueError:
            print("Invalid input. Please enter a number.")

    source_dir = dirs[choice - 1]

    # Proceed with combining CSVs from the selected directory
    output_filename = "combined_trips.csv"
    print(f"Processing directory: {source_dir}")
    print("Starting CSV combination process...")
    combine_csvs(source_dir, output_filename)