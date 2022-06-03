import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

from pathlib import Path
import os
import sys

def testPath(model, class_names):
    image_height = 180
    image_width = 180
    print()
    print("Enter path to file you want to test (ex: pneumonia/person47_backteria_229.jpeg)")
    testPath = input("Or type exit to leave: ")

    while(testPath != "exit"):
        print()
        img = tf.keras.utils.load_img(testPath, target_size=(image_height, image_width))
        imgArray = tf.keras.utils.img_to_array(img)
        imgArray = tf.expand_dims(imgArray, 0)

        predictions = model.predict(imgArray)
        score = tf.nn.softmax(predictions[0])

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[np.argmax(score)], 100 * np.max(score))
        )
        print()

        print("Enter path to file you want to test (ex: pneumonia/person47_backteria_229.jpeg)")
        testPath = input("Or type exit to leave: ")

def processArgs(argv):
    train_dir = None
    modelName = None

    if (len(argv) != 2):
        print("Usage: python handsOnTest.py <model_to_test>")
        print("Model options are pneumonia and mix")
        exit()
    
    elif (argv[1] == "pneumonia"):
        train_dir = Path("./chest-xray-pneumonia/chest_xray/train")
        modelName = "smallModel"
    
    elif (argv[1] == "infiltration"):
        train_dir = Path("./infil_staged/")
        modelName = "infilModel"
    
    elif (argv[1] == "mix"):
        train_dir = Path("./nih_staged")
        modelName = "nihModel"
    
    else:
        print("Usage: python handsOnTest.py <model_to_test>")
        print("Model options are pneumonia, infiltration, and mix")
        exit()

    return (train_dir, modelName)

def main(argv):
    (train_dir, modelName) = processArgs(argv)

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
    model = tf.keras.models.load_model(modelName)

    testPath(model, class_names)

if __name__ == "__main__":
    main(sys.argv)