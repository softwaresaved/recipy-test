#!/bin/bash
MODULE=""
# MODULE="-m recipy"
python $MODULE run_matplotlib.pyplot.py savefig plot.png
python $MODULE run_bs4.py BeautifulSoup data/index.html
python $MODULE run_lxml.etree.py parse data/data.xml
python $MODULE run_lxml.etree.py iterparse data/data.xml
python $MODULE run_PIL.py Image.open data/image.png
python $MODULE run_PIL.py Image.save data/image.png pilplot.png
