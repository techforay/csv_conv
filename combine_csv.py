import os
import csv
import argparse
import datetime
import pandas as pd

def combine_csvs(directory, output_file):
    """
    Combines all CSV files in a directory into a single CSV file,
    adding an 'Original_File' column to each row.

    Args:
        directory (str): The directory containing the CSV files.
        output_file (str): The name of the output CSV file.
    """
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    csv_files.sort()

    if not csv_files:
        print(f"No CSV files found in {directory}")
        return

    all_data = []
    fieldnames = None

    for filename in csv_files:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                
                if fieldnames is None:
                    fieldnames = reader.fieldnames + ['Original_File']
                
                for row in reader:
                    # Create a new dictionary to ensure all fieldnames are present
                    new_row = {k: row.get(k, '') for k in fieldnames if k != 'Original_File'}
                    new_row['Original_File'] = filename
                    all_data.append(new_row)
        except Exception as e:
            print(f"Could not read file {filename}. Reason: {e}")

    if not all_data:
        print(f"No data to write to {output_file}")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    print(f"Successfully combined {len(csv_files)} CSV files into {output_file}")



def summarize_by_purpose(output_file):
    """
    Reads a CSV file, groups by 'Purpose' and sums the 'Miles'.
    Also identifies and reports dates for blank 'Purpose' entries.

    Args:
        output_file (str): The path to the CSV file.
    """
    try:
        df = pd.read_csv(output_file)
        # Convert 'Miles' to numeric, coercing errors to NaN, then fill NaN with 0
        df['Miles'] = pd.to_numeric(df['Miles'], errors='coerce').fillna(0)
        
        if 'Purpose' in df.columns and 'Miles' in df.columns:
            # Identify rows with blank 'Purpose' before filling them
            blank_purpose_rows = df[df['Purpose'].isna() | (df['Purpose'] == '')]
            
            if not blank_purpose_rows.empty:
                print("\n--- Entries with Blank Purpose ---")
                if 'Date' in df.columns and 'Original_File' in df.columns:
                    for index, row in blank_purpose_rows.iterrows():
                        print(f"Date: {row['Date']}, Miles: {row['Miles']}, File: {row['Original_File']}")
                elif 'Original_File' in df.columns:
                    for index, row in blank_purpose_rows.iterrows():
                        print(f"Miles: {row['Miles']}, File: {row['Original_File']}")
                elif 'Date' in df.columns:
                    for index, row in blank_purpose_rows.iterrows():
                        print(f"Date: {row['Date']}, Miles: {row['Miles']}")
                else:
                    for index, row in blank_purpose_rows.iterrows():
                        print(f"Miles: {row['Miles']}")
                print("----------------------------------")

            # Fill blank 'Purpose' values with 'Unspecified'
            df['Purpose'] = df['Purpose'].fillna('Unspecified')
            
            # Group by 'Purpose' and sum the 'Miles'
            purpose_summary = df.groupby('Purpose')['Miles'].sum().reset_index()
            
            print("\nSummary of Miles by Purpose:")
            print(purpose_summary)
        else:
            print("\nCould not find 'Purpose' or 'Miles' columns in the combined CSV.")
            
    except FileNotFoundError:
        print(f"\nOutput file {output_file} not found. Cannot generate summary.")
    except Exception as e:
        print(f"\nAn error occurred while generating the summary: {e}")


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
    summarize_by_purpose(output_filename)