FROM ubuntu:trusty-20160217
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y nano
RUN apt-get install -y git
RUN apt-get install -y python3-numpy
RUN apt-get install -y python3-scipy
RUN apt-get install -y python3-matplotlib
RUN apt-get install -y python3-pandas python3-nose
RUN apt-get install -y python3-nose
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pillow
RUN pip3 install scikit-learn
RUN apt-get install -y python3-skimage
RUN pip3 install nibabel
RUN apt-get install -y python3-gdal
RUN pip3 freeze
# Default command to run as part "docker run" if no command is given.
CMD ["/bin/bash"]
