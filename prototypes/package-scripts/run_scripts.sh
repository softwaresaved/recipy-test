#!/bin/bash
MODULE=""
# MODULE="-m recipy"
mkdir -p tmp
rm -rf tmp/*

mkdir -p tmp/lxml
python $MODULE run_lxml.etree.py parse data/lxml/data.xml
python $MODULE run_lxml.etree.py iterparse data/lxml/data.xml

mkdir -p tmp/PIL
python $MODULE run_PIL.py Image.open data/PIL/image.png
python $MODULE run_PIL.py Image.save data/PIL/image.png tmp/PIL/rotated.png

mkdir -p tmp/sklearn
python $MODULE run_sklearn.py dump_svmlight_file tmp/sklearn/data.svmlight
python $MODULE run_sklearn.py load_svmlight_file data/sklearn/data.svmlight

mkdir -p tmp/skimage
python $MODULE run_skimage.py io.imread data/skimage/image.png 
python $MODULE run_skimage.py io.imsave data/skimage/image.png tmp/skimage/rotated.png
python $MODULE run_skimage.py external.tifffile.imread data/skimage/image.tiff
python $MODULE run_skimage.py external.tifffile.imsave data/skimage/image.tiff tmp/skimage/rotated.tiff
python $MODULE run_skimage.py io.load_sift data/skimage/sift.key 
python $MODULE run_skimage.py io_load_surf data/skimage/image.surf 

mkdir -p tmp/nibabel
python $MODULE run_nibabel.py nifti1.Nifti1Image.from_filename data/nibabel/nifti1_image
python $MODULE run_nibabel.py nifti1.Nifti1Image.to_filename tmp/nibabel/nifti1_image
python $MODULE run_nibabel.py nifti2.Nifti2Image.from_filename data/nibabel/nifti2_image
python $MODULE run_nibabel.py nifti2.Nifti2Image.to_filename tmp/nibabel/nifti2_image
python $MODULE run_nibabel.py freesurfer.mghformat.MGHImage.from_filename data/nibabel/mgh_image
python $MODULE run_nibabel.py freesurfer.mghformat.MGHImage.to_filename tmp/nibabel/mgh_image
python $MODULE run_nibabel.py spm99analyze.Spm99AnalyzeImage.from_filename data/nibabel/spm99_image
python $MODULE run_nibabel.py spm99analyze.Spm99AnalyzeImage.to_filename tmp/nibabel/spm99_image
python $MODULE run_nibabel.py minc1.Minc1Image.from_filename data/nibabel/minc1_image
python $MODULE run_nibabel.py minc1.Minc1Image.to_filename tmp/nibabel/minc1_image
python $MODULE run_nibabel.py minc2.Minc2Image.from_filename data/nibabel/minc2_image
python $MODULE run_nibabel.py minc2.Minc2Image.to_filename tmp/nibabel/minc2_image
python $MODULE run_nibabel.py analyze.AnalyzeImage.from_filename data/nibabel/analyze_image
python $MODULE run_nibabel.py analyze.AnalyzeImage.to_filename tmp/nibabel/analyze_image
python $MODULE run_nibabel.py parrec.PARRECImage.from_filename data/nibabel/parrec_image.PAR
python $MODULE run_nibabel.py parrec.PARRECImage.to_filename data/nibabel/parrec_image.PAR tmp/nibabel/parrec_image
python $MODULE run_nibabel.py spm2analyze.Spm2AnalyzeImage.from_filename data/nibabel/spm2_image
python $MODULE run_nibabel.py spm2analyze.Spm2AnalyzeImage.to_filename tmp/nibabel/spm2_image

mkdir -p tmp/gdal
python $MODULE run_gdal.py Open data/gdal/image.tiff
python $MODULE run_gdal.py Driver.Create tmp/gdal/image.tiff
python $MODULE run_gdal.py Driver.CreateCopy data/gdal/image.tiff tmp/gdal/imagecopy.tiff
