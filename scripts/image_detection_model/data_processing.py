import os

root = "/data/data/"
count = 0
for path, subdirs, files in os.walk(root):
    for name in files:
      # if (name.split(".")[-1]) != 'jpg':
      print(name)
      if (os.stat(os.path.join(path, name)).st_size==0) == True:
        os.remove(os.path.join(path, name))
        print(os.path.join(path, name))
        count += 1
print(count)
