import os
import shutil
from PIL import Image, ImageOps
from pathlib import Path
import time

countMax = 19000

def makeDirectories():
    try:
        os.mkdir("infil_staged")
    except FileExistsError:
        print("infil_staged directory already created")

    try:
        os.mkdir("infil_staged/infiltration")
    except FileExistsError:
        print("infiltration directory already created")   

    try:
        os.mkdir("infil_staged/normal")
    except FileExistsError:
        print("normal/ directory already created")

    try:
        os.mkdir("infil_test/")
    except FileExistsError:
        print("test folder alrealy created")
    
    try:
        os.mkdir("infil_test/infiltration")
    except FileExistsError:
        print("infiltration test directory already created")   

    try:
        os.mkdir("infil_test/normal")
    except FileExistsError:
        print("normal/ test directory already created")

def stageImages(dirName, imageNum, icount, nCount):
    #Goes to 112121, but are saving the last few hundred for testing
    starts = [0, 5001, 15001, 25001, 35001, 45001, 55001, 65001, 75001, 85001, 95001, 105001, 109407]

    dataEntry = open("archive/Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()

    # Traverse CSV file
    print("going through {:d} lines ({:d} - {:d})".format(starts[imageNum] - starts[imageNum - 1],
        starts[imageNum - 1], starts[imageNum]))
    for i in range(starts[imageNum-1], starts[imageNum]): #skip first line (column labels)
        line = lines[i].strip().split(",") #delimiter may need to be changed
        filename = line[0]
        disease = line[1].lower().strip()
        # Pick out images of diseaseType from dirName

        if (('infiltration' in disease) and (icount < countMax)):
            try:
                shutil.copy(dirName + '/images/' + filename, "infil_staged/infiltration/")
                icount = icount + 1
            except:
                continue
        elif (("no finding" in disease) and (nCount < countMax)):
            try:
                shutil.copy(dirName + '/images/' + filename, "infil_staged/normal")
                nCount += 1
            except:
                continue
    return (icount, nCount)

def buildTestDir():
    #Each test directory is going to have 300 images
    #Start with normal images and atelectasis images
    dirName = "archive/images_012"
    dataEntry = open("archive/Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()
    starts = [109407, 112121]
    noneCount = 0
    infilCount = 0
    
    for i in range(starts[0], starts[1]):
        line = lines[i].lower().split(",")
        filename = line[0]
        disease = line[1].lower().strip()
        
        if (infilCount == 300) and (noneCount == 300):
            break

        # elif ("infiltration" in disease) and (infilCount < 300):
        #     try:
        #         shutil.copy(dirName + '/images/' + filename, "infil_test/infiltration")
        #         infilCount += 1
        #     except:
        #         continue

        elif ("no finding" in disease) and (noneCount < 300):
            try:
                shutil.copy(dirName + '/images/' + filename, "infil_test/normal")
                noneCount = noneCount + 1
            except:
                continue   

def main():
    makeDirectories()
    icount = 0
    nCount = 0
    print("About to go through roughly 112,000 lines")
    start = time.time()
    for i in range(1, 13, 1):
        # The nih chest xray dataset was installed and unzipped called archive/
        # If yours is different, change the path name here
        (icount, nCount) = stageImages("archive/images_0{:02d}".format(i), i, icount, nCount)
    
    end = time.time()
    print("After {:.2f} minutes, there are a total of {:d} infiltration files and {:d} normal files".format(
        (end - start) / 60, icount, nCount))

    buildTestDir()

if __name__ == "__main__":
    main()