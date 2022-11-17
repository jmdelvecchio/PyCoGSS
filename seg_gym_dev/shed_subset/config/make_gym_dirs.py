# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

jpg_dir = Path('./jpgs')
jpg_dir.mkdir(exist_ok=True)


if os.getlogin( ) == 'f0055wb':
    doodler_asset_dir = Path('//dartfs-hpc/rc/home/b/f0055wb/dash_doodler/assets')
elif os.getlogin( ) == 'f005dv1':
    doodler_asset_dir = Path('//dartfs-hpc/rc/home/1/f005dv1/dash_doodler_dev/dash_doodler/assets')
    doodler_results_dir = Path('//dartfs-hpc/rc/home/1/f005dv1/dash_doodler_dev/dash_doodler/results')
    gym_dir = Path('//dartfs/rc/lab/V/VecchioJ/arctic_image_segmentation/joanmarie_dev/seg_gym_dev')
else:
    print("WHo are you, go set your assets path")
    
imdir = gym_dir / 'images'
imdir.mkdir(exist_ok=True)
print("Sending image files to: " + str(imdir))  

for pth in doodler_asset_dir.glob('*_rgb*.jpg'):
    # images
    shutil.copy2(pth, imdir / pth.name)

ladir = gym_dir / 'labels'
ladir.mkdir(exist_ok=True)
print("Sending label files to: " + str(ladir))
for pth in doodler_results_dir.rglob('*_label*.png'):
    # labels
    shutil.copy2(pth, ladir / pth.name)

npzdir = gym_dir / 'npzForModel'
npzdir.mkdir(exist_ok=True)
print("Sending npz files to: " + str(npzdir))
for pth in doodler_results_dir.rglob('*.npz'):
    # npz
    shutil.copy2(pth, npzdir / pth.name)


