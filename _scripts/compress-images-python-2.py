import os
from os import listdir
from os.path import isfile, join, expanduser
import math
from PIL import Image

# Use expanduser instead of Path.home() for Python 2.7
home = expanduser("~")

# UNIX-style paths (will be converted for Windows automatically)
read_directory = os.path.join(home, 'Git', 'exip', '_images', 'original')
write_directory = os.path.join(home, 'Git', 'exip', '_images', 'compressed')

# Create output directory if it doesn't exist
if not os.path.exists(write_directory):
    os.makedirs(write_directory)

# Get list of already compressed files
already_compressed_files = [f for f in listdir(write_directory) if isfile(join(write_directory, f))]

for filename in os.listdir(read_directory):
    if (filename.endswith('.jpg') or filename.endswith('.png')) and (filename not in already_compressed_files):
        # Use os.path.join for reliable path handling
        image_path = os.path.join(read_directory, filename)
        write_path = os.path.join(write_directory, filename)
        
        print("Processing: %s" % image_path)
        
        try:
            img = Image.open(image_path)
            
            # Get and fix size
            width_pixels = img.size[0]
            height_pixels = img.size[1]
            adjusted_width_pixels = int(math.ceil(float(width_pixels) / 2))
            adjusted_height_pixels = int(math.ceil(float(height_pixels) / 2))
            
            # Use ANTIALIAS since we're in Python 2.7
            img = img.resize((adjusted_width_pixels, adjusted_height_pixels), Image.ANTIALIAS)
            
            print('Writing image: %s' % filename)
            img.save(write_path, optimize=True, quality=75)
            
        except Exception as e:
            print("Error processing %s: %s" % (filename, str(e)))
            continue
        finally:
            if 'img' in locals():
                img.close()
    else:
        continue

print("Compression complete!")
