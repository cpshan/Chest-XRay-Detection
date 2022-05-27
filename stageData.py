import os
from posixpath import dirname
import sys
import shutil

def makeDirectories():
    try:
        os.mkdir("nih_staged")
    except FileExistsError:
        print("nih_staged directory already created!")

    try:
        os.mkdir("nih_staged/pneumonia")
    except FileExistsError:
        print("pneumonia directory already created")   
    
    try:
        os.mkdir("nih_staged/atelectasis")
    except FileExistsError:
        print("atelectasis directory already created")

    try:
        os.mkdir("nih_staged/neither")
    except FileExistsError:
        print("neither/ directory already created")

def stageImages(dirName, imageNum):
    starts = [0, 5001, 15001, 25001, 35001, 45001, 55001, 65001, 75001, 85001, 95001, 105001, 112121]

    dataEntry = open("archive/Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()

    # Traverse CSV file
    print("going through {:d} lines".format(starts[imageNum] - starts[imageNum - 1]))
    pcount = 0
    acount = 0
    for i in range(starts[imageNum-1], starts[imageNum]): #skip first line (column labels)
        line = lines[i].strip().split(",") #delimiter may need to be changed
        filename = line[0]
        disease = line[1].lower().strip()
        # Pick out images of diseaseType from dirName
        if (i % 1000) == 0:
            print(i)

        if ('pneumonia' in disease) == True:
            try:
                shutil.copy(dirName + '/images/' + filename, "nih_staged/pneumonia/")
                pcount = pcount + 1
            except:
                continue
        elif ('atelectasis' in disease):
            try:
                shutil.copy(dirName + '/images/' + filename, "nih_staged/atelectasis")
                acount = acount + 1
            except:
                continue
        else:
            try:
                shutil.copy(dirName + '/images/' + filename, "nih_staged/neither")
            except:
                continue
    return (pcount, acount)

def main():
    makeDirectories()
    pcount = 0
    acount = 0
    for i in range(1, 13, 1):
        (pCurr, aCurr) = stageImages("archive/images_00"+str(i), i)
        acount += aCurr
        pcount += pCurr
    print("There were a total of {:d} pneumonia files and {:d} atelectasis files")

if __name__ == "__main__":
    main()