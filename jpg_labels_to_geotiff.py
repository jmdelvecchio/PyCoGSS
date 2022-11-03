from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

original_geotiff_dir = Path('./geotiffs')
label_dir = Path('./jpgs')

label_geotiff_dir = Path('./label_geotiff_dir')
label_geotiff_dir.mkdir(exist_ok=True)

# Get list of oginal geotiffs from geotiff file name prefixes

# Get spatial references of original geotiffs

# Project jpegs with corresponding crs
gdal_translate -of GTiff in.jpeg tif_out.tif

for tif_pth in geotiff_dir.glob('*.tif'):
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
for pth in jpg_dir.glob('*.jpg'):
    shutil.copy2(pth, doodler_asset_dir / pth.name)