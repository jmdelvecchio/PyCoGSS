# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

#geotiff_dir = Path('./geotiffs')
geotiff_dir = Path('.')
jpg_dir = Path('./jpgs')
jpg_dir.mkdir(exist_ok=True)


if os.getlogin( ) == 'f0055wb':
    doodler_asset_dir = Path('//dartfs-hpc/rc/home/b/f0055wb/dash_doodler/assets')
elif os.getlogin( ) == 'f005dv1':
    doodler_asset_dir = Path('//dartfs-hpc/rc/home/1/f005dv1/dash_doodler_dev/dash_doodler/assets')
else:
    print("WHo are you, go set your assets path")
print("Sending files to: " + str(doodler_asset_dir))

for tif_pth in geotiff_dir.glob('*ndwi*.tif'):
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
    
# Now move to the Doodler asset folder
# for pth in jpg_dir.glob('*ndwi*.jpg'):
#     shutil.copy2(pth, doodler_asset_dir / pth.name)
