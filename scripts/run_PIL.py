"""
Usage:

    python -m run_PIL.py Image.open data/image.png
    python -m run_PIL.py Image.save data/image.png plot.png
"""
from __future__ import print_function
from PIL import Image
import sys


def invoke_Image_open(arguments):
    file_name = arguments[0]
    print("Loading image:", file_name)
    with Image.open(file_name) as f:
        print("Size:", f.size)


def invoke_Image_save(arguments):
    in_file_name = arguments[0]
    out_file_name = arguments[1]
    print("Loading image:", in_file_name)
    with Image.open(in_file_name) as i:
        j = i.rotate(90)
        print("Saving rotated image:", out_file_name)
        j.save(out_file_name)


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
