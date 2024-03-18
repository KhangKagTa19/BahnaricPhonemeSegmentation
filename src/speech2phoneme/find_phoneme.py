import os
import librosa
import soundfile as sf
import numpy as np

def calculate_cost(audio_segment, phoneme_audio):
    D, _ = librosa.sequence.dtw(X=audio_segment, Y=phoneme_audio) 
    return D[-1, -1]

# Load the input .wav file and remove silence from the beginning
input_wav = "bahnaric/dataset/raw\lap_cut.wav"
audio, sr = librosa.load(input_wav, sr=None)
audio, _ = librosa.effects.trim(audio)

# Define the folder paths for each phoneme
phoneme_folders = ["phoneme1", "phoneme2", "phoneme3"]

# Determine the length of each segment
segment_length = len(audio) // 3
remainder = len(audio) % 3  # Handle remainder for uneven division

# Divide the audio into three segments
segments = []
start = 0
for i in range(3):
    length = segment_length
    if remainder > 0:
        length += 1  # Add one extra sample to the segment if there's a remainder
        remainder -= 1
    segments.append(audio[start:start+length])
    start += length


# Traverse through each segment
for i, segment in enumerate(segments, start=1):
    # Get the corresponding phoneme folder for this segment
    phoneme_folder = phoneme_folders[i - 1]
    
    min_cost = float('inf')
    min_cost_file = None
    
    # Traverse through each subfolder within the phoneme folder
    for subfolder in os.listdir(phoneme_folder):
        subfolder_path = os.path.join(phoneme_folder, subfolder)
        if os.path.isdir(subfolder_path):
            # Traverse through each file in the subfolder
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".wav"):
                    phoneme_file = os.path.join(subfolder_path, filename)
                    phoneme_audio, _ = librosa.load(phoneme_file, sr=sr)
                    cost = calculate_cost(segment, phoneme_audio)
                    if cost < min_cost:
                        min_cost = cost
                        min_cost_file = phoneme_file
    
    # Print the filename with the minimum cost for this segment and phoneme folder
    print(f"For part {i}, best phoneme in folder {phoneme_folder}: {min_cost_file}")
