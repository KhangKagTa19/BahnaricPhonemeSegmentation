import glob
import multiprocessing
import multiprocessing as mp
import os
import shutil
import zipfile

import gdown
import librosa
import numpy as np
import pandas as pd
import parselmouth
from praatio.utilities import textgrid_io
from tqdm.auto import tqdm
from unidecode import unidecode
import soundfile as sf
from acoustic_features import extract_feature_means

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists("bahnaric"):
    # shutil.rmtree("bahnaric")
    if os.path.exists("Am vi Ba Na"):
        shutil.rmtree("Am vi Ba Na")
    # Unzip the ZIP file
    with zipfile.ZipFile("Am vi Ba Na-20240202T004404Z-001.zip", "r") as zip_file:
        zip_file.extractall()
    shutil.move("Am vi Ba Na", "bahnaric/dataset/raw")
else: 
    pass

print(" check 1 ")
# --------------------------------------------------------------------------- #
# Parse TextGrid
# Read the TextGrid file, keep the interval that text != ""
# and get the label from that interval, also try to store a set of possible phonemes in labels
data = []

sr=16000
def process_textgrid_and_audio(textgrid_file):
    """
    Extracts text from a TextGrid file and cuts a corresponding audio segment from a WAV file.
    Args:
        textgrid_file (str): Path to the TextGrid file.
        wav_file (str): Path to the WAV file.
    Returns:
        None (prints results to console).
    """

    try:
        labels = []
        count = 0
        # Open TextGrid file using Parselmouth
        textgrid_data = parselmouth.Data.read(textgrid_file)
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
        

        if len(entries) > 0:
            for i in range(0, len(entries)):
                labels.append(
                    {
                        "file_name": textgrid_file,
                        "start": entries[i].start,
                        "end": entries[i].end,
                        "phoneme": entries[i].label,
                        
                        
                    }
                )
       
        # Get the first 'start' value
        first_start = float(labels[0]['start'])

        # Get the last 'end' value
        last_end = float(labels[-1]['end'])

        # Concatenate 'phoneme' into a single string
        phoneme_string = ''.join(item['phoneme'] for item in labels)
        for item in labels:
            count +=1
        # Load the audio file
        audio_file = labels[0]['file_name'].replace('.TextGrid', '.wav')
       
        # Load the audio
        y, sr = librosa.load(audio_file, sr=16000)

        # Calculate sample indices for t1 and t2
        start_idx = int(first_start * sr)
        end_idx = int(last_end * sr)

        # Extract the desired segment
        desired_segment = y[start_idx:end_idx]

        # Calculate padding lengths based on desired padding duration
        padding_length = int(1 * sr // 2)

        # Create padding arrays
        padding_before = np.zeros(padding_length)
        padding_after = np.zeros(padding_length)

        # Combine the desired segment, padding, and check for overflow
        padded_segment = np.concatenate((padding_before, desired_segment, padding_after))
        if padded_segment.shape[0] > y.shape[0]:
            padded_segment = padded_segment[:y.shape[0]]  # Truncate if overflow occurs

        
        sf.write(
            labels[0]['file_name'].replace('.TextGrid', '_cut.wav'), padded_segment, sr
            )
        data.append(
            {
                "file_name": textgrid_file,
                "start": first_start,
                "end": last_end,
                "phoneme": phoneme_string,
                "number_phoneme": count,
            }
        )

    except Exception as e:
        labels = []
        count = 0
        textgrid_data = parselmouth.Data.read(textgrid_file)
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
        

        if len(entries) > 0:
            for i in range(0, len(entries)):
                labels.append(
                    {
                        "file_name":textgrid_file,
                        "start": entries[i].start,
                        "end": entries[i].end,
                        "phoneme": entries[i].label,
                        
                    }
                )
       
        # Get the first 'start' value
        first_start = float(labels[0]['start'])

        # Get the last 'end' value
        last_end = float(labels[-1]['end'])

        # Concatenate 'phoneme' into a single string
        phoneme_string = ''.join(item['phoneme'] for item in labels)
        for item in labels:
            count +=1
        # Load the audio file
        audio_file = labels[0]['file_name'].replace('.TextGrid', '.wav')
       
        # Load the audio
        y, sr = librosa.load(audio_file, sr=16000)

        # Calculate sample indices for t1 and t2
        start_idx = int(first_start * sr)
        end_idx = int(last_end * sr)

        # Extract the desired segment
        desired_segment = y[start_idx:end_idx]

        # Calculate padding lengths based on desired padding duration
        padding_length = int(1 * sr // 2)

        # Create padding arrays
        padding_before = np.zeros(padding_length)
        padding_after = np.zeros(padding_length)

        # Combine the desired segment, padding, and check for overflow
        padded_segment = np.concatenate((padding_before, desired_segment, padding_after))
        if padded_segment.shape[0] > y.shape[0]:
            padded_segment = padded_segment[:y.shape[0]]  # Truncate if overflow occurs

        
        sf.write(
            
            labels[0]['file_name'].replace('.TextGrid', '_cut.wav'), padded_segment, sr
            )
        data.append(
            {
                "file_name": textgrid_file,
                "start": first_start,
                "end": last_end,
                "phoneme": phoneme_string,
                "number_phoneme": count,
            }
        )

print(" check 2 ") 



if not os.path.exists("bahnaric/features"):
    # Create the folder
    os.makedirs("bahnaric/features")
folder_path = "bahnaric/dataset/raw"
file_extension = ".TextGrid"

# Traverse the directory
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # Check if the file ends with ".TextGrid"
        if file.endswith(file_extension):
            # If so, print the absolute path of the file
            file_path = os.path.join(root, file)
            process_textgrid_and_audio(file_path)

data = pd.DataFrame(data)
data.to_csv("preprocess.csv", index=False, encoding="utf-8")
print("here!!!")





import pandas as pd

# Read the CSV file
df = pd.read_csv("preprocess.csv")

# Define the minimum and maximum values based on the data (assuming consecutive integers)
min_value = min(df['number_phoneme'])
max_value = max(df['number_phoneme'])

# Create a dictionary to store counts for each value
value_counts = {}
for value in range(min_value, max_value + 1):
    value_counts[value] = (df['number_phoneme'] == value).sum()

# Print the value counts
print("Statistic of number_phoneme values: \n")
print(value_counts)

# Read the data from the CSV file
data = pd.read_csv("preprocess.csv")

# Filter rows where number_phoneme is equal to 3
filtered_data = data[data["number_phoneme"] == 3]

# Create a sub table with the filtered data
sub_table = filtered_data[["file_name", "start", "end", "phoneme", "number_phoneme"]]

# Save the sub table to a new CSV file
sub_table.to_csv("three_phoneme.csv", index=False)

# Print confirmation message
print("Sub table with three phonemes saved to three_phoneme.csv")

import csv
# Function to print phoneme and number of phonemes
def print_phoneme_info(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            phoneme = row['phoneme']
            num_phoneme = row['number_phoneme']
            print(f"{phoneme} : {num_phoneme}")

# Call the function with the file name
print_phoneme_info('preprocess.csv')