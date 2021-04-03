import wand # pip3 install Wand, install libmagickwand-dev
from wand.image import Image
import glob
import os

convert_from = ".dds"
convert_to = ".png"
for file in glob.glob(f"*{convert_from}"):
    with Image(filename=file) as original:
        with original.convert('png') as converted:
            converted.save(filename=file.replace(convert_from, convert_to))
            print(file, f'to {convert_to}')
            os.remove(file) # WARNING THIS DELETES THE ORIGINAL FILE. comment it out if you dont want that.