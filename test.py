from pathlib import Path
import os

testDir = Path("./nih_staged/")

otherDir = Path("./chest-xray-pneumonia/chest_xray/test/")

otherP = otherDir / 'PNEUMONIA'

none = testDir / 'neither'
pneumonia = testDir / 'pneumonia'
atelectasis = testDir / 'atelectasis'

print("there are {:d} normal".format(len(os.listdir(none))))
print("there are {:d} pneumonia".format(len(os.listdir(pneumonia))))
print("there are {:d} atelectasis".format(len(os.listdir(atelectasis))))