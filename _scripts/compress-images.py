'''
pip install pillow
pip install exif

Notes:

Some portrait-oriented images will come out flipped.
The fix would involve looking at EXIF data and adusting.
Unfortunately, EXIF is not always available in the jpgs
so I will spend a lot less time flipping back a few images
in the file manager than I would writing a fix.

'''

import os
from os import listdir
from os.path import isfile, join
import math
from pathlib import Path

from PIL import ExifTags
from PIL import Image

home = str(Path.home())
# UNIX
read_directory = (home + r'/Git/exip/_images/original')
write_directory = (home + r'/Git/exip/_images/compressed')

already_compressed_files = [f for f in listdir(write_directory) if isfile(join(write_directory, f))]	

for filename in os.listdir(read_directory):
    if (filename.endswith('.jpg') or filename.endswith('.png')) and (filename not in already_compressed_files):
        # Gather path info
        if os.name == 'nt':
            image_path = str(read_directory + '\\' + '\\' + filename) # Weird Windows file path garbage
        else: 
            image_path = str(read_directory + '/' + filename)
        print(image_path)
        img = Image.open(image_path)

        # Get and fix size
        width_pixels = img.size[0]
        height_pixels = img.size[1]
        adjusted_width_pixels = math.ceil((int(img.size[0]) / 2))
        adjusted_height_pixels = math.ceil((int(img.size[1]) / 2))
        img = img.resize((adjusted_width_pixels, adjusted_height_pixels), Image.ANTIALIAS)
    
        # Write new compressed image
        if os.name == 'nt':
            write_path = str(write_directory + '\\' + '\\' + filename) # Weird Windows file path garbage
        else: 
            write_path = str(write_directory + '/' + filename)
        print('writing image...')
        print(filename)
        img.save(write_path, optimize=True, quality=75)
    else:
        continue

