import pandas as pd

# List of paths to the CSV files
file_paths = [
    '2_phoneme_features.csv',
    '3_phoneme_features.csv',
    '4_phoneme_features.csv',
    '5_phoneme_features.csv',
    '6_phoneme_features.csv'
]

# Initialize an empty list to store dataframes
dfs = []

# Iterate through each CSV file
for file_path in file_paths:
    # Read the CSV file into a dataframe
    df = pd.read_csv(file_path, encoding= 'utf-8')
    # Append the dataframe to the list
    dfs.append(df)

# Merge all dataframes into one, filling missing columns with null values
merged_df = pd.concat(dfs, ignore_index=True, sort=False)

# Write the merged dataframe to a new CSV file
merged_df.to_csv('database.csv', index=False, encoding = 'utf-8')