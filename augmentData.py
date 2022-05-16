import os
from PIL import Image, ImageOps
from pathlib import Path

normal_dir = Path('./chest-xray-pneumonia/chest_xray/train/NORMAL')

for filename in os.scandir(normal_dir):
    img = Image.open(normal_dir + filename)
    img_mirror = ImageOps.mirrored(img)
    img_mirror.save(normal_dir + filename + '_mirrored')



