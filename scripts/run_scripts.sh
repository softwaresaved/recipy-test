#!/bin/bash
MODULE=""
# MODULE="-m recipy"
python $MODULE run_matplotlib.pyplot.py savefig plot.png

python $MODULE run_bs4.py BeautifulSoup data/index.html

python $MODULE run_lxml.etree.py parse data/data.xml
python $MODULE run_lxml.etree.py iterparse data/data.xml

python $MODULE run_PIL.py Image.open data/image.png
python $MODULE run_PIL.py Image.save data/image.png pilplot.png

python $MODULE run_numpy.py loadtxt data/data.csv
python $MODULE run_numpy.py fromfile data/data.csv
python $MODULE run_numpy.py genfromtxt data/data_incomplete.csv
python $MODULE run_numpy.py save data.npy
python $MODULE run_numpy.py savez data.npz
python $MODULE run_numpy.py savez_compressed dataz.npz
python $MODULE run_numpy.py savetxt data.txt
