import os
import sys
import shutil


def stageImages(dirName, diseaseType):
    diseaseType = diseaseType.lower().strip()
    print(diseaseType)

    dataEntry = open("archive/Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()

    os.mkdir("nih_staged")
    os.mkdir("nih_staged/pneumonia")
    # Traverse CSV file
    for i in range(1, len(lines)): #skip first line (column labels)
        line = lines[i].strip().split(",") #delimiter may need to be changed
        filename = line[0]
        disease = line[1].lower().strip()

        # Pick out images of diseaseType from dirName
        # print(disease)
        if (diseaseType in disease) == True:
            for file in os.scandir(dirName + '/images'): # dirpath may need to be changed
                if file.name == filename:
                    shutil.copy(dirName + '/images/' + file.name, "nih_staged/pneumonia/")







if __name__ == "__main__":
    stageImages("archive/images_001", "Pneumonia")
