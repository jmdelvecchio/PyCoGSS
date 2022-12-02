from glob import glob 
from imageio import imread, imwrite
import numpy as np
import matplotlib.pyplot as plt
import os, shutil
# from pathlib import Path 

# folder of labels
inroot = os.getcwd()+'/labels/'
# cwd / 'labels'
# inroot.mkdri(exist_o)
# image_outroot = Path('./new_images/')
# image_outroot.mkdir(exist_ok=True)
# outroot = Path('./new_labels')
# outroot.mkdir(exist_ok=True)

# new folder of class balanced labels
outroot = os.getcwd()+'/new_labels/'

image_inroot = os.getcwd()+'/images/'
image_outroot = os.getcwd()+'/new_images/'

os.makedirs(image_outroot, exist_ok=True)
os.makedirs(outroot, exist_ok=True)


## read labels and copy them if they have more than 1 class
files = glob(inroot+'*.jpg')

print("{} label files".format(len(files)))

for file in files:
    dat = imread(file)

    if len(np.unique(dat))==1:
        print("Skipping {} with only one class".format(file))

    else:
        print("{} unique classes".format(len(np.unique(dat))))
        imwrite(file.replace(inroot,outroot), dat, quality=100, chroma_subsampling=False, check_contrast=False)



files = glob(image_inroot+'*.jpg')

label_files = glob(outroot+'*.jpg')

label_files = [l.split(os.sep)[-1] for l in label_files]

print("{} class balanced label files".format(len(label_files)))


for file in files:
    f = file.split(os.sep)[-1]
    if f.split('.jpg')[0]+'_label.jpg' in label_files:
        shutil.copyfile(file, image_outroot+f)