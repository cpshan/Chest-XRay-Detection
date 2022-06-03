import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from pathlib import Path
import os

import matplotlib.pyplot as plt

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
    return (correct, total, guesses)

def main():
    test_dir = Path("./nih_test")

    class_names = ['atelectasis', 'infiltration', 'neither']
    model = tf.keras.models.load_model("nihModel")

    (nC, nT, nGuesses) = testSet("neither", test_dir / "neither", model, class_names)
    (aC, aT, aGuesses) = testSet("atelectasis", test_dir / "atelectasis", model, class_names)
    (pC, pT, pGuesses) = testSet("infiltration", test_dir / "infiltration", model, class_names)

    print("A total score of {:d}/{:d} ({:.3f} accuracy)".format(
        nC + aC + pC, nT + aT + pT, (nC + aC + pC) / (nT + aT + pT)
    ))

    allGuesses = []
    allGuesses.append(aGuesses)
    allGuesses.append(pGuesses)
    allGuesses.append(nGuesses)
    allGuesses = np.array(allGuesses)

    # cm = confusion_matrix(true, allGuesses)
    # print(cm)
    plt.figure()
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.imshow(allGuesses, interpolation='none', cmap=plt.cm.PuBuGn)
    for (j, i), label in np.ndenumerate(allGuesses):
        plt.text(i, j, label, ha='center', va='center')
    plt.xticks(range(3), class_names, fontsize=16)
    plt.yticks(range(3), class_names, fontsize=16)

    input("Press enter to show plot")
    plt.show()




if __name__ == "__main__":
    main()