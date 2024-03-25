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
                "phoneme_3_length": labels[2]['length'],
                "phoneme_4_length": labels[3]['length'],
                "phoneme_5_length": labels[4]['length'],
                "phoneme_6_length": labels[5]['length'],
                "%_length_phoneme_1": labels[0]['percent_length'],
                "%_length_phoneme_2": labels[1]['percent_length'],
                "%_length_phoneme_3": labels[2]['percent_length'],
                "%_length_phoneme_4": labels[3]['percent_length'],
                "%_length_phoneme_5": labels[4]['percent_length'],
                "%_length_phoneme_6": labels[5]['percent_length'],
                "phoneme_1": labels[0]['phoneme'],
                "phoneme_2": labels[1]['phoneme'],
                "phoneme_3": labels[2]['phoneme'],
                "phoneme_4": labels[3]['phoneme'],
                "phoneme_5": labels[4]['phoneme'],
                "phoneme_6": labels[5]['phoneme'],
                "full_phoneme": phoneme_string
            }

            return df_dict

        else:
            return None


# Load filenames from three_phoneme.csv

# Load the CSV file into a DataFrame
df = pd.read_csv("preprocess.csv")

# Filter the DataFrame where number_phoneme equals 5
filtered_df = df[df['number_phoneme'] == 6]

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
df.to_csv("6_phoneme_features.csv", index=False)

print("phoneme features saved to 6_phoneme_features.csv.")



