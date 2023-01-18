from osgeo import gdal
import glob, os, shutil
import pathlib
from pathlib import Path 
from tkinter import filedialog, messagebox
import tkinter as tk
import numpy as np

def merge_and_tile(tag=None, tile=None):
    """
  Merges geotiffs delivered in strips/tiles and optionally retiles for Doodler

  tag = a string that might be a prefix or suffix that helps you gather the files you want to merge
  If you leave it blank it'll just merge everything in the directory
  tile = a single integer of the dimensions of the tile size u want
  """
    from osgeo import gdal
    import glob, os, shutil
    import pathlib
    from pathlib import Path 

    print("merge and tile!")

    geotiff_dir = Path('.')
    geotiff_dir.mkdir(exist_ok=True)
    merged_dir = Path('./merged')
    merged_dir.mkdir(exist_ok=True)

    dir_name = Path.cwd().name
    print(dir_name)

    if tag is not None:
        globber = "*" + tag + "*.tif"
    else:
        globber = "*.tif"

    tif_list = glob.glob(globber)      

    first_tif = tif_list[0]
    #print(str(first_tif))

    wkt_string = "gdalsrsinfo -o wkt " + first_tif + " > target.wkt"
    os.system(wkt_string)

    filename = dir_name + "_" + tag + ".tif"

    warp_string = "gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE -srcnodata 0 " + globber + " " + filename
    #warp_string = "gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE *_Visual_clip.tif " + dir_name + ".tif"
    #warp_string = "gdalwarp -overwrite -multi -wm 80% -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE " + dir_name + ".tif *_Visual_clip.tif"
    os.system(warp_string)
    #https://gis.stackexchange.com/questions/414915/fastest-possible-use-of-gdal-to-merge-reproject-convert

    #tile_string = "gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co "TILED=YES" -co "COMPRESS=JPEG" -targetDir image_tiles vc_merged.tif"
    #os.system(tile_string)

    print("Created ", filename)

   

    if type(tile) == int:
        print("Making jpg titles")
        jpg_dir = Path('./jpgs')
        jpg_dir.mkdir(exist_ok=True)
        retiled_dir = Path('./retiled')
        retiled_dir.mkdir(exist_ok=True)
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
    else:
        print("Skipping making tiled jpgs")


    shutil.move("./"+filename, merged_dir / filename)

def jpg_from_ee(tag=None):


    """
  converting EE-derived tiles to jpg
  """
    from osgeo import gdal
    import glob, os, shutil
    import pathlib
    from pathlib import Path 

    print("converting EE-derived tiles to jpg!")

    geotiff_dir = Path('.')
    geotiff_dir.mkdir(exist_ok=True)
    jpg_dir = Path('./jpgs_from_ee')
    jpg_dir.mkdir(exist_ok=True)

    if tag is not None:
        globber = "*" + tag + "*.tif"
    else:
        globber = "*.tif"

    #tif_list = glob.glob(globber)



    for tif_pth in geotiff_dir.glob(globber):
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

def labels_to_tif():


    """
  matches original tif-to-jpeg xml files with labels generated in Doodle
  you gotta run the gen_images_and_labels.py in doodler after you get results from doodler
  """
    from osgeo import gdal
    import glob, os, shutil
    import pathlib
    from pathlib import Path 
    from tkinter import filedialog, messagebox
    import tkinter as tk
    # from tkinter import *

    print("converting labels to tiffs!")

    # Dialog is not great for CLI but I am too lazy rn
    # Matches Doodleverse anyway

    root = tk.Tk()
    root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of LABEL files")
    label_data_path = root.filename
    print(label_data_path)
    root.withdraw()

    label_data_path = Path(label_data_path)

    new_tif_dir = Path(f'{label_data_path.parents[0]}/converted_tiffs')
    new_tif_dir.mkdir(exist_ok=True)
    print("Created directory for converted tiffs at ", new_tif_dir.as_posix())

    for file in label_data_path.glob("*_label.jpg"):
        shutil.copy(file.as_posix(), (new_tif_dir).as_posix())


    # (
    #     [shutil.copy("./"+file,
    #      new_tif_dir / file)
    #      for file in label_data_path.glob("*_label.jpg")]
    # )

    # shutil.move("./"+filename, merged_dir / filename)
    
    print("Copied labels to ", new_tif_dir.as_posix())

    root = tk.Tk()
    root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of CONVERTED JPEG files")
    xml_path = root.filename
    print(xml_path)
    root.withdraw()
    
    xml_path = Path(xml_path)

    for xml in xml_path.glob('*.xml'):
        print("Trying to match ", xml)
        file = xml.stem.split('.')[0]
        for file_match in label_data_path.glob(f'{file}*_label.jpg'):
            print("Match found with ", file_match)
            shutil.copy(xml, new_tif_dir / f'{file_match}.aux.xml')
        # file_match = (label_data_path.glob(f'{file}*_label.jpg'))
        # shutil.copy(xml, new_tif_dir / f'{file_match}.aux.xml' )

            options_list = [
            '-of GTiff',
            ]  

            options_string = " ".join(options_list)  

            tifname = file_match.stem.split('.')[0]

            gdal.Translate(
                (new_tif_dir / f'{tifname}.tif').as_posix(),
                file_match.as_posix(),
                options=options_string
            )
            
    
    print("Converted label jpegs to tiffs!")

def labels_by_hybas():
    """
groups by HYBAS ID 
     """
    from osgeo import gdal
    import glob, os, shutil
    import pathlib
    from pathlib import Path 
    import numpy as np

    root = tk.Tk()
    root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of LABEL TIFF files")
    tif_dir = Path(root.filename)
   
    os.chdir(tif_dir.as_posix())
    print("Changed working directory to", os.getcwd())
    root.withdraw()

    ids = np.unique(
        np.array([
            file.stem[:10]
            for file in tif_dir.glob('*.tif')
        ])
    )

    print("Number of files you should see: ", str(len(ids)))

    for id in ids:
        files = [path.as_posix() for path in tif_dir.glob(f'{id}*.tif')]

        wkt_string = f"gdalsrsinfo -o wkt {files[0]} > target.wkt"
        os.system(wkt_string)

        filename = f"{id}_labels.tif"

        # Yo what is no data in labels 

        warp_string = f"gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE {id}*.tif {filename}"
        print(warp_string)
        #warp_string = "gdalwarp -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE *_Visual_clip.tif " + dir_name + ".tif"
        #warp_string = "gdalwarp -overwrite -multi -wm 80% -t_srs target.wkt -co TILED=YES -co BIGTIFF=YES -co COMPRESS=DEFLATE " + dir_name + ".tif *_Visual_clip.tif"
        os.system(warp_string)
        #https://gis.stackexchange.com/questions/414915/fastest-possible-use-of-gdal-to-merge-reproject-convert

        #tile_string = "gdal_retile.py -v -r bilinear -levels 1 -ps 2048 2048 -co "TILED=YES" -co "COMPRESS=JPEG" -targetDir image_tiles vc_merged.tif"
        #os.system(tile_string)

        print("Created ", filename)

# Somehow this is garbage:

# def to_polar():
#     """
# Google doesn't let you export shapefiles with a crs
# Not strictly a tiff
#      """
#     root = tk.Tk()
#     root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory of EARTH ENGINE SHAPES")
#     shp_dir = Path(root.filename)
   
#     os.chdir(shp_dir.as_posix())
#     print("Changed working directory to ", os.getcwd())
#     root.withdraw()

#     for shp in glob.glob('*.shp'):
#         shape_string = f'ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:5936 -s_srs EPSG:4326 polar_{shp} {shp}'
#         os.system(shape_string)

def cut_labels():
    """
Google doesn't let you export shapefiles with a crs
Not strictly a tiff
     """
    root = tk.Tk()
    root.filename =  filedialog.askdirectory(initialdir = os.getcwd(),title = "Select directory containing SHAPES AND TIFS")
    shp_dir = Path(root.filename)
   
    os.chdir(shp_dir.as_posix())
    print("Changed working directory to ", os.getcwd())
    root.withdraw()

    ids = np.unique(
        np.array([
            file.stem[:10]
            for file in shp_dir.glob('*.tif')
        ])
    )

    #-crop_to_cutline  -t_srs EPSG:5936 -s_srs EPSG:5936

    for id in ids:
        
        # print(os.system(f'ogrinfo -ro -so -al polar_{id}.shp'))
        # print(os.system(f'gdalinfo {id}_labels.tif'))

        # repro_string = f'gdalwarp -of GTiff -t_srs EPSG:5936 {id}_labels.tif {id}_polar_labels.tif'
        # os.system(repro_string)

        cutline_string = (
            f'gdalwarp -of GTiff -cutline polar_{id}.shp -dstnodata 9999 {id}_labels.tif {id}_cropped_labels.tif'
            )
        os.system(cutline_string)
        # gdal.Warp(f'{id}_cropped_labels.tif',
        #            f'{id}_labels.tif',
        #            cutlineDSName=f'polar_{id}.shp',
        #            cropToCutline=True)
        print(f'Removing nodata parts of {id}')