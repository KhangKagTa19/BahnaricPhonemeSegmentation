import csv
# Define an empty set to store unique phoneme characters
phoneme_characters = set()

# Open the CSV file and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract phoneme characters from phoneme_1 to phoneme_6 columns
        for i in range(1, 7):
            phoneme_column = f'phoneme_{i}'
            phoneme = row[phoneme_column].strip()
            # If the phoneme column is not empty, add its characters to the set
            if phoneme:
                phoneme_characters.update(phoneme.split(','))

# Print the unique phoneme characters
print("All possible phoneme characters:", phoneme_characters)
all_possible_phonemes = set()
# Open the CSV file with UTF-8 encoding and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Get the phoneme from the phoneme_1 column
        phoneme_1 = row['phoneme_1'].strip()
        # If the phoneme_1 column is not empty, add its phonemes to the set
        if phoneme_1:
            all_possible_phonemes.update(phoneme_1.split(','))

# Print the set of all possible phonemes
print("Set of all possible phonemes can be phoneme_1:", all_possible_phonemes)


all_possible_phonemes = set()
# Open the CSV file with UTF-8 encoding and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Get the phoneme from the phoneme_1 column
        phoneme_1 = row['phoneme_2'].strip()
        # If the phoneme_1 column is not empty, add its phonemes to the set
        if phoneme_1:
            all_possible_phonemes.update(phoneme_1.split(','))

# Print the set of all possible phonemes
print("Set of all possible phonemes can be phoneme_2:", all_possible_phonemes)

all_possible_phonemes = set()
# Open the CSV file with UTF-8 encoding and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Get the phoneme from the phoneme_1 column
        phoneme_1 = row['phoneme_3'].strip()
        # If the phoneme_1 column is not empty, add its phonemes to the set
        if phoneme_1:
            all_possible_phonemes.update(phoneme_1.split(','))

# Print the set of all possible phonemes
print("Set of all possible phonemes can be phoneme_3:", all_possible_phonemes)

all_possible_phonemes = set()
# Open the CSV file with UTF-8 encoding and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Get the phoneme from the phoneme_1 column
        phoneme_1 = row['phoneme_4'].strip()
        # If the phoneme_1 column is not empty, add its phonemes to the set
        if phoneme_1:
            all_possible_phonemes.update(phoneme_1.split(','))

# Print the set of all possible phonemes
print("Set of all possible phonemes can be phoneme_4:", all_possible_phonemes)

all_possible_phonemes = set()
# Open the CSV file with UTF-8 encoding and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Get the phoneme from the phoneme_1 column
        phoneme_1 = row['phoneme_5'].strip()
        # If the phoneme_1 column is not empty, add its phonemes to the set
        if phoneme_1:
            all_possible_phonemes.update(phoneme_1.split(','))

# Print the set of all possible phonemes
print("Set of all possible phonemes can be phoneme_5:", all_possible_phonemes)

all_possible_phonemes = set()
# Open the CSV file with UTF-8 encoding and iterate through each row
with open('database.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Get the phoneme from the phoneme_1 column
        phoneme_1 = row['phoneme_6'].strip()
        # If the phoneme_1 column is not empty, add its phonemes to the set
        if phoneme_1:
            all_possible_phonemes.update(phoneme_1.split(','))

# Print the set of all possible phonemes
print("Set of all possible phonemes can be phoneme_6:", all_possible_phonemes)