#!/bin/bash
MODULE=""
# MODULE="-m recipy"
mkdir -p tmp
rm -rf tmp/*

mkdir -p tmp/gdal
python $MODULE run_gdal.py Open data/gdal/image.tiff
python $MODULE run_gdal.py Driver.Create tmp/gdal/image.tiff
python $MODULE run_gdal.py Driver.CreateCopy data/gdal/image.tiff tmp/gdal/imagecopy.tiff
