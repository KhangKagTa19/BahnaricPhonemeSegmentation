import os
import csv
import librosa
import soundfile as sf

# Define dictionaries
first_phoneme_dict = {'y': 1, 'ch': 1, 'k': 4, 'h': 4, 'm': 3, 'c': 3, 'l': 9, 'j': 2, 'd': 3, 'r': 3, 'p': 2, 'g': 2, 'đ': 5, 'tr': 1, 's': 1, 't': 3, 'nh': 2, 'b': 3, '‰': 1, 'n': 1, 'ng': 1}
second_phoneme_dict = {'a': 6, 'r': 1, 'ơ': 1, 'ư': 2, 'ă': 10, 'ứ': 1, 'u': 8, 'uô': 1, 'ia': 1, 'e': 1, 'o': 5, 'ê': 2, 'i': 4, 'uə': 1, 'U': 3, 'ô': 1, 'ĭ': 2, 'ɛ': 1, 'ự': 1, 'â': 2}
third_phoneme_dict = {'h': 9, 'a': 1, 'l': 8, 'ch': 3, 'q': 2, 'p': 4, 'ng': 6, 'i': 3, 'n': 2, 't': 3, 'k': 3, 'm': 7, 'o': 1, 'c': 1, 'r': 2}

# Create folders
for folder_name, phoneme_dict in [("phoneme1", first_phoneme_dict), ("phoneme2", second_phoneme_dict), ("phoneme3", third_phoneme_dict)]:
    os.makedirs(folder_name, exist_ok=True)
    
    # Create subfolders based on phonemes
    for phoneme in phoneme_dict.keys():
        subfolder_path = os.path.join(folder_name, phoneme)
        os.makedirs(subfolder_path, exist_ok=True)

# Define the path to the CSV file
csv_file = "3_phoneme_features.csv"

# Function to process each line
def process_line(row, row_idx):
    # Extract information from the row
    filename = row['file_name'].replace('\\\\', '\\')
    start = float(row['start'])
    phoneme1_length = float(row['phoneme_1_length'])
    phoneme2_length = float(row['phoneme_2_length'])
    phoneme3_length = float(row['phoneme_3_length'])
    full_phoneme = row['full_phoneme']
    phonemes = [row['phoneme_1'],row['phoneme_2'],row['phoneme_3']]
    print(len(phonemes))

    # Change .TextGrid to .wav in filename
    audio_filename = str(filename).replace('.TextGrid', '.wav')
    print(audio_filename)
    # Load the audio file
    audio, sr = librosa.load(audio_filename, sr=None)
    
    # Convert start and lengths to sample indices
    start_idx = int(start * sr)
    end_idx1 = start_idx + int(phoneme1_length * sr)
    end_idx2 = end_idx1 + int(phoneme2_length * sr)
    end_idx3 = end_idx2 + int(phoneme3_length * sr)

    # Cut the audio into three parts based on phoneme lengths
    part1 = audio[start_idx:end_idx1]
    part2 = audio[end_idx1:end_idx2]
    part3 = audio[end_idx2:end_idx3]

    # Save each part to the corresponding subfolder
    for idx, part in enumerate([part1, part2, part3], start=1):
        if idx <= len(phonemes):  # Check if idx is within the bounds of phonemes list
            phoneme = phonemes[idx-1]
            folder_name = f"phoneme{idx}"
            subfolder_path = os.path.join(folder_name, phoneme)
            os.makedirs(subfolder_path, exist_ok=True)
            sf.write(os.path.join(subfolder_path, f"{row_idx}_of_phoneme_{phoneme}.wav"), part, sr)
        else:
            print(f"Error: Phoneme index {idx} is out of range.")

# Read the CSV file and process each line
i = 1
with open(csv_file, mode="r", encoding="utf-8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        process_line(row, i)
        i+=1
