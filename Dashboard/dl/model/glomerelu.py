import tensorflow as tf 
import matplotlib.pyplot as plt
import segmentation_models as sm
import cv2
encoder= 'efficientnetb3'
IMG_SIZE=512

path='/content/107.png'
img=tf.image.decode_png(tf.io.read_file(path),channels=3)
model=sm.Unet(encoder,input_shape=(IMG_SIZE,IMG_SIZE,3),classes=1)
model.load_weights('/content/glomerelu.h5')

#display_img = model.predict(img.numpy().reshape((1,512,512,3))).reshape((512,512,1))
# cv2.imwrite(filename, img)

plt.imshow(img)
plt.imshow((model.predict(img.numpy().reshape((1,512,512,3)))).reshape((512,512)),cmap='coolwarm',alpha=0.5)

plt.axis('off')
#plt.show()
plt.savefig('/content/capstoneproject/Dashboard/dash_app/static/assets/img/outglomerelu.png')
