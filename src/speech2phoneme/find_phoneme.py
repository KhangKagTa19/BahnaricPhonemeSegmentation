import os
import numpy as np
import pandas as pd
import librosa
from dtw import dtw

# Define constants
NUMBER_OF_MFCC = 13
NUMBER_FFT = 2048
HOP_LENGTH = 512

# Define the set of all possible phonemes for each phoneme_i
phonemes = {
    'phoneme_1': ['d', 'c', 'k', 'y', 'b', 'l', 's', 'nh', 'j', 'ch', 'g', 'đ', 'ɉ', 't', 'n', 'Kl', 'Gr', 'm', 'r', 'h', 'tr', 'ng', "'b", 'v', 'p'],
    'phoneme_2': ['U', 'uô', 'up', 'ĭ', 'i', 'uch', 'u', 'ih', 'ŭ', 'l', 'ol', 'o', 'ă', 'ơ', 
                  'ɯə', 'uə', 'ɤm', 'ɛ', 'a', 'ia', 'r', 'ŭq', 'oh', 'âm', 'ô', 'â', 'ĕr', 'ê', 'ư', 'ĭ', 'e'],
    'phoneme_3': ['ch', 'n', 'ng', 'o', 'a', 'h', 'c', 'm', 'r', 'd', 'k', 'q', 'i', 't', 'y', 'p', 'l'],
    'phoneme_4': ['ch', 'o', 'i', 'đ', 'au', 'u', 'e'],
    'phoneme_5': ['ng', 'h', 'u'],
    'phoneme_6': ['nh']
}

# Function to find optimal warping between target audio and database audios
def find_optimal_warping(file_paths, target_audio, sr):
    most_similar_score = float('-inf')
    most_similar_file = None

    # Iterate over database audio files
    for filename in file_paths:
        # Load database audio
        database_audio, _ = librosa.load(filename, sr=sr)

        # Extract MFCC features for database audio
        database_mfcc = librosa.feature.mfcc(y=database_audio, sr=sr, n_mfcc=NUMBER_OF_MFCC, n_fft=NUMBER_FFT, hop_length=HOP_LENGTH)

        # Check if either sequence has zero length
        if target_audio.shape[0] == 0 or database_mfcc.shape[1] == 0:
            print("One of the sequences has zero length. Skipping DTW computation.")
            continue

        # Compute DTW similarity
        alignment = dtw(target_audio.T, database_mfcc.T, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
        similarity_score = alignment[0]  # Access the distance from the alignment tuple
        
        # Update most similar if necessary
        if similarity_score > most_similar_score:
            most_similar_score = similarity_score
            most_similar_file = filename

    return most_similar_file, most_similar_score

# Function to process the input audio file
def process_audio(input_file):
    # Step 1: Remove silence
    y, sr = librosa.load(input_file)
    non_silent_intervals = librosa.effects.split(y)
    start_time, end_time = non_silent_intervals[0][0], non_silent_intervals[-1][1]
    target_audio = y[start_time:end_time]

    # Step 2: Iterate through each phoneme set and find optimal subsequence warping
    best_phoneme_files = []
    remaining_audio = target_audio
    for phoneme_set in ['phoneme_1', 'phoneme_2', 'phoneme_3', 'phoneme_4', 'phoneme_5', 'phoneme_6']:
        phoneme_files = []
        mean_length_df = pd.read_csv('mean_lengths.csv')
        for phoneme in phonemes[phoneme_set]:
            mean_length_row = mean_length_df[mean_length_df['Phoneme'] == phoneme]
            mean_length = mean_length_row['Mean_Wav_Length'].values[0]
            mean_length_samples = int(mean_length * sr)
            cut_audio = remaining_audio[:mean_length_samples]

            # Find the folder path corresponding to the phoneme
            if phoneme == 'U':
                folder_path = os.path.join('./phoneme_folders', 'upper_u')
            else:
                folder_path = os.path.join('./phoneme_folders', phoneme)

            if os.path.exists(folder_path):
                file_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
                best_phoneme_file = find_optimal_warping(file_paths, cut_audio, sr)
                phoneme_files.append(best_phoneme_file)

        # Add the best phoneme file for this step to the overall list
        best_tuple = max(phoneme_files, key=lambda x: x[1]) if phoneme_files else None
        if best_tuple:
            best_phoneme_files.append(best_tuple)

        # Update the remaining audio
        if best_tuple:
            best_phoneme_audio, _ = librosa.load(best_tuple[0], sr=sr)
            remaining_audio = remaining_audio[len(best_phoneme_audio):]

            # Break if remaining audio is empty
            if len(remaining_audio) == 0:
                break

    return best_phoneme_files

input_file = 'han_cut.wav'
result = process_audio(input_file)
print(result)
