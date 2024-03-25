import os
import csv
import soundfile as sf

# Define the base directory where the phoneme folders are located
base_directory = "./phoneme_folders"

# Function to calculate the mean length of WAV files in a folder
def calculate_mean_wav_length(folder_path):
    total_length = 0
    num_files = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            file_path = os.path.join(folder_path, filename)
            # Load the WAV file to get its duration
            with sf.SoundFile(file_path, 'r') as f:
                total_length += len(f) / f.samplerate
                num_files += 1
    if num_files > 0:
        return total_length / num_files
    else:
        return 0

# Prepare CSV file for storing mean lengths
csv_output_file = "mean_lengths.csv"
csv_header = ["Phoneme", "Mean_Wav_Length"]
csv_rows = []

# Traverse through each phoneme folder
for phoneme_folder in os.listdir(base_directory):
    phoneme_folder_path = os.path.join(base_directory, phoneme_folder)
    if phoneme_folder_path.endswith("upper_u"):
        mean_length = calculate_mean_wav_length(phoneme_folder_path)
        csv_rows.append(['U', mean_length])
    elif os.path.isdir(phoneme_folder_path):
        mean_length = calculate_mean_wav_length(phoneme_folder_path)
        csv_rows.append([phoneme_folder, mean_length])
    

# Write the collected information to the CSV file
with open(csv_output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_header)
    writer.writerows(csv_rows)

print("Mean lengths calculated and stored in:", csv_output_file)