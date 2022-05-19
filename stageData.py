import os
import sys
import shutil

if __name__ == "__main__":
    stageImages(images_001, "Pneumonia")


def stageImages(dirName, diseaseType):
    diseaseType = diseaseType.lower().trim()

    dataEntry = open("Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()

    # Traverse CSV file
    for i in range(1, len(lines)): #skip first line (column labels)
        line = lines[i].strip().split(",") #delimiter may need to be changed
        filename = line[0]
        disease = line[1].lower().trim()

        # Pick out images of diseaseType from dirName
        if disease == diseaseType:
            for file in os.scandir(dirName + '/images'): # dirpath may need to be changed
                if file == filename:
                    shutil.copy(dirName + '/images/' + file, "DEST DIR")







