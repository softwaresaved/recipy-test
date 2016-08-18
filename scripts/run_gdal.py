"""
Usage:

    python run_gdal.py Open image.tiff
    python run_gdal.py Driver.Create image.tiff
    python run_gdal.py Driver.CreateCopy image.tiff imagecopy.tiff
"""
from __future__ import print_function
import gdal
import numpy
import osr
import sys


def invoke_Open(arguments):
    file_name = arguments[0]
    print("Loading:", file_name)
    data_source = gdal.Open(file_name)
    print("Data:", data_source)
    print("X size:", data_source.RasterXSize)
    print("Y size:", data_source.RasterYSize)


def invoke_Driver_Create(arguments):
    file_name = arguments[0]
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    data_source = driver.Create(file_name, 50, 50, 1, gdal.GDT_Byte)
    raster = numpy.ones((50, 50), dtype=numpy.uint8)
    raster[10:40,10:40] = 0
    raster = raster * 255
    print("Saving:", file_name)
    data_source.GetRasterBand(1).WriteArray(raster)


def invoke_Driver_CreateCopy(arguments):
    in_file_name = arguments[0]
    out_file_name = arguments[1]
    data_source = gdal.Open(in_file_name)
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    print("Saving:", out_file_name)
    data_sink = driver.CreateCopy(out_file_name, data_source, 0)


if len(sys.argv) < 3:
    print(__doc__, file=sys.stderr)
    sys.exit(1)
function_name = "invoke_" + sys.argv[1].replace(".", "_")
arguments = sys.argv[2:]
if function_name not in locals():
    print(__doc__, file=sys.stderr)
    sys.exit(1)
function = locals()[function_name]
function(arguments)
