from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

from tkinter import filedialog, messagebox
import tkinter as tk

print("converting Planet strips to jpg!")

tile = 1024 # Need to revisit implementation with GUI

root = tk.Tk()
root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of geotiffs")
geotiff_data_path = root.filename
print(geotiff_data_path)
root.withdraw()

geotiff_data_path = Path(geotiff_data_path)

retiled_dir = geotiff_data_path / 'retiled'
retiled_dir.mkdir(exist_ok=True)

jpg_dir = geotiff_data_path / 'jpgs_from_planet'
jpg_dir.mkdir(exist_ok=True)


root = tk.Tk()
root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of doodler assets")
doodler_asset_dir = root.filename
print(doodler_asset_dir)
root.withdraw()

tag='Visual' # Need to revisit implementation with GUI

if tag is not None:
    globber = "*" + tag + "*.tif"
else:
    globber = "*.tif"

# tif_list = geotiff_data_path.glob(globber)

tif_list = [file.as_posix() for file in geotiff_data_path.glob(globber)]

# print(tif_list)

first_tif = tif_list[0]
#print(str(first_tif))

target_wkt_string = geotiff_data_path.as_posix() + "/target.wkt"

wkt_string = "gdalsrsinfo -o wkt " + first_tif + " > " + target_wkt_string
# print(wkt_string)
os.system(wkt_string)

# filename = geotiff_data_path.name + "_" + tag + ".tif"

filename= (geotiff_data_path / Path(first_tif).stem[0:8]).as_posix() + ".tif"
print('Your merged image is named after the imagery date: ', filename)

globber_path = geotiff_data_path.as_posix() + "/" + globber

warp_string = "gdalwarp -t_srs " + target_wkt_string + " -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE -srcnodata 0 " + globber_path + " " + filename
#warp_string = "gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE *_Visual_clip.tif " + dir_name + ".tif"
#warp_string = "gdalwarp -overwrite -multi -wm 80% -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE " + dir_name + ".tif *_Visual_clip.tif"
# print(warp_string)
os.system(warp_string)
#https://gis.stackexchange.com/questions/414915/fastest-possible-use-of-gdal-to-merge-reproject-convert

#tile_string = "gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co "TILED=YES" -co "COMPRESS=JPEG" -targetDir image_tiles vc_merged.tif"
#os.system(tile_string)

print("Created ", filename)

    #segmentation_dir = Path('//dartfs/rc/lab/V/VecchioJ/arctic_image_segmentation/images_to_segment')

tiled = "TILED=YES" 
compress = "COMPRESS=JPEG"
#os.system("gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co " + tiled + " -co " + compress + " -targetDir " + jpg_dir.as_posix() + " vc_merged.tif")
os.system(
    "gdal_retile.py -v -r bilinear -ps " 
    + str(int(tile)) + " " + str(int(tile)) 
    + " -co " + tiled + " -co " + compress + " -targetDir " + retiled_dir.as_posix() 
    + " -tileIndex vc_merged.shp -csv vc_merged.csv " + filename
    )

###

for tif_pth in retiled_dir.glob('*.tif'):
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
    # gdal.Translate(
    #     (jpg_dir / f'{tif_pth.stem}.jpg').as_posix(),
    #     tif_pth.as_posix(),
    #     options=options_string
    # )
    
    #https://stackoverflow.com/questions/50207292/how-to-convert-geotiff-to-jpg-in-python-or-java
    
# Now move to the folder where we'll load in images to be segmented with Gym
# print("Sending files to: " + str(segmentation_dir))
# for pth in jpg_dir.glob('*.jpg'):
#     shutil.copy2(pth, segmentation_dir / pth.name)

for pth in jpg_dir.glob('*.jpg'):
    shutil.copy2(pth, os.path.join(doodler_asset_dir, pth.name)) #not sure why "/" isn't working, whoops
























# # The two different quotes are necessary to get quotes as the variables
# nodata_string = '"0 0 0"'
# vrt_string = "gdalbuildvrt -srcnodata " + str(nodata_string) + " vc_merged.vrt *_Visual_clip.tif"
# os.system(vrt_string)

# translate_string = "gdal_translate -of GTiff vc_merged.vrt " + hybas_id + ".tif"
# os.system(translate_string)

# #tile_string = "gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co "TILED=YES" -co "COMPRESS=JPEG" -targetDir image_tiles vc_merged.tif"
# #os.system(tile_string)

# tiled = "TILED=YES" 
# compress = "COMPRESS=JPEG"
# #os.system("gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co " + tiled + " -co " + compress + " -targetDir " + jpg_dir.as_posix() + " vc_merged.tif")
# os.system("gdal_retile.py -v -r bilinear -ps 2048 2048 -co " + tiled + " -co " + compress + " -targetDir " + geotiff_dir.as_posix() + " -tileIndex vc_merged.shp -csv vc_merged.csv " + hybas_id + ".tif")

# ###

# if os.getlogin( ) == 'f0055wb':
#     doodler_asset_dir = Path('//dartfs-hpc/rc/home/b/f0055wb/dash_doodler/assets')
# elif os.getlogin( ) == 'f005dv1':
#     doodler_asset_dir = Path('//dartfs-hpc/rc/home/1/f005dv1/dash_doodler_dev/dash_doodler/assets')
# else:
#     print("WHo are you, go set your assets path")
# print("Sending files to: " + str(doodler_asset_dir))

# for tif_pth in geotiff_dir.glob('*.tif'):
#     options_list = [
#         '-ot Byte',
#         '-of JPEG',
#         '-b 1',
#         '-b 2',
#         '-b 3'
#         '-scale'
#     ]           
    
#     options_string = " ".join(options_list)

#     gdal.Translate(
#         (jpg_dir / f'{tif_pth.stem}.jpg').as_posix(),
#         tif_pth.as_posix(),
#         options=options_string
#     )
    
#     #https://stackoverflow.com/questions/50207292/how-to-convert-geotiff-to-jpg-in-python-or-java
    
# # Now move to the Doodler asset folder
# for pth in jpg_dir.glob('*.jpg'):
#     shutil.copy2(pth, doodler_asset_dir / pth.name)
