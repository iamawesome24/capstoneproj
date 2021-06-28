import tensorflow as tf
import tifffile as tff
import matplotlib.pyplot as plt


def dense_block(units, dropout_rate):
    block = tf.keras.Sequential([
        tf.keras.layers.Dense(units, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(dropout_rate)
    ])
    
    return block
    
def build_model():
    
    efficient_net = tf.keras.applications.DenseNet121(classes=2, 
                                                      include_top=False,
                                                      input_shape=(96,96,3))

    inp = tf.keras.Input(shape=(96,96,3))
    x = efficient_net(inp)
    gap = tf.keras.layers.GlobalAveragePooling2D(name='GlobalAvgPool')(x)
    gap=dense_block(1024, 0.4)(gap)
    gap=dense_block(512, 0.4)(gap)
    gap = tf.keras.layers.Dense(2, activation='linear')(gap)

    gmp = tf.keras.layers.GlobalMaxPooling2D(name='GlobalMaxPool')(x)
    gmp=dense_block(1024, 0.4)(gmp)
    gmp=dense_block(512, 0.4)(gmp)
    # gmp=dense_block(64, 0.3)(gmp)

    gmp = tf.keras.layers.Dense(2, activation='linear')(gmp)

    out = tf.keras.layers.add([gap, gmp])
    out = tf.keras.layers.Dense(1, activation='sigmoid')(out)

    model = tf.keras.Model(inputs=inp, outputs=out)
    return model

model=build_model()
model.add_weight('/content/drive/MyDrive/weights/Breast_Cancer/DenseNet121_fold_5.h5')

img=tff.imread('/content/drive/MyDrive/weights/Breast_Cancer/00001b2b5609af42ab0ab276dd4cd41c3e7745b5.tif')
plt.imshow(img)
plt.axis('off')

p=model.predict(img.reshape((1,96,96,3)))
if p > 0.4 : 
    return('cancer cell present in image')
else : 
    return('no cancer cell present in image')

