import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
model = tf.keras.models.load_model('/content/Inceptionv3.h5')

img = cv2.imread('/content/xray.jpeg')
#print(img)
plt.imshow(img,cmap='gray')

img = cv2.resize(img,(150,150))
img = img.reshape((1,150,150,3))

#print(img.shape)

def xray_pred(path):
    img = '/content/capstoneproj/Dashboard/' + path
    img = cv2.resize(img,(150,150))
    img = img.reshape((1,150,150,3))

    a = model.predict(img)
    
    return a[0][0]