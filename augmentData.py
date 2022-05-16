import os
from PIL import Image, ImageOps
from pathlib import Path

normal_dir = Path('./chest-xray-pneumonia/chest_xray/train/NORMAL')

for filename in os.listdir(normal_dir):
    img = Image.open(normal_dir / filename)
    img_mirror = ImageOps.mirror(img)
    img_mirror.save(normal_dir / ('_mirrored' + filename))



