import efficientnet.tfkeras as efn
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

model_list=[efn.EfficientNetB0,
efn.EfficientNetB1,
efn.EfficientNetB2,
efn.EfficientNetB3,
efn.EfficientNetB4,
efn.EfficientNetB5,
efn.EfficientNetB6,
]

def build_model(n):
    
    base=model_list[n](input_shape=(512,512,3), 
                       weights=None,
                       include_top=False,pooling='avg')
    inp=tf.keras.layers.Input((512,512,3))
    x=base(inp)
    x=tf.keras.layers.Dense(500,activation='relu')(x)
    x=tf.keras.layers.Dropout(0.3)(x)
    x=tf.keras.layers.Dense(6,activation='softmax')(x)
    model= tf.keras.Model(inputs=inp,outputs=x)
    
    return model

def prostatepred(path):
    model = build_model(5)
    model.load_weights('/content/prostate.h5')
    img=tf.image.decode_png(tf.io.read_file('/content/101.png'),channels=3)
    plt.imshow(img)
    pred=np.argmax(model.predict(img.numpy().reshape((1,512,512,3))))
    print("Tissue Grade = ", pred)
    return pred