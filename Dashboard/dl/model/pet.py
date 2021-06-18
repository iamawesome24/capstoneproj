import os
import glob
import cv2 
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from tqdm import tqdm
import gc
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf

model = tf.keras.models.load_model('/content/capstoneproj/Dashboard/dl//pet.h5')


def readImage(location,y_temp):
    image = nib.load(location)
    temp = np.array(image.get_fdata())[:,:,:,0]
    
    return (temp/temp.max()).astype(np.float32),y_temp



def getSegments_test(subject,y_temp):
    #subject = subject.numpy()
    
    ret,thresh_low = cv2.threshold(subject,0.20,1.0,cv2.THRESH_BINARY)
    ret,thresh_med = cv2.threshold(subject,0.40,1.0,cv2.THRESH_BINARY)
    ret,thresh_high = cv2.threshold(subject,0.60,1.0,cv2.THRESH_BINARY)
    
    return np.append(np.append(
    cv2.bitwise_and(thresh_low[:,:,:],subject[:,:,:]).reshape(128,128,63,1),
    cv2.bitwise_and(thresh_med[:,:,:],subject[:,:,:]).reshape(128,128,63,1),
    axis=-1), cv2.bitwise_and(thresh_high[:,:,:],subject[:,:,:]).reshape(128,128,63,1),axis=-1),y_temp



def output(file):
    
    path = '/content/capstoneproj/Dashboard/'+ file
    image,_ = readImage(path,[])
    segments,_ = getSegments_test(image,[])

    segments = segments.reshape((1,128,128,63,3))
    a = model.predict(segments)
    a = a[0][0].round()

    return a