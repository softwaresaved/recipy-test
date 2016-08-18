#!/bin/bash
MODULE=""
# MODULE="-m recipy"
mkdir -p tmp
rm -rf tmp/*

mkdir tmp/matplotlib
python $MODULE run_matplotlib.pyplot.py savefig tmp/matplotlib/plot.png

mkdir tmp/bs4
python $MODULE run_bs4.py BeautifulSoup data/bs4/index.html

mkdir tmp/lxml
python $MODULE run_lxml.etree.py parse data/lxml/data.xml
python $MODULE run_lxml.etree.py iterparse data/lxml/data.xml

mkdir tmp/PIL
python $MODULE run_PIL.py Image.open data/PIL/image.png
python $MODULE run_PIL.py Image.save data/PIL/image.png tmp/PIL/image.png

mkdir tmp/numpy
python $MODULE run_numpy.py loadtxt data/numpy/data.csv
python $MODULE run_numpy.py fromfile data/numpy/data.csv
python $MODULE run_numpy.py genfromtxt data/numpy/data_incomplete.csv
python $MODULE run_numpy.py save tmp/numpy/data.npy
python $MODULE run_numpy.py savez tmp/numpy/data.npz
python $MODULE run_numpy.py savez_compressed tmp/numpy/dataz.npz
python $MODULE run_numpy.py savetxt tmp/numpy/data.txt

mkdir tmp/sklearn
python $MODULE run_sklearn.py dump_svmlight_file tmp/sklearn/data.svmlight
python $MODULE run_sklearn.py load_svmlight_file data/sklearn/data.svmlight

mkdir tmp/skimage
python $MODULE run_skimage.py io.imread data/skimage/image.png 
python $MODULE run_skimage.py io.imsave data/skimage/image.png tmp/skimage/image.png
python $MODULE run_skimage.py external.tifffile.imread data/skimage/image.tiff
python $MODULE run_skimage.py external.tifffile.imsave data/skimage/image.tiff tmp/skimage/image.tiff
python $MODULE run_skimage.py io.load_sift data/skimage/sift.key 
python $MODULE run_skimage.py io_load_surf data/skimage/image.surf 
