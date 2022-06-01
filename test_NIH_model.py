import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

from pathlib import Path
import os

def testSet(name, dir, model, class_names):
    files = os.listdir(dir)
    total = len(files)
    correct = 0
    guesses = [0,0,0]

    image_height = 180
    image_width = 180

    print("Testing a total of {:d} {:s} files".format(total, name))

    for fileName in files:
        img = tf.keras.utils.load_img(dir / fileName, target_size = (image_height, image_width))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        if (class_names[np.argmax(score)] == name):
            correct = correct + 1
        guesses[np.argmax(score)] +=1
    
    print("A total of {:d} out of {:d} {:s} files correct ({:.2f} accuracy)".format(correct, total, name, correct / total))
    print("GUESSES: {:s}: {:d}, {:s}: {:d}, {:s}: {:d}".format(
        class_names[0], guesses[0], class_names[1], guesses[1], class_names[2], guesses[2]
    ))
    return (correct, total)

def main():
    train_dir = Path("./nih_staged")
    test_dir = Path("./nih_test")

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
    model = tf.keras.models.load_model("nihModel")

    (nC, nT) = testSet("neither", test_dir / "neither", model, class_names)
    (aC, aT) = testSet("atelectasis", test_dir / "atelectasis", model, class_names)
    (pC, pT) = testSet("pneumonia", test_dir / "pneumonia", model, class_names)

    print("A total score of {:d}/{:d} ({:.3f} accuracy)".format(
        nC + aC + pC, nT + aT + pT, (nC + aC + pC) / (nT + aT + pT)
    ))


if __name__ == "__main__":
    main()