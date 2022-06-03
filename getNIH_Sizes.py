from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import os

labels = {'Atelectasis': 11559, 'Cardiomegaly': 2776, 'Effusion': 13317, 'Infiltration': 19894, 'Mass': 5782, 'Nodule': 6331, 'Pneumonia': 1431, 'No Finding': 60361, 'Pneumothorax': 5302, 'Consolidation': 4667, 'Edema': 2303, 'Emphysema': 2516, 'Fibrosis': 1686, 'Pleural_Thickening': 3385, 'Hernia': 227}

keys = list(labels.keys())
keys[7] = "Normal"
input("Press enter to show plot")
plt.figure()
plt.title("Number of Files for Each Symptom")
plt.xlabel("Count")
plt.ylabel("Symptom")
plt.barh(keys, list(labels.values()),
            color='blue')
plt.show()

