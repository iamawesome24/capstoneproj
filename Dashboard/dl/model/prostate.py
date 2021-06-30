import efficientnet.tfkeras as efn
import numpy as np, pandas as pd, os
import matplotlib.pyplot as plt, cv2
import tensorflow as tf, re, math


def read_tfrec(file):
    
    ex = tf.io.parse_single_example(file,features=feature)
    return ex['image'],ex['file_id']

def decode(img,lab):
    
    img=tf.image.resize(tf.image.decode_jpeg(img,channels=3),(IMG_SIZE,IMG_SIZE))
    img=tf.cast(img,tf.float32)/255.0
    
    return img,lab

def data_gen(files,bs=10,aug=True,cache=True,repeat=True,shuffle=True):
    ds=tf.data.TFRecordDataset(files,num_parallel_reads=tf.data.experimental.AUTOTUNE)
    
    
    ds=ds.map(read_tfrec,num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds=ds.map(decode,num_parallel_calls=tf.data.experimental.AUTOTUNE)
    
#     ds=ds.map(get_predictions,num_parallel_calls=tf.data.experimental.AUTOTUNE) if aug else ds

    ds=ds.prefetch(tf.data.experimental.AUTOTUNE)
    ds=ds.batch(1,drop_remainder=True)
    return ds



def build_model(n):
    
    base=model_list[n](input_shape=(IMG_SIZE,IMG_SIZE,3), 
#                        weights='loho',
                       weights=None,#../input/effnetweights/efficientnet-b3_weights_tf_dim_ordering_tf_kernels_autoaugment_notop.h5', 
                       include_top=False,pooling='avg')
    inp=tf.keras.layers.Input((IMG_SIZE,IMG_SIZE,3))
    x=base(inp)
    x=tf.keras.layers.Dense(500,activation='relu')(x)
    x=tf.keras.layers.Dropout(0.3)(x)
    x=tf.keras.layers.Dense(6,activation='softmax')(x)
    model= tf.keras.Model(inputs=inp,outputs=x)
    
    return model



def prostatepred(path):
    IMG_SIZE=512 

    feature = {
        'file_id': tf.io.FixedLenFeature([], tf.string),
        'image': tf.io.FixedLenFeature([], tf.string),
    }
    files=tf.io.gfile.glob(path)    
    ds=data_gen(files)
    
    model_list=[efn.EfficientNetB0,
    efn.EfficientNetB1,
    efn.EfficientNetB2,
    efn.EfficientNetB3,
    efn.EfficientNetB4,
    efn.EfficientNetB5,
    efn.EfficientNetB6,
    ]

    model=build_model(5)
    model.load_weights('/content/prostate.h5')
    preds=model.predict( ds,steps=10,verbose=1)
    
    sub_file=pd.DataFrame()#read_csv('../input/prostate-cancer-grade-assessment/sample_submission.csv')

    sub_file['image_id']=np.array([img_name.numpy().decode("utf-8") for img, img_name in iter(ds.unbatch())])
    sub_file = sub_file.iloc[:10]
    sub_file['isup_grade']=np.argmax(preds,axis=1)

    return (sub_file.head(5))
    