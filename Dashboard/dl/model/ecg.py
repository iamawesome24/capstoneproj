import tensorflow as tf
import cv2
import os
import librosa
import librosa.display
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

model = tf.keras.models.load_model('/content/capstoneproj/Dashboard/dl/ecg.h5')


def converttoSpectrogram(x):
    sos = signal.butter(5, 25, 'lp', fs=125, output='sos')
    filtered = signal.sosfilt(sos, x)   
    X = librosa.stft(filtered,n_fft=10)
    Xdb = librosa.amplitude_to_db(abs(X))
    print(Xdb.shape)
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=125)
    plt.savefig('temp.jpg', bbox_inches='tight')
    plt.close()
 
    image = cv2.imread('temp.jpg')[:,:,[2,1,0]]
    os.remove('temp.jpg')
    return cv2.resize(image,(128,128))

def prediction(file):

    path = '/content/capstoneproj/Dashboard/'+ file

    train = pd.read_csv(path)
    temp = train.iloc[30,:-1].values
    b = converttoSpectrogram(temp)
    b = b.reshape(1,128,128,3)
    print(b.shape)
    a = model.predict(b)
    print(a)
    return a