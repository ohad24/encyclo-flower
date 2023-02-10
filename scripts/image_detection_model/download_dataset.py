import pandas as pd
import os, sys
import requests

csv_file = sys.argv[1]
df = pd.read_csv(csv_file, header=0)

for i in df.groupby('scientificname'):
    exists_dir_name = "/data/dataset/" + i[0]
    print(exists_dir_name)
    dir_name = "/data/dataset/" + i[0]
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    print(i[0])
    count = 0
    for link in (i[1]["identifier"]):
        img_name = exists_dir_name + "/" + str(count) + ".jpg"
        save_img_name = dir_name + "/" + str(count) + ".jpg"
        if not os.path.exists(img_name):
          try:
            img_data = requests.get(link).content
            with open(save_img_name, 'wb') as handler:
                handler.write(img_data)
          except:
            pass
        count += 1
        if count > 500:
            break
