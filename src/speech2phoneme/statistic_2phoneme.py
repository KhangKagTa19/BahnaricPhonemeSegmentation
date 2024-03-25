import os
import shutil
import zipfile
import parselmouth
import numpy as np
import librosa
import soundfile as sf
import pandas as pd
from tqdm.auto import tqdm
from unidecode import unidecode
from praatio.utilities import textgrid_io

def parse_textgrid(file_path):
    try:
        labels = []
        # Open TextGrid file using Parselmouth
        textgrid_data = parselmouth.Data.read(file_path)
        textgrid_data.save_as_text_file("textgrid.txt")
        text = open("textgrid.txt", "r", encoding="utf-16").read()
    
        textgrid_data = textgrid_io.parseTextgridStr(
            text,
            includeEmptyIntervals=False,
        )
        
        entries = []
        for tier in textgrid_data["tiers"]:
            for entry in tier["entries"]:
                entries.append(entry)
        # Get the first 'start' value
        first_start = float(entries[0].start)

        # Get the last 'end' value
        last_end = float(entries[-1].end)
        phoneme_length = last_end - first_start
        if len(entries) > 0:
            for i in range(0, len(entries)):
                labels.append(
                    {
                        "start": entries[i].start,
                        "end": entries[i].end,
                        "phoneme": entries[i].label,
                        "length": float(entries[i].end) - float(entries[i].start),
                        "percent_length": (float(entries[i].end) - float(entries[i].start))/ phoneme_length,
                    }
                )
        
        return labels
    except Exception as e:
        labels = []
        textgrid_data = parselmouth.Data.read(file_path)
        textgrid_data.save_as_text_file("textgrid.txt")
        text = open("textgrid.txt", "r", encoding="ISO-8859-1").read()
        text = unidecode(text, "utf-8")
        text = text.replace("\x00", "")

        textgrid_data = textgrid_io.parseTextgridStr(
            text,
            includeEmptyIntervals=False,
        )
        
        entries = []
        for tier in textgrid_data["tiers"]:
            for entry in tier["entries"]:
                entries.append(entry)
        # Get the first 'start' value
        first_start = float(entries[0].start)

        # Get the last 'end' value
        last_end = float(entries[-1].end)
        phoneme_length = last_end - first_start
        if len(entries) > 0:
            for i in range(0, len(entries)):
                labels.append(
                    {
                        "start": entries[i].start,
                        "end": entries[i].end,
                        "phoneme": entries[i].label,
                        "length": float(entries[i].end) - float(entries[i].start),
                        "percent_length": (float(entries[i].end) - float(entries[i].start))/ phoneme_length,
                    }
                )
     
        return labels

def process_textgrid_and_audio(textgrid_file):
        labels = parse_textgrid(textgrid_file)
        
        if labels:
          
            phoneme_string = ''.join(item['phoneme'] for item in labels)
           
            
            df_dict = {
                "file_name": textgrid_file,
                "start": labels[0]['start'],
                "phoneme_1_length": labels[0]['length'],
                "phoneme_2_length": labels[1]['length'],
                
                "%_length_phoneme_1": labels[0]['percent_length'],
                "%_length_phoneme_2": labels[1]['percent_length'],
                
                "phoneme_1": labels[0]['phoneme'],
                "phoneme_2": labels[1]['phoneme'],
               
                "full_phoneme": phoneme_string
            }

            return df_dict

        else:
            return None


# Load filenames from three_phoneme.csv

# Load the CSV file into a DataFrame
df = pd.read_csv("preprocess.csv")

# Filter the DataFrame where number_phoneme equals 2
filtered_df = df[df['number_phoneme'] == 2]

# Get the filenames where number_phoneme equals 2
filenames = filtered_df['file_name'].tolist()
# Initialize lists to store data
data = []

# Iterate over filenames
for filename in filenames:
    
    result = process_textgrid_and_audio(filename)
    if result:
        data.append(result)

# Convert data list to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("2_phoneme_features.csv", index=False)

print("phoneme features saved to 2_phoneme_features.csv.")


import csv
from collections import Counter


# Initialize a dictionary for the hierarchical tree
hierarchy_tree = {}

# Read the CSV-like data
with open('3_phoneme_features.csv',mode="r", encoding="utf-8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        phoneme_1 = row['phoneme_1']
        phoneme_2 = row['phoneme_2']
       
        
        # Add phoneme 1 to the hierarchy tree if not already present
        if phoneme_1 not in hierarchy_tree:
            hierarchy_tree[phoneme_1] = {}
        
        # Add phoneme 2 to the hierarchy tree if not already present
        if phoneme_2 not in hierarchy_tree[phoneme_1]:
            hierarchy_tree[phoneme_1][phoneme_2] = []
        
       
# Function to recursively print the hierarchy tree as a dictionary
def print_hierarchy_dict(tree, indent=0):
    result = ''
    for key, value in sorted(tree.items(), key=lambda item: len(item[1]), reverse=True):
        result += ' ' * indent + str(key) + ': '
        if isinstance(value, dict):
            result += '{\n' + print_hierarchy_dict(value, indent + 2) + ' ' * indent + '}\n'
        else:
            result += str(value) + '\n'
    return result

# Print the hierarchical tree as a dictionary
print(print_hierarchy_dict(hierarchy_tree))