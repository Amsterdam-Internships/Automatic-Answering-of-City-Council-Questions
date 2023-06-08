import os 
import pandas as pd

def combine_csv_files(folder_path, output_file_path):
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Filter only CSV files
    csv_files = [file for file in file_list if file.endswith('.csv')]

    # Initialize an empty list to store the dataframes
    dfs = []

    # Read each CSV file and append its contents to the list of dataframes
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save the combined dataframe to a new CSV file
    combined_df.to_csv(output_file_path, index=False)
