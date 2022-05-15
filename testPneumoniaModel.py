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

normal_files = os.listdir(test_dir / "NORMAL")

total = 0
correct = 0
print("Testing {:d} normal files".format(len(normal_files)))
for file in normal_files:
    total = total + 1
    img = tf.keras.utils.load_img(
        test_dir / "NORMAL" / file, target_size = (image_height, image_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    if (class_names[np.argmax(score)] == "NORMAL"):
        correct = correct + 1

print("A total of {:d} out of {:d} normal files correct ({:.2f} accuracy)".format(correct, total, correct / total))

virus_files = os.listdir(test_dir / "PNEUMONIA")

total = 0
correct = 0
print("Testing {:d} pneumonia files".format(len(virus_files)))
for file in virus_files:
    total = total + 1
    img = tf.keras.utils.load_img(
        test_dir / "PNEUMONIA" / file, target_size = (image_height, image_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    if (class_names[np.argmax(score)] == "PNEUMONIA"):
        correct = correct + 1

print("A total of {:d} out of {:d} pneumonia files correct ({:.2f} accuracy)".format(correct, total, correct / total))