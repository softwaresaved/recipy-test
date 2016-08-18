"""
Usage:

    python run_numpy.py loadtxt data/data.csv
    python run_numpy.py fromfile data/data.csv
    python run_numpy.py genfromtxt data/data_incomplete.csv
    python run_numpy.py save data.npy
    python run_numpy.py savez data.npz
    python run_numpy.py savez_compressed dataz.npz
    python run_numpy.py savetxt data.txt
"""
from __future__ import print_function
import numpy as np
import sys


def invoke_loadtxt(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = np.loadtxt(file_name, delimiter=",")
    print("Data:", data.shape)
    print(data)


def invoke_fromfile(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = np.fromfile(file_name, sep=",")
    print("Data:", data.shape)
    print(data)


def invoke_genfromtxt(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = np.genfromtxt(file_name, delimiter=",", missing_values="", filling_values=-1)
    print("Data:", data.shape)
    print(data)


def invoke_save(arguments):
    file_name = arguments[0]
    data = np.arange(10)
    print("Data:", data.shape)
    print(data)
    print("Saving data:", file_name)
    np.save(file_name, data)


def invoke_savez(arguments):
    file_name = arguments[0]
    data1 = np.arange(5)
    data2 = np.arange(20,30)
    print("Data:", data1.shape)
    print(data1)
    print("Data:", data2.shape)
    print(data2)
    print("Saving data:", file_name)
    np.savez(file_name, data1=data1, data2=data2)


def invoke_savez_compressed(arguments):
    file_name = arguments[0]
    data1 = np.arange(5)
    data2 = np.arange(20,30)
    print("Data:", data1.shape)
    print(data1)
    print("Data:", data2.shape)
    print(data2)
    print("Saving data:", file_name)
    np.savez_compressed(file_name, data1=data1, data2=data2)


def invoke_savetxt(arguments):
    file_name = arguments[0]
    data = np.arange(10)
    print("Data:", data.shape)
    print(data)
    print("Saving data:", file_name)
    np.savetxt(file_name, data)


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
