import os
import shutil
from PIL import Image, ImageOps
from pathlib import Path
import time

def makeDirectories():
    try:
        os.mkdir("nih_staged")
    except FileExistsError:
        print("nih_staged directory already created")

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

    try:
        os.mkdir("nih_test/")
    except FileExistsError:
        print("test folder alrealy created")
    
    try:
        os.mkdir("nih_test/pneumonia")
    except FileExistsError:
        print("pneumonia test directory already created")   
    
    try:
        os.mkdir("nih_test/atelectasis")
    except FileExistsError:
        print("atelectasis test directory already created")

    try:
        os.mkdir("nih_test/neither")
    except FileExistsError:
        print("neither/ test directory already created")

def stageImages(dirName, imageNum, nCount):
    #Goes to 112121, but are saving the last few hundred for testing
    starts = [0, 5001, 15001, 25001, 35001, 45001, 55001, 65001, 75001, 85001, 95001, 105001, 109407]

    dataEntry = open("archive/Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()

    # Traverse CSV file
    print("going through {:d} lines ({:d} - {:d})".format(starts[imageNum] - starts[imageNum - 1],
        starts[imageNum - 1], starts[imageNum]))
    pcount = 0
    acount = 0
    for i in range(starts[imageNum-1], starts[imageNum]): #skip first line (column labels)
        line = lines[i].strip().split(",") #delimiter may need to be changed
        filename = line[0]
        disease = line[1].lower().strip()
        # Pick out images of diseaseType from dirName

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
        elif (("no finding" in disease) and (nCount < 11000)):
            try:
                shutil.copy(dirName + '/images/' + filename, "nih_staged/neither")
                nCount += 1
            except:
                continue
    return (pcount, acount, nCount)

def addMorePneumonia():
    #Get path from chest-xray-pneumonia dataset
    #Directory needs to be installed, unzipped, and named chest-xray-pneumonia
    pathToCpy = "chest-xray-pneumonia/chest_xray/train/PNEUMONIA"
    files = os.listdir(pathToCpy)
    #copy each file to the nih_staged directory
    for pfile in files:
        filePath = pathToCpy + '/' + pfile
        shutil.copy(filePath, "nih_staged/pneumonia")
        
def augmentData():
    pDir = Path("nih_staged/pneumonia")
    i = 0
    dirLen = len(os.listdir(pDir))
    print("Augmenting pneumonia")
    #Mirror all the pneumonia images
    for fileName in os.listdir(pDir):
        if (i % 1000) == 0:
            print("{:d} / {:d}".format(i, dirLen))
        img = Image.open(pDir / fileName)
        img_mirror = ImageOps.mirror(img)
        img_mirror.save(pDir / ('mirrored' + fileName)) 
        i += 1

def buildTestDir():
    #Each test directory is going to have 300 images
    #Start with normal images and atelectasis images
    dirName = "archive/images_012"
    dataEntry = open("archive/Data_Entry_2017.csv", 'r')
    lines = dataEntry.readlines()
    starts = [109407, 112121]
    noneCount = 0
    atelectasisCount = 0
    
    for i in range(starts[0], starts[1]):
        line = lines[i].lower().split(",")
        filename = line[0]
        disease = line[1].lower().strip()
        
        if (atelectasisCount == 300) and (noneCount == 300):
            break
        
        if ("atelectasis" in disease) and (atelectasisCount < 300):
            try:
                shutil.copy(dirName + '/images/' + filename, "nih_test/atelectasis")
                atelectasisCount = atelectasisCount + 1
            except:
                continue

        elif ("pneumonia" not in disease) and (noneCount < 300):
            try:
                shutil.copy(dirName + '/images/' + filename, "nih_test/neither")
                noneCount = noneCount + 1
            except:
                continue   
    
    dirName = "chest-xray-pneumonia/chest_xray/test/PNEUMONIA"
    count = 0
    for fileName in os.listdir(dirName):
        if count == 300:
            break

        try:
            shutil.copy(dirName + '/' + fileName, "nih_test/pneumonia")
            count = count + 1
        except:
            continue


def main():
    makeDirectories()
    pcount = 0
    acount = 0
    nCount = 0
    print("About to go through roughly 112,000 lines")
    start = time.time()
    for i in range(1, 13, 1):
        # The nih chest xray dataset was installed and unzipped called archive/
        # If yours is different, change the path name here
        (pCurr, aCurr, nCount) = stageImages("archive/images_0{:02d}".format(i), i, nCount)
        acount += aCurr
        pcount += pCurr
    
    end = time.time()
    print("After {:.2f} minutes, there are a total of {:d} pneumonia files and {:d} atelectasis files".format(
        (end - start) / 60, pcount, acount))

    print("Adding more pneumonia files")
    start = time.time()
    addMorePneumonia()
    end = time.time()
    print("After {:.2f} minutes, there are now a total of {:d} pnuemonia files and {:d} atelectasis files".format(
        (end - start) / 60, len(os.listdir("nih_staged/pneumonia")), len(os.listdir("nih_staged/atelectasis"))
    ))

    print("Augmenting data")
    start = time.time()
    augmentData()
    end = time.time()
    print("After augmentation for {:.2f} minutes, there are now a total of {:d} pnuemonia files and {:d} atelectasis files".format(
        (end - start) / 60, len(os.listdir("nih_staged/pneumonia")), len(os.listdir("nih_staged/atelectasis"))
    ))

    buildTestDir()
    print("After building the test directory, there are:")
    print("\t{:d} neither test files".format(len(os.listdir("nih_test/neither"))))
    print("\t{:d} pneumonia test files".format(len(os.listdir("nih_test/pneumonia"))))
    print("\t{:d} atelectasis test files".format(len(os.listdir("nih_test/atelectasis"))))

    print("Finally, there are {:d} neither train files".format(len(os.listdir("nih_staged/neither"))))


if __name__ == "__main__":
    main()