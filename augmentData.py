import os
from PIL import Image, ImageOps
from pathlib import Path

normal_dir = Path('./chest-xray-pneumonia/chest_xray/train/NORMAL')
pneumonia_dir = Path('./chest-xray-pneumonia/chest_xray/train/PNEUMONIA')

for filename in os.listdir(normal_dir):
    img = Image.open(normal_dir / filename)
    img_mirror = ImageOps.mirror(img)
    img_mirror.save(normal_dir / ('_mirrored' + filename))

numNormal = len(os.listdir(normal_dir))
numPneumonia = len(os.listdir(pneumonia_dir))

count = 0
max = numPneumonia - numNormal

for filename in os.listdir(pneumonia_dir):
    if count == max:
        break
    os.remove(pneumonia_dir / filename)
    count += 1