import sys
import os
from PIL import Image

#####################
#
# Purpose: Convert .jpeg files to .png
#
# Args: 1 - existing folder with .jpeg files (eg images/)
#       2 - new folder for .png files (eg. new_images/)
#
#####################


def converter(folder_jpeg, folder_png):
  # Check the 2 arguments
  try:
      assert type(folder_png) == str
      assert len(folder_png) > 0
      assert folder_jpeg[-1] == '/'
      assert os.path.isdir(folder_jpeg) == True
      assert type(folder_jpeg) == str
      assert len(folder_jpeg) > 0
      assert folder_png[-1] == '/'

  except :
    print('Both arguments must end in a /')
    return False

  # Check if the new folder exists, if not create it
  if not os.path.exists(folder_png):
    os.mkdir(folder_png)

  # Loop through the folder
  pattern = '.jpeg'
  files = os.listdir(folder_jpeg)
  print('Converting files now...')
  for file in files:
    # Convert .jpeg files to .png
    # Save the .png files in the new folder
    if pattern in file:
      img_JPEG = Image.open(folder_jpeg + file)
      img_JPEG.save(folder_png + file.split('.')[0] + '.png', 'png')
  return True

if __name__ == '__main__':
  # Grab the 2 arguments
  try:
    folder_jpeg = sys.argv[1]
    folder_png = sys.argv[2]

  except :
    print('Énter 2 arguments please, 1st being JPG dir and 2nd new PNG dir')
    sys.exit()

  converter(folder_jpeg, folder_png)