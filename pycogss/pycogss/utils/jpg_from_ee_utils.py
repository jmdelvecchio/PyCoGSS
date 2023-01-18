# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

from tkinter import filedialog, messagebox
import tkinter as tk

print("converting EE-derived tiles to jpg!")

root = tk.Tk()
root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of geotiffs")
geotiff_data_path = root.filename
print(geotiff_data_path)
root.withdraw()

geotiff_data_path = Path(geotiff_data_path)

jpg_dir = geotiff_data_path / 'jpgs_from_ee'
jpg_dir.mkdir(exist_ok=True)

root = tk.Tk()
root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of doodler assets")
doodler_asset_dir = root.filename
print(doodler_asset_dir)
root.withdraw()

tag=None # For now, not sure how to implement this with a GUI

if tag is not None:
    globber = "*" + tag + "*.tif"
else:
    globber = "*.tif"

#tif_list = glob.glob(globber)

for tif_pth in geotiff_data_path.glob(globber):
    print(tif_pth)
    options_list = [
    '-ot Byte',
    '-of JPEG',
    '-b 1',
    '-b 2',
    '-b 3'
    '-scale'
    ]       
    options_string = " ".join(options_list)     

    print((jpg_dir / f'{tif_pth.stem}.jpg').as_posix())

    gdal.Translate(
        (jpg_dir / f'{tif_pth.stem}.jpg').as_posix(),
        tif_pth.as_posix(),
        options=options_string
    )
# Now move to the Doodler asset folder
for pth in jpg_dir.glob('*_rgb*.jpg'):
    shutil.copy2(pth, os.path.join(doodler_asset_dir, pth.name)) #not sure why "/" isn't working, whoops
