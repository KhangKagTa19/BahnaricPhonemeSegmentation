import os
import csv
import librosa
import soundfile as sf

# Define the set of phoneme characters
phoneme_characters = {'t', 'Kl', 'n', 'ĭ', 'oh', 'âm', 'ih', 'uch', 'ô', 'tr', 'd', 'ŭq', 'r', 'ol', 'ơ', 'U', 'nh', 'a', 'o', 'uə', 'm', "'b", 'c', 's', 'i', 'đ', 'ɤm', 'ia', 'e', 'ng', 'ɉ', 'p', 'ă', 'ŭ', 'ê', 'ɛ', 'j', 'y', 'h', 'v', 'up', 'au', 'l', 'q', 'â', 'u', 'ĕr', 'ư', 'ɯə', 'ĭ', 'uô', 'ch', 'k', 'b', 'g', 'Gr'}

# Specify the directory where you want to create the folders
base_directory = "./phoneme_folders"

# Create folders for each phoneme character
for phoneme in phoneme_characters:
    # Handle case for 'u' and 'U'
    if phoneme == 'u':
        folder_name = os.path.join(base_directory, phoneme)
    elif phoneme == 'U':
        folder_name = os.path.join(base_directory, "upper_u")
    else:
        folder_name = os.path.join(base_directory, phoneme)
    
    os.makedirs(folder_name, exist_ok=True)
    print(f"Created folder: {folder_name}")

csv_file = "database.csv"

# Function to process each line
def process_line(row, row_idx):
    # Extract information from the row
    filename = row['file_name'].replace('\\\\', '\\')
    start = float(row['start'])

    phoneme_lengths = [float(row[f'phoneme_{i}_length']) if row[f'phoneme_{i}_length'] else 0.0 for i in range(1, 7)]
    phonemes = [row[f'phoneme_{i}'] for i in range(1, 7)]

    # Change .TextGrid to .wav in filename
    audio_filename = str(filename).replace('.TextGrid', '.wav')
    print(audio_filename)
    # Load the audio file
    audio, sr = librosa.load(audio_filename, sr=None)
    # Convert start and lengths to sample indices
    start_idx = int(start * sr)
    end_indices = [start_idx + int(length * sr) for length in phoneme_lengths]

    # Save each part to the corresponding subfolder
    for idx, (phoneme, length, end_idx) in enumerate(zip(phonemes, phoneme_lengths, end_indices), start=1):
        if phoneme == "":
            continue
        if phoneme == "U":
            subfolder_path = os.path.join(base_directory, "upper_u")
        else:
            subfolder_path = os.path.join(base_directory, phoneme)
        os.makedirs(subfolder_path, exist_ok=True)
        part = audio[start_idx:end_idx]
        sf.write(os.path.join(subfolder_path, f"{row_idx}_of_phoneme_{phoneme}.wav"), part, sr)
        print(phoneme)
        start_idx = end_idx

# Read the CSV file and process each line
i = 1
with open(csv_file, mode="r", encoding="utf-8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        process_line(row, i)
        i += 1
