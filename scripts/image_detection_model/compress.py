import cv2
import imutils
import os

root = "/data/dataset/"
save_root = "/data/data/"
count = 0
for path, subdirs, files in os.walk(root):
    for name in files:
      file = os.path.join(path, name)
      plant_name = path.split("/")[-1]
      # if plant_name == 'Daucus carota':
      save_path = os.path.join(save_root, plant_name)
      if not os.path.isdir(save_path):
        os.mkdir(save_path)
        print(plant_name)
      save_dir = os.path.join(save_path, name)
      try:
        if not os.path.isfile(save_dir):
          img = cv2.imread(file)
          img = imutils.resize(img, width=224)
          cv2.imwrite(save_dir, img)
      except:
        print(os.path.join(path, name))
