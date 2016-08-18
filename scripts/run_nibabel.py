"""
Usage:

    python run_nibabel.py nifti1.Nifti1Image.from_filename nifti1_image
    python run_nibabel.py nifti1.Nifti1Image.to_filename nifti1_image
    python run_nibabel.py nifti2.Nifti2Image.from_filename nifti2_image
    python run_nibabel.py nifti2.Nifti2Image.to_filename nifti2_image
    python run_nibabel.py freesurfer.mghformat.MGHImage.from_filename mgh_image
    python run_nibabel.py freesurfer.mghformat.MGHImage.to_filename mgh_image
    python run_nibabel.py spm99analyze.Spm99AnalyzeImage.from_filename spm99_image
    python run_nibabel.py spm99analyze.Spm99AnalyzeImage.to_filename spm99_image
    python run_nibabel.py minc1.Minc1Image.from_filename minc1_image
    python run_nibabel.py minc1.Minc1Image.to_filename minc1_image
    python run_nibabel.py minc2.Minc2Image.from_filename minc2_image
    python run_nibabel.py minc2.Minc2Image.to_filename minc2_image
    python run_nibabel.py analyze.AnalyzeImage.from_filename analyze_image
    python run_nibabel.py analyze.AnalyzeImage.to_filename analyze_image
    python run_nibabel.py parrec.PARRECImage.from_filename parrec_image.PAR
    python run_nibabel.py parrec.PARRECImage.to_filename parrec_image.PAR parrec_image-copy
    python run_nibabel.py spm2analyze.Spm2AnalyzeImage.from_filename spm2_image
    python run_nibabel.py spm2analyze.Spm2AnalyzeImage.to_filename spm2_image
"""
from __future__ import print_function
import nibabel as nib
import numpy as np
import os
import sys


def get_data():
    return np.arange(24, dtype=np.int16).reshape((2, 3, 4))


def get_affine():
    affine = np.diag([1, 2, 3, 1])


def invoke_nifti1_Nifti1Image_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.Nifti1Image.from_filename(file_name)
    print("Data:", data.shape)


def invoke_nifti1_Nifti1Image_to_filename(arguments):
    file_name = arguments[0]
    img = nib.Nifti1Image(get_data(), get_affine())
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_nifti2_Nifti2Image_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.Nifti2Image.from_filename(file_name)
    print("Data:", data.shape)


def invoke_nifti2_Nifti2Image_to_filename(arguments):
    file_name = arguments[0]
    img = nib.Nifti2Image(get_data(), get_affine())
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_freesurfer_mghformat_MGHImage_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.freesurfer.mghformat.MGHImage.from_filename(file_name)
    print("Data:", data.shape)


def invoke_freesurfer_mghformat_MGHImage_to_filename(arguments):
    file_name = arguments[0]
    img = nib.freesurfer.mghformat.MGHImage(get_data(), np.eye(4))
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_spm99analyze_Spm99AnalyzeImage_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.spm99analyze.Spm99AnalyzeImage.from_filename(file_name)
    print("Data:", data.shape)


def invoke_spm99analyze_Spm99AnalyzeImage_to_filename(arguments):
    file_name = arguments[0]
    img = nib.spm99analyze.Spm99AnalyzeImage(get_data(), np.eye(4))
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_minc1_Minc1Image_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.minc1.Minc1Image.from_filename(file_name)
    print("Data:", data.shape)


def invoke_minc1_Minc1Image_to_filename(arguments):
    file_name = arguments[0]
    img = nib.minc1.Minc1Image(get_data(), np.eye(4))
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_minc2_Minc2Image_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.minc2.Minc2Image.from_filename(file_name)
    print("Data:", data.shape)


def invoke_minc2_Minc2Image_to_filename(arguments):
    file_name = arguments[0]
    img = nib.minc2.Minc2Image(get_data(), np.eye(4))
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_analyze_AnalyzeImage_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.analyze.AnalyzeImage.from_filename(file_name)
    print("Data:", data.shape)


def invoke_analyze_AnalyzeImage_to_filename(arguments):
    file_name = arguments[0]
    img = nib.AnalyzeImage(get_data(), np.eye(4))
    print("Saving data:", file_name)
    img.to_filename(file_name)


def invoke_parrec_PARRECImage_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.parrec.PARRECImage.from_filename(file_name)
    print("Data:", data.shape)


def invoke_parrec_PARRECImage_to_filename(arguments):
    in_file_name = arguments[0]
    out_file_name = arguments[1]
    img = nib.parrec.PARRECImage.from_filename(in_file_name)
    print("Saving data:", out_file_name)
    img.to_filename(out_file_name)


def invoke_spm2analyze_Spm2AnalyzeImage_from_filename(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = nib.spm2analyze.Spm2AnalyzeImage.from_filename(file_name)
    print("Data:", data.shape)


def invoke_spm2analyze_Spm2AnalyzeImage_to_filename(arguments):
    file_name = arguments[0]
    img = nib.spm2analyze.Spm2AnalyzeImage(get_data(), np.eye(4))
    print("Saving data:", file_name)
    img.to_filename(file_name)


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
