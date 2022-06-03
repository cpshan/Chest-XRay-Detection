import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

from pathlib import Path
import os

def main():
    train_dir = Path('./infil_staged')
    test_dir = Path('/infil_test')

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

    classNames = train_ds.class_names
    print(classNames)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        validation_split = 0.2,
        subset = "validation",
        seed = 123,
        image_size = (image_height, image_width),
        batch_size = batch_size
    )

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    num_classes = len(classNames)

    model = Sequential([
        layers.Rescaling(1./255, input_shape=(image_height, image_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    epochs = 1
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    model.save('infilModel')


if __name__ == "__main__":
    main()