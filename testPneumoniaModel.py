import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

from pathlib import Path
import os

data_dir = Path('./chest-xray-pneumonia/chest_xray/chest_xray')

train_dir = data_dir / 'train'
val_dir = data_dir / 'val'
test_dir = data_dir / 'test'

batch_size = 32
image_height = 180
image_width = 180

train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    validation_split = 0.2,
    subset = "training",
    seed = 123,
    image_size = (image_height, image_width),
    batch_size = batch_size
)

class_names = train_ds.class_names

model = tf.keras.models.load_model('pneumoniaModel')

normal_test = Path('./chest-xray-pneumonia/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg')
virus_test = Path('./chest-xray-pneumonia/chest_xray/chest_xray/test/PNEUMONIA/person1_virus_6.jpeg')

img = tf.keras.utils.load_img(
    normal_test, target_size = (image_height, image_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)

img = tf.keras.utils.load_img(
    virus_test, target_size = (image_height, image_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)