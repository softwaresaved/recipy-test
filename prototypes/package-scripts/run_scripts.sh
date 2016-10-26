#!/bin/bash
MODULE=""
# MODULE="-m recipy"
mkdir -p tmp
rm -rf tmp/*

mkdir -p tmp/skimage
python $MODULE run_skimage.py io.imread data/skimage/image.png 
python $MODULE run_skimage.py io.imsave data/skimage/image.png tmp/skimage/rotated.png
python $MODULE run_skimage.py external.tifffile.imread data/skimage/image.tiff
python $MODULE run_skimage.py external.tifffile.imsave data/skimage/image.tiff tmp/skimage/rotated.tiff
python $MODULE run_skimage.py io.load_sift data/skimage/sift.key 
python $MODULE run_skimage.py io_load_surf data/skimage/image.surf 

mkdir -p tmp/gdal
python $MODULE run_gdal.py Open data/gdal/image.tiff
python $MODULE run_gdal.py Driver.Create tmp/gdal/image.tiff
python $MODULE run_gdal.py Driver.CreateCopy data/gdal/image.tiff tmp/gdal/imagecopy.tiff
