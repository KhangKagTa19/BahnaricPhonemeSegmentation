import os
import numpy as np
import pandas as pd
import librosa
from dtw import dtw
from sklearn.neighbors import KNeighborsClassifier

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

# Function to extract MFCC features from an audio file
def extract_mfcc(audio_file, sr):
    y, _ = librosa.load(audio_file, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=NUMBER_OF_MFCC, n_fft=NUMBER_FFT, hop_length=HOP_LENGTH)
    return mfcc.T

# Function to find the most similar WAV file using DTW
def find_most_similar_wav(input_mfcc, database_folder):
    # Initialize variables to store the most similar WAV file and its distance
    most_similar_wav = None
    min_distance = float('inf')

    # Iterate over the database WAV files
    for filename in os.listdir(database_folder):
        database_file = os.path.join(database_folder, filename)
        if not os.path.isfile(database_file):
            continue

        # Extract MFCC features from the database audio file
        database_mfcc = extract_mfcc(database_file, sr=22050)  # Adjust sampling rate as needed

        # Compute DTW distance between input and database MFCC features
        alignment = dtw(input_mfcc, database_mfcc, keep_internals=True)
        distance = alignment.distance

        # Update most similar WAV file if distance is smaller
        if distance < min_distance:
            min_distance = distance
            most_similar_wav = database_file

    return most_similar_wav

# Function to refine the search using k-nearest neighbor (KNN) classifier
def refine_search(input_mfcc, candidates, k=5):
    # Extract MFCC features from candidate WAV files
    candidate_mfcc = [extract_mfcc(candidate, sr=22050) for candidate in candidates]

    # Flatten MFCC features
    X = np.vstack(candidate_mfcc)

    # Create labels (indices of candidate files)
    y = np.repeat(np.arange(len(candidates)), [len(mfcc) for mfcc in candidate_mfcc])

    # Train KNN classifier
    knn = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
    knn.fit(X, y)

    # Predict the most similar candidate using the KNN classifier
    input_mfcc_flattened = input_mfcc.flatten().reshape(1, -1)
    predicted_index = knn.predict(input_mfcc_flattened)[0]
    most_similar_wav = candidates[predicted_index]

    return most_similar_wav

# Function to process the input audio file
def process_audio(input_file, database_folder):
    # Extract MFCC features from the input audio
    input_mfcc = extract_mfcc(input_file, sr=22050)  # Adjust sampling rate as needed

    # Find initial candidate using DTW
    initial_candidate = find_most_similar_wav(input_mfcc, database_folder)

    # Refine search using KNN classifier
    candidates = [os.path.join(database_folder, filename) for filename in os.listdir(database_folder)]
    refined_candidate = refine_search(input_mfcc, candidates)

    return initial_candidate, refined_candidate

# Example usage
input_file = 'han_cut.wav'
database_folder = 'phoneme_folders'

initial_candidate, refined_candidate = process_audio(input_file, database_folder)

print("Initial candidate:", initial_candidate)
print("Refined candidate:", refined_candidate)
