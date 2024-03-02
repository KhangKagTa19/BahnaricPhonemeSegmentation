import glob
import multiprocessing
import multiprocessing as mp
import os
import shutil
import zipfile
import textgrid 
import gdown
import librosa
import numpy as np
import pandas as pd
import parselmouth
from praatio.utilities import textgrid_io
from tqdm.auto import tqdm
from unidecode import unidecode
import soundfile as sf
os.chdir(os.path.dirname(os.path.abspath(__file__)))


data = []
sr=16000
def process_textgrid_and_audio(textgrid_file, wav_file):
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
        # Open TextGrid file using Parselmouth
        textgrid_data = parselmouth.Data.read(textgrid_file)
        print(textgrid_data)
        textgrid_data.save_as_text_file("textgrid.txt")
        text = open("textgrid.txt", "r", encoding="utf-16").read()
        print("Encode: ", text)
        

        textgrid_data = textgrid_io.parseTextgridStr(
            text,
            includeEmptyIntervals=False,
        )
        print(textgrid_data)
        entries = []
        for tier in textgrid_data["tiers"]:
            for entry in tier["entries"]:
                entries.append(entry)
        print("preprocessing..." )

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
        print(labels)
        # Get the first 'start' value
        first_start = float(labels[0]['start'])

        # Get the last 'end' value
        last_end = float(labels[-1]['end'])

        # Concatenate 'phoneme' into a single string
        phoneme_string = ''.join(item['phoneme'] for item in labels)

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


        sf.write(labels[0]['file_name'].replace('.TextGrid', '_cut.wav'), padded_segment, sr)
        data.append(
            {
                "file_name": textgrid_file,
                "start": first_start,
                "end": last_end,
                "phoneme": phoneme_string,
                "speech": labels[0]['file_name'].replace('.TextGrid', '_cut.wav'),
            }
        )

    except Exception as e:
        labels = []
        text = open("textgrid.txt", "r", encoding="ISO-8859-1").read()
        print("Encode: ", text)
        text = unidecode(text, "utf-8")
        text = text.replace("\x00", "")

        textgrid_data = textgrid_io.parseTextgridStr(
            text,
            includeEmptyIntervals=False,
        )
        print(textgrid_data)
        entries = []
        for tier in textgrid_data["tiers"]:
            for entry in tier["entries"]:
                entries.append(entry)
        print("preprocessing..." )

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
        print(labels)
        # Get the first 'start' value
        first_start = float(labels[0]['start'])

        # Get the last 'end' value
        last_end = float(labels[-1]['end'])

        # Concatenate 'phoneme' into a single string
        phoneme_string = ''.join(item['phoneme'] for item in labels)

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


        sf.write(labels[0]['file_name'].replace('.TextGrid', '_cut.wav'), padded_segment, sr)
        data.append(
            {
                "file_name": textgrid_file,
                "start": first_start,
                "end": last_end,
                "phoneme": phoneme_string,
                "speech": labels[0]['file_name'].replace('.TextGrid', '_cut.wav'),
            }
        )

# Replace with your actual file paths
textgrid_file = ["chup.TextGrid","bu.TextGrid","apach.TextGrid","Ba.TextGrid"]
for x in textgrid_file:
    process_textgrid_and_audio(x, x.replace('.TextGrid', '.wav'))

print(data)
data = pd.DataFrame(data)
data.to_csv("preprocess.csv", index=False, encoding="utf-8")


labels = pd.read_csv("preprocess.csv")
print(labels)