"""
Usage:

    python run_skimage.py io.imread image.png 
    python run_skimage.py io.imsave image.png rotated.png
    python run_skimage.py external.tifffile.imread image.tiff
    python run_skimage.py external.tifffile.imsave image.tiff rotated.tiff
    python run_skimage.py io.load_sift sift.key 
    python run_skimage.py io_load_surf image.surf 
"""
from __future__ import print_function
import numpy as np
from skimage import external
from skimage import io
from skimage import transform
import sys


def invoke_io_imread(arguments):
    file_name = arguments[0]
    print("Loading image:", file_name)
    data = io.imread(file_name)
    print("Data:", data.shape)


def invoke_io_load_sift(arguments):
    file_name = arguments[0]
    print("Loading SIFT:", file_name)
    data = io.load_sift(file_name)
    print("Data:", data.shape)
    print("Arrays:", data.dtype.names)


def invoke_io_load_surf(arguments):
    file_name = arguments[0]
    print("Loading SURF:", file_name)
    data = io.load_surf(file_name)
    print("Data:", data.shape)
    print("Arrays:", data.dtype.names)


def invoke_io_imsave(arguments):
    in_file_name = arguments[0]
    out_file_name = arguments[1]
    print("Loading image:", in_file_name)
    data = io.imread(in_file_name)
    data = transform.rotate(data, 90)
    print("Saving rotated image:", out_file_name)
    io.imsave(out_file_name, data)


def invoke_external_tifffile_imread(arguments):
    file_name = arguments[0]
    print("Loading image:", file_name)
    data = external.tifffile.imread(file_name)
    print("Data:", data.shape)


def invoke_external_tifffile_imsave(arguments):
    in_file_name = arguments[0]
    out_file_name = arguments[1]
    print("Loading image:", in_file_name)
    data = external.tifffile.imread(in_file_name)
    data = transform.rotate(data, 90)
    data = 255 * data
    data = data.astype(dtype=np.uint8)
    print("Saving rotated image:", out_file_name)
    external.tifffile.imsave(out_file_name, data)


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
