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


if os.path.exists("Am vi Ba Na"):
    shutil.rmtree("Am vi Ba Na")
# Unzip the ZIP file
with zipfile.ZipFile("Am vi Ba Na-20240202T004404Z-001.zip", "r") as zip_file:
    zip_file.extractall()
shutil.move("Am vi Ba Na", "bahnaric/dataset/raw")
#os.remove("bahnardata.zip")