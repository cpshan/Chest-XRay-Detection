import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

from pathlib import Path
import os

import matplotlib.pyplot as plt

def testSet(name, dir, model, class_names):
    files = os.listdir(dir)
    total = len(files)
    correct = 0
    guesses = [0,0]

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
    print("GUESSES: {:s}: {:d}, {:s}: {:d}".format(
        class_names[0], guesses[0], class_names[1], guesses[1]
    ))
    return (correct, total, guesses)

def main():
    train_dir = Path('./infil_staged')
    test_dir = Path("./infil_test")

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
    print(class_names)
    model = tf.keras.models.load_model("infilModel")

    (nC, nT, nGuesses) = testSet("infiltration", test_dir / "infiltration", model, class_names)
    (pC, pT, pGuesses) = testSet("normal", test_dir / "normal", model, class_names)

    print("A total score of {:d}/{:d} ({:.3f} accuracy)".format(
        nC + pC, nT + pT, (nC + pC) / (nT + pT)
    ))

    allGuesses = []
    allGuesses.append(nGuesses)
    allGuesses.append(pGuesses)
    allGuesses = np.array(allGuesses)

    # cm = confusion_matrix(true, allGuesses)
    # print(cm)
    plt.figure()
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.imshow(allGuesses, interpolation='none', cmap=plt.cm.PuBuGn)
    for (j, i), label in np.ndenumerate(allGuesses):
        plt.text(i, j, label, ha='center', va='center')
    plt.xticks(range(2), class_names, fontsize=16)
    plt.yticks(range(2), class_names, fontsize=16)

    input("Press enter to show plot")
    plt.show()

if __name__ == "__main__":
    main()