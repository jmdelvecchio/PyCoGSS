# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

geotiff_dir = Path('.')
jpg_dir = Path('./jpgs')
jpg_dir.mkdir(exist_ok=True)
gym_dir = Path('//dartfs/rc/lab/V/VecchioJ/arctic_image_segmentation/joanmarie_dev/seg_gym_dev')

for tif_pth in geotiff_dir.glob('*_rgb*.tif'):
    options_list = [
        '-ot Byte',
        '-of JPEG',
        '-b 1',
        '-b 2',
        '-b 3'
        '-scale'
    ]           
    
    options_string = " ".join(options_list)

    gdal.Translate(
        (jpg_dir / f'{tif_pth.stem}.jpg').as_posix(),
        tif_pth.as_posix(),
        options=options_string
    )
    
    #https://stackoverflow.com/questions/50207292/how-to-convert-geotiff-to-jpg-in-python-or-java

for pth in jpg_dir.glob('*_rgb*.jpg'):
    # toPredict
    dir = gym_dir / 'toPredict'
    dir.mkdir(exist_ok=True)
    shutil.copy2(pth, dir / pth.name)
    print("Sending unlabeled files to: " + str(dir))