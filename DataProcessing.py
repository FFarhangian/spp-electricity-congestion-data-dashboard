import os
import pandas as pd

def merge_csv_files():
    input_dir = input("Enter the path to the input directory: ")
    output_dir = input("Enter the path to the output directory: ")
    output_file = input("Enter the name of the output CSV file: ")

    os.makedirs(output_dir, exist_ok=True)
    all_files = [os.path.join(root, file) for root, _, files in os.walk(input_dir) if 'By_Day' in root for file in files if file.endswith(".csv")]

    if not all_files:
        print("No CSV files found to merge.")
        return

    final_df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)
    final_df.to_csv(os.path.join(output_dir, output_file), index=False)
    print(f"Merged data saved to {os.path.join(output_dir, output_file)}")

if __name__ == "__main__":
    merge_csv_files()
