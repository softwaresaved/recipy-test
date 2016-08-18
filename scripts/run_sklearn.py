"""
Usage:

    python run_sklearn.py dump_svmlight_file data.svmlight
    python run_sklearn.py load_svmlight_file data/data.svmlight
"""
from __future__ import print_function
import numpy as np
from sklearn import datasets
import sys


def invoke_dump_svmlight_file(arguments):
    file_name = arguments[0]
    x = np.array([[1,2,3,4,5],[6,7,8,9,10]])
    print("Data:", x.shape)
    print(x)
    y = np.array([10, 20])
    print("Data:", y.shape)
    print(y)
    print("Saving data:", file_name)
    datasets.dump_svmlight_file(x, y, file_name, comment="Sample svmlight file")


def invoke_load_svmlight_file(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    (x, y) = datasets.load_svmlight_file(file_name)
    print("X:")
    print(x)
    print("Y:")
    print(y)


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
