from osgeo import gdal
import os
import glob, os, shutil

from pathlib import Path 

original_geotiff_dir = Path('./geotiffs')
label_dir = Path('./jpgs')

label_geotiff_dir = Path('./label_geotiff_dir')
label_geotiff_dir.mkdir(exist_ok=True)

# Get list of oginal geotiffs from geotiff file name prefixes

       data = dict()
        with load(anno_file, allow_pickle=True) as dat:
            #create a dictionary of variables
            #automatically converted the keys in the npz file, dat to keys in the dictionary, data, then assigns the arrays to data
            for k in dat.keys():
                data[k] = dat[k]
            del dat

        #Make the original images as jpg
        if 'orig_image' in data.keys():
            im = np.squeeze(data['orig_image'].astype('uint8'))[:,:,:3]
        else:
            if data['image'].shape[-1]==4:
                im=np.squeeze(data['image'].astype('uint8'))[:,:,:-1]
                band4=np.squeeze(data['image'].astype('uint8'))[:,:,-1]
            else:
                im = np.squeeze(data['image'].astype('uint8'))[:,:,:3]

        io.imsave(anno_file.replace('.npz','.jpg'),
                  im, quality=100, chroma_subsampling=False)

        if 'band4' in locals():
                io.imsave(anno_file.replace('.npz','_band4.jpg'),
                          band4, quality=100, chroma_subsampling=False)
                del band4

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