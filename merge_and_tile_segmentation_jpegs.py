
from osgeo import gdal
import glob, os, shutil
import pathlib
from pathlib import Path 

geotiff_dir = Path('./geotiffs')
geotiff_dir.mkdir(exist_ok=True)
jpg_dir = Path('./jpgs')
jpg_dir.mkdir(exist_ok=True)
segmentation_dir = Path('//dartfs/rc/lab/V/VecchioJ/arctic_image_segmentation/images_to_segment')

hybas_id = Path.cwd().name
print(hybas_id)

# # The two different quotes are necessary to get quotes as the variables
# nodata_string = '"0 0 0"'
# vrt_string = "gdalbuildvrt -srcnodata " + str(nodata_string) + " vc_merged.vrt *_Visual_clip.tif"
# os.system(vrt_string)

# translate_string = "gdal_translate -of GTiff vc_merged.vrt " + hybas_id + ".tif"
# os.system(translate_string)

# Globber is what you want to use to gather (glob) the files for merging e.g. '*_rgb*.tif'
globber = '*_Visual_clip.tif'

tif_list = glob.glob(globber)

first_tif = tif_list[0]
#print(str(first_tif))

wkt_string = "gdalsrsinfo -o wkt " + first_tif + " > target.wkt"
os.system(wkt_string)

warp_string = "gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE " + globber + " " + hybas_id + ".tif"
#warp_string = "gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE *_Visual_clip.tif " + hybas_id + ".tif"
#warp_string = "gdalwarp -overwrite -multi -wm 80% -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE " + hybas_id + ".tif *_Visual_clip.tif"
os.system(warp_string)
#https://gis.stackexchange.com/questions/414915/fastest-possible-use-of-gdal-to-merge-reproject-convert

#tile_string = "gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co "TILED=YES" -co "COMPRESS=JPEG" -targetDir image_tiles vc_merged.tif"
#os.system(tile_string)

tiled = "TILED=YES" 
compress = "COMPRESS=JPEG"
#os.system("gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co " + tiled + " -co " + compress + " -targetDir " + jpg_dir.as_posix() + " vc_merged.tif")
os.system("gdal_retile.py -v -r bilinear -ps 2048 2048 -co " + tiled + " -co " + compress + " -targetDir " + geotiff_dir.as_posix() + " -tileIndex vc_merged.shp -csv vc_merged.csv " + hybas_id + ".tif")

###




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
    
# Now move to the folder where we'll load in images to be segmented with Gym
print("Sending files to: " + str(segmentation_dir))
for pth in jpg_dir.glob('*.jpg'):
    shutil.copy2(pth, segmentation_dir / pth.name)
