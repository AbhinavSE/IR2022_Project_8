from glob import glob
import librosa
import librosa.display as dsp
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import numpy as np
from PIL import Image
import joblib
import cv2
from sklearn.model_selection import train_test_split
import keras
import random
from keras.models import Sequential
from keras.models import Model
from keras.layers import *
import pandas as pd
from tqdm.notebook import tqdm
import pathlib
import io
from six.moves.urllib.request import urlopen
import warnings
warnings.filterwarnings("ignore")


def create_spectrogram_file(inp_file):
    if not os.path.exists('Data/Test'):
        os.makedirs('Data/Test')
    y, sr = librosa.load(inp_file)
    melspectrogram_array = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=8000)
    mel = librosa.power_to_db(melspectrogram_array)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = float(mel.shape[1]) // float(100)
    fig_size[1] = float(mel.shape[0]) // float(100)
    plt.rcParams["figure.figsize"] = fig_size
    plt.axis('off')
    plt.axes([0., 0., 1., 1.0], frameon=False, xticks=[], yticks=[])
    librosa.display.specshow(mel, cmap='gray_r')
    if not os.path.exists('Data/Test_Spectogram_Images'):
        os.makedirs('Data/Test_Spectogram_Images')
    op_file = "Data/Test_Spectogram_Images/"+inp_file.split("/")[-1].split(".")[0]+".jpg"
    plt.savefig(op_file, bbox_inches=None, pad_inches=0)
    plt.close()
    return op_file

def slice_spect_file(inp_file):
    img = Image.open(inp_file)
    subsample_size = 128
    width, height = img.size
    number_of_samples = width // subsample_size
    op_files = []
    counter = 0
    if not os.path.exists('Data/Test_Sliced_Images'):
        os.makedirs('Data/Test_Sliced_Images')
    for i in range(number_of_samples):
        start = i*subsample_size
        img_temporary = img.crop((start, 0., start + subsample_size, subsample_size))
        op_file = "Data/Test_Sliced_Images/" +str(counter)+"_"+inp_file.split("/")[-1]
        img_temporary.save(op_file)
        op_files.append(op_file)
        counter = counter + 1
    return op_files

def get_data(inp_file):
    # print("Creating Spectogram...")
    op_file = create_spectrogram_file(inp_file)
    # print("Slicing Spectogram...")
    filenames = slice_spect_file(op_file)
    # print("Converting to numpy array")
    images_all = [None]*(len(filenames))
    index = 0
    for f in filenames:
        temp = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        images_all[index] = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        index += 1
    images = np.array(images_all)
    return images

def get_data_online_url(url):
    # print("Fetching File from URL...")
    z = io.BytesIO(urlopen(url).read())
    if not os.path.exists('Data/Test'):
        os.makedirs('Data/Test')
    file_path = 'Data/Test/'+url.split("/")[-1]
    pathlib.Path(file_path).write_bytes(z.getbuffer())
    return get_data(file_path)

def get_genre(url, online=False):
    model = keras.models.load_model("Saved_Model/Model.h5")
    genre = {
        0: "Hip-Hop",
        1: "International",
        2: "Electronic",
        3: "Folk",
        4: "Experimental",
        5: "Rock",
        6: "Pop",
        7: "Instrumental"
        }
    if online:
        inputs = get_data_online_url(url)
    else:
        inputs = get_data(url)
    outputs = model(inputs)
    output = np.argmax(outputs, axis=1)
    return [genre[label] for label in output]

def get_embeddings(url, online=False):
    raw_model = keras.models.load_model("Saved_Model/Model.h5")
    model = Model(inputs=raw_model.input, outputs=raw_model.layers[-2].output)
    if online:
        inputs = get_data_online_url(url)
    else:
        inputs = get_data(url)
    outputs = model(inputs)
    output = np.mean(outputs, axis=0)
    return output


metadata = pd.read_csv("Data/metadata.csv")
embeddings = []
errors = 0
for path in tqdm(metadata["music_folder"]):
    try:
        embeddings.append(get_embeddings("Data"+path))
    except Exception as e:
        errors += 1
        embeddings.append(np.zeros(128))

embeddings = np.array(embeddings)
joblib.dump(embeddings, "Data/embeddings.pkl")
