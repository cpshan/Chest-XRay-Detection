from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import os

smallDir = Path('./chest-xray-pneumonia/chest_xray/train/')

pDir = smallDir / "PNEUMONIA"
nDir = smallDir / "NORMAL"

print("Pneumonia Dataset:")
print("there are {:d} pneumonia files".format(len(os.listdir(pDir))))
print("there are {:d} normal files".format(len(os.listdir(nDir))))

input("Press enter to show plot")
plt.figure()
plt.title("Number of Files for Each Symptom")
plt.xlabel("Symptom")
plt.ylabel("Count")
plt.bar(["Pneumonia", "Normal"], [len(os.listdir(pDir)), len(os.listdir(nDir))],
            color='green', width=0.4)
plt.show()
print()

print("Infiltration Dataset:")
infilDir = Path('./infil_staged')

iDir = infilDir / "infiltration"
nDir = infilDir / "normal"

testDir = Path('./infil_test')

itestDir = testDir / 'infiltration'
ntestDir = testDir / 'normal'

print("there are {:d} infiltration files".format(len(os.listdir(iDir))))
print("there are {:d} normal files".format(len(os.listdir(nDir))))
print("there are {:d} infiltration test files".format(len(os.listdir(itestDir))))
print("there are {:d} normal test files".format(len(os.listdir(ntestDir))))

input("Press enter to show plot")
plt.figure()
plt.title("Number of Files for Each Symptom")
plt.xlabel("Symptom")
plt.ylabel("Count")
plt.bar(["Infiltration", "Normal"], [len(os.listdir(iDir)), len(os.listdir(nDir))],
            color='green', width=0.4)
plt.show()
print()

testDir = Path("./nih_staged/")

none = testDir / 'neither'
infiltration = testDir / 'infiltration'
atelectasis = testDir / 'atelectasis'

print("NIH Dataset:")
print("there are {:d} normal".format(len(os.listdir(none))))
print("there are {:d} infiltration".format(len(os.listdir(infiltration))))
print("there are {:d} atelectasis".format(len(os.listdir(atelectasis))))

input("Press enter to show plot")
plt.figure()
plt.title("Number of Files for Each Symptom")
plt.xlabel("Symptom")
plt.ylabel("Count")
plt.bar(["Atelectasis", "Infiltration", "Normal"], 
            [len(os.listdir(atelectasis)), len(os.listdir(infiltration)), len(os.listdir(none))],
            color='green', width=0.4)
plt.show()
print()