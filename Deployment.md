# recipy deployment and usage

Mike Jackson, The Software Sustainability Institute / EPCC, The University of Edinburgh

## Introduction

This report reviews recipy, a provenance framework for Python developed by RObin Wilson of the University of Southampton. This report summarises experiences of, and makes recommendations relating to, deploying and using recipy.

The review used the following resources:

* [recipy](https://github.com/recipy/recipy) GitHub repository.
* [recipy 0.2.3](https://pypi.python.org/pypi/recipy) package on PyPI (Python Package Index).

Suggestions and issues arising are marked in **bold**.

---

## Deployment environments

The deployment environments are virtual machines running on:

* VMWare Player 7.1.3 ([download page](https://my.vmware.com/en/web/vmware/free#desktop_end_user_computing/vmware_workstation_player)).
* Dell Latitude E7440:
  - 64-bit Intel Core i5-4310U CPU 2GHz, 2.60GHz 2 core.
  - 8GB RAM.
  - 185GB hard disk.
  - Windows 7 Enterprise Service Pack 1.

Currently all of the input/output functions for the following Python packages are wrapped by recipy:

* [numpy](http://www.numpy.org/). This can be installed as part of [SciPy](https://www.scipy.org/) ([Installing the SciPy Stack](https://www.scipy.org/install.html))
* [pandas](http://pandas.pydata.org/). This can be installed as part of SciPy.
* [matplotlib](http://matplotlib.org/). This can be installed as part of SciPy.
* [Pillow](https://python-pillow.org/). See [Installation](https://pillow.readthedocs.io/en/latest/installation.html).
* [scikit-learn](http://scikit-learn.org/stable/). See [Installing scikit-learn](http://scikit-learn.org/stable/install.html). They comment that "We don't recommend installing scipy or numpy using pip on linux".
* [scikit-image](http://scikit-image.org). See [Installing scikit-image](http://scikit-image.org/docs/dev/install.html).
* [NiBabel](http://nipy.org/nibabel/) (only the data formats in submodules imported by default). See [Installation](http://nipy.org/nibabel/installation.html).
* [Geospatial Data Abstraction Library](https://pypi.python.org/pypi/GDAL/). Note that Windows requires installing GDAL Windows binaries, modifying system paths and creating environment variables.

The following describes the virtual machines used and the Python versions installed onto these, along with the commands used to install the above packages.

### Windows 7 Enterprise Service Pack 1 virtual machine

Install:

* [Git for Windows](https://git-for-windows.github.io/) 2.9.2
* [Anaconda](https://www.continuum.io/downloads) 4.1.1 and Python 3.5.2.

```
pip install nibabel
```

I didn't install GDAL due to the additional Windows-specific install process. 

**TODO** revisit GDAL for completeness.

### Ubuntu 14.04.3 LTS virtual machine (default Python users)

By default, Ubuntu 14.04.3 LTS comes with Python 2.7.6 and 3.4.0.

Install Python 2 packages:

```
sudo su -
apt-get install python-numpy python-scipy python-matplotlib python-pandas python-nose

apt-get install python-pip
apt-get install python-setuptools

apt-get install python-pillow
apt-get install python-sklearn
apt-get install python-skimage
apt-get install python-nibabel
apt-get install python-gdal

pip freeze
```
```
GDAL==1.10.1
Pillow==2.3.0
matplotlib==1.3.1
nibabel==1.2.2
numpy==1.8.2
pandas==0.13.1
scikit-image==0.9.3
scikit-learn==0.14.1
```

Install Python 3 packages:

```
sudo su -
apt-get install python3-numpy python3-scipy python3-matplotlib python3-pandas python3-nose

apt-get install python3-pip
apt-get install python3-setuptools

apt-get install python3-pillow
pip3 install scikit-learn
apt-get install python3-skimage
pip3 install python3-nibabel
apt-get install python3-gdal

pip3 freeze
```
```
GDAL==1.10.1
Pillow==2.3.0
matplotlib==1.3.1
nibabel==2.0.2
numpy==1.8.2
pandas==0.13.1
scikit-image==0.9.3
scikit-learn==0.17.1
```

I used pip for scikit-learn and nibabel as there are no python3-sklearn or python3-nibabel packages.

**virtualenv 15.0.2**

[virtualenv](https://pypi.python.org/pypi/virtualenv) is a tool that creates isolated Python environments with all the executables and packages that that specific environment needs. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) extends virtualenv with wrappers to make creating and managing virtual environments easier:

```
sudo su -
pip install virtualenvwrapper
pip3 install virtualenvwrapper
```

### Ubuntu 14.04.3 LTS virtual machine (local Python users)

**Anaconda 4.1.1**

[Anaconda](https://www.continuum.io) provides Python, the SciPy stack and other scientific Python packages, including (from [Anaconda package list](https://docs.continuum.io/anaconda/pkg-docs)): numpy, pandas, matplotlib, scikit-learn, scikit-image, pillow.

Install Anaconda, Python 2.7.12 and packages:

```
wget http://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh
bash Anaconda2-4.1.1-Linux-x86_64.sh
```

Create use-anaconda2.sh to set up environment (usually this goes into .bashrc, but don't want to collide with Anaconda Python 3 or pyenv):

```
export PATH=/home/ubuntu/anaconda2/bin:$PATH
```

```
source use-anaconda2.sh

pip install nibabel
apt-get install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
easy_install "GDAL==1.10.0"

pip freeze
```
```
GDAL==1.10.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.2.0
scikit-image==0.12.3
scikit-learn==0.17.1
```

The current version of GDAL, 2.1.0, needs libgdal 1.11.0 or greater. apt-get installs version 1.9.0-1~. Running apt-get install python-gdal, on the default Python users VM, showed it to install Python GDAL 1.10.1. easy_install failed to find 1.10.1. pip install GDAL=1.10.0 showed the closest was 1.10.0.

Install Anaconda, Python 3.5.2 and packages:

```
wget http://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh
bash Anaconda3-4.1.1-Linux-x86_64.sh
```

Create use-anaconda3.sh to set up environment:

```
export PATH=/home/ubuntu/anaconda3/bin:$PATH
```

```
source use-anaconda3.sh
```

Install packages as above.

```
pip freeze
```
```
GDAL==1.10.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.2.0
scikit-image==0.12.3
scikit-learn==0.17.1
```

**pyenv 05/08/2016**

[pyenv](https://github.com/yyuu/pyenv) allows users to deploy multiple versions of Python within thier own directory, and to switch between these versions.

```
sudo su -
apt-get install git
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

Create use-pyenv.sh to set up environment to use pyenv (usually this goes into .bash_profile, but don't want to have pyenv on same PATH with Anaconda):

```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

```
$ source use-pyenv.sh
$ pyenv update
$ pyenv install -l
$ pyenv install 2.7.6
$ pyenv install 3.4.0
```

Ubuntu package pre-requisites can be assumed to have been installed via Anaconda.

Install Python 2 packages:

```
source use-pyenv.sh 
mkdir py2dir
cd py2dir/
pyenv local 2.7.6

pip install numpy
pip install scipy
sudo apt-get install libfreetype6-dev
pip install matplotlib
pip install pandas
pip install nose
pip install pillow
pip install scikit-learn
pip install scikit-image
pip install nibabel
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
easy_install "GDAL==1.10.0"
pip freeze
```
```
GDAL==1.10.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.3.0
scikit-image==0.12.3
scikit-learn==0.17.1
```

Install Python 3 packages:

```
source use-pyenv.sh 
mkdir py3dir
cd py3dir/
pyenv local 3.4.0

pip install numpy
sudo apt-get install libblas-dev liblapack-dev gfortran
pip install scipy
pip install matplotlib
pip install pandas
pip install nose
pip install pillow=="3.2.10"
pip install scikit-learn
pip install scikit-image
pip install nibabel
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
easy_install "GDAL==1.10.0"

pip freeze
```
```
GDAL==1.10.0
Pillow==3.2.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
scikit-image==0.12.3
scikit-learn==0.17.1
```

Installing the current Pillow gives an error under Python 3:

```
pip install pillow

Tk/tkImaging.c:396:5: error: ISO C90 forbids mixed declarations and code [-Werror=declaration-after-statement]
```

which has been [noted by others](https://github.com/python-pillow/Pillow/issues/2017). So I installed the same version as for Python 2 (3.2.0), which others noted works.

#### Docker (dockeruser)

**TODO** is there any point in doing this? It's just another VM in effect!

---

## Summary of deployment environments

This summarises the environments into which recipy was deployed. The default package location for each Python version was used, except for the virtualenv environments where recipy was installed into a virtualenv in the user's local directory.

| Operating System         | Python                     |
| ------------------------ | -------------------------- |
| Windows 7 Enterprise SP1 |                            |
|                          | 3.5.2 (Anaconda 4.1.1)     |
| Ubuntu 14.04.3 LTS       |                            |
|                          | 2.7.6                      |
|                          | 3.4.0                      |
|                          | 2.7.6 + virtualenv 15.0.2) |
|                          | 3.4.0 + virtualenv 15.0.2) |
| Ubuntu 14.04.3 LTS       |                            |
|                          | 3.5.2 (Anaconda 4.1.1)     |
|                          | 2.7.4 (pyenv 05/08/2016)   |
|                          | 3.4.0 (pyenv 05/08/2016)   |

---

## Deploy recipy and run simple script

The following scripts were used to check that a recipy deployment was operating correctly with numpy.

check-recipy.py:

```
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file.csv", data, delimiter=",")
```

check-recipy-import.py:

```
import recipy
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file-import.csv", data, delimiter=",")
```

The following script was used to check recipy's wrapper's for Python's open command:

check-recipy-open.py:

```
import recipy
with recipy.open('file-open.txt', 'w') as f:
    f.write("This is a test")
```

### Install recipy package 0.2.3 under Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)

The latest recipy package, 0.2.3, can be installed, via Python's [pip](https://pip.pypa.io/en/stable/) package manager, as follows:

```
python --version
```
```
Python 3.5.2 :: Anaconda 4.1.1 (64-bit)
```
```
pip install recipy
pip freeze | grep recipy
```
```
recipy==0.2.3
```
```
recipy --version
```
```
recipy v0.2.3
```

### Run script

```
mkdir deployment
cd deployment
```

Copy scripts to deployment/

```
python check-recipy-import.py
```
```
recipy run inserted, with ID b07adfa8-b1bc-4ef9-85f2-1c4ae8a8db44
```
```
recipy search file-import.csv
```
```
Run ID: b07adfa8-b1bc-4ef9-85f2-1c4ae8a8db44
Created by mjj on 2016-08-11T15:00:12 UTC
Ran C:\Users\mjj\deployment\check-recipy-import.py using C:\Users\mjj\Anaconda3\python.exe
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Inputs: none
Outputs:
  C:\Users\mjj\deployment\file-import.csv
```

**Suggestion** README.md states that:

> it will produce an output called test.npy. To find out the details of the run which created this file you can search using
> recipy search test.npy

Rephrase this to:

> The sample script above will produce...

to reinforce that it's the sample script, and not recipy, that produces test.npy.

**Suggestion** Log the versions of the libraries (e.g. numpy) used too.

### Use GUI

```
recipy gui
```

A browser appears.

**Issue** The search box did not seem to work. I tried it using "mjj", "file.txt", "C:\Users\mjj\ssi\file" and for each got a HTTP 500 Interal Server Error.

**Suggestion** Provide examples of search strings in the documentation.

* Click View details
* Click Save as JSON

```
cat ../Downloads/runs.json
```
```
[
  {
    "author": "mjj",
    "command": "C:\\Users\\mjj\\Anaconda3\\python.exe",
    "command_args": "",
    "date": "{TinyDate}:2016-08-11T15:00:12",
    "description": "",
    "environment": [
      "Windows-7-6.1.7601-SP1",
      "python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]"
    ],
    "inputs": [],
    "outputs": [
      "C:\\Users\\mjj\\deployment\\file-import.csv"
    ],
    "script": "C:\\Users\\mjj\\deployment\\check-recipy-import.py",
    "unique_id": "b07adfa8-b1bc-4ef9-85f2-1c4ae8a8db44"
  }
]
```

* Enter Notes: "This was Mike's first use of recipy."
* Click Save notes
* Click Save as JSON

```
cat ../Downloads/runs.json
```
```
...
    "notes": "This was Mike's first use of recipy.",
...
```

### Rerun script and view information

Rerun:

```
python check-recipy-import.py
```
```
$ recipy search file-import.csv
Run ID: 23bf2fd2-b67a-46c1-9fd8-960e71d32f2f
Created by mjj on 2016-08-11T15:03:53 UTC
Ran C:\Users\mjj\deployment\check-recipy-import.py using C:\Users\mjj\Anaconda3\python.exe
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Inputs: none
Outputs:
  C:\Users\mjj\deployment\file-import.csv

** Previous runs creating this output have been found. Run with --all to show. **
```
```
python check-recipy-import.py --all
```
```
...shows both...
```
```
recipy latest
```
```
...shows most recent...
```
```
recipy latest -j
```
```
...shows most recent as JSON...
```

### Search information

```
recipy search -i 23bf2fd2-b67a-46c1-9fd8-960e71d32f2f
```
```
No results found
```
```
recipy search -i 23bf2fd2-b67a-46c1-9fd8-960e71d32f2
```
```
...shows details...
```
```
recipy search -i 23bf2fd2-b67a-46c1-9fd8-960e71d32f2 -j
```
```
...shows JSON...
```

**Suggestion** Allow use of full IDs when searching. It feels counter-intuitive that a partial match succeeds but a full match does not.

**Suggestion** As not all command-line options apply to all commands, provide information, via the usage information and in the documentation, on which options apply to which commands.

```
recipy search -r ".*ile.*c.*"
```
```
...shows details...
```
```
recipy search -f "ile"
```
```
...shows details...
```
```
recipy search -f "il..c"
```
```
No results found.
```

**Suggestion** Explain the difference between fuzzy and regex searching in the documentation, and provide examples of fuzzy and regular expression patterns.

### Annotate information

```
recipy annotate
```
```
'$EDITOR' is not recognized as an internal or external command, operable program or batch file.
No annotation entered, exiting.
```

**Suggestion** Document the need to set the EDITOR variable and that user can override their default e.g. if they want nano rather than vi on Ubuntu.

```
EDITOR=notepad.exe
recipy annotate
```
```
...as above...
```

```
export EDITOR=notepad.exe
recipy annotate
```
```
...as above...
```

**Issue** Under Windows, I tried using .bashrc and .bash_profile to set EDITOR, and also tried running these commands within the Anaconda Python Prompt, rather than the Git Bash prompt, but with no success.

**Suggestion** Resolve this issue or, if it cannot be resolved, recommend that Windows/Git Bash/Anaconda users use recipy gui.

### View information outwith original directory

```
cd
recipy search C:/Users/mjj/deployment/file-import.csv
```
```
...shows details...
```
```
mv deployment tmp
```
```
recipy search C:/Users/mjj/deployment/file-import.csv
```
```
...shows details...
```
```
mv tmp deployment
cd deployment/
```

**Suggestion** Provide examples of using absolute paths with recipy search in the documentation.

**Suggestion** Add a note to the documentation that files can be searched for even if they no longer exist, and a complementary caution that just because a file exists in the recipy database it does not necessarily exist in reality!

### Use `-m recipy`

```
python -m recipy check-recipy.py
recipy latest
```
```
Run ID: 8b624e12-3ec9-4bae-a39b-1bca2d53af8e
Created by mjj on 2016-08-11T15:11:44 UTC
Ran C:\Users\mjj\deployment\check-recipy.py using C:\Users\mjj\Anaconda3\python.exe
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Inputs: none
Outputs:
  C:\Users\mjj\deployment\file.csv
```

### Use `recipy.open`

```
python check-recipy-open.py
```
```
recipy run inserted, with ID 3e5b0039-b611-44b7-b027-de241e4d4a4b
Traceback (most recent call last):
  File "check-recipy-open.py", line 2, in <module>
    with recipy.open('file-open.txt', 'w') as f:
AttributeError: module 'recipy' has no attribute 'open'
```
```
recipy latest
```
```
Run ID: 3e5b0039-b611-44b7-b027-de241e4d4a4b
Created by mjj on 2016-08-11T15:12:47 UTC
Ran C:\Users\mjj\deployment\check-recipy-open.py using C:\Users\mjj\Anaconda3\python.exe
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Exception: (AttributeError) module 'recipy' has no attribute 'open'
Inputs: none
Outputs: none
```

**TODO** maybe this was added to recipy and README.md since the most recent package was bundled? See if this arises using latest version. If it doesn't arise in the latest version then add a Suggestion to describe what features are supported by what versions.

### Use Git

```
git init
git config --global user.name "Mike Jackson"
git config --global user.email "michaelj@epcc.ed.ac.uk"
git add *.py
git commit -m "Added recipy scripts"
python -m recipy check-recipy-import.py
recipy latest
```
```
Run ID: 6ca48f3b-1a7e-4b40-8762-801fe9a94970
Created by mjj on 2016-08-11T15:15:32 UTC
Ran C:\Users\mjj\deployment\check-recipy-import.py using C:\Users\mjj\Anaconda3\python.exe
Git: commit d51ec9c83681f82ea8f53e228fddd55c95728282, in repo C:\Users\mjj\deployment, with origin None
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Inputs: none
Outputs:
  C:\Users\mjj\deployment\file-import.csv
```

Edit check-recipy-import.py and change first range to be range(5,9)

```
python check-recipy-import.py
cat file-import.csv
git commit -m "Changed check-recipy-import.py range to 5,9" .
recipy latest
recipy latest --diff
```
```
Run ID: fba82435-0e50-464d-8986-b9f8f81d085b
Created by mjj on 2016-08-11T15:17:12 UTC
Ran C:\Users\mjj\deployment\check-recipy-import.py using C:\Users\mjj\Anaconda3\python.exe
Git: commit d51ec9c83681f82ea8f53e228fddd55c95728282, in repo C:\Users\mjj\deployment, with origin None
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Inputs: none
Outputs:
  C:\Users\mjj\deployment\file-import.csv

@@ -1,5 +1,5 @@
 import recipy
 import numpy as np

-data = np.array([list(range(4,8)), list(range(12,16))])
+data = np.array([list(range(5,9)), list(range(12,16))])
 np.savetxt("file-import.csv", data, delimiter=",")
```
```
python check-recipy-import.py
recipy latest --diff
```
```
...as above but without the diff information...
```

**Suggestion** Describe how and when --diff will show the diff i.e. if the commit is newer than the most recent files is what it seems to do.

**Suggestion** Provide brief descriptions, with sample inputs and outputs for every command.

```
cd ..
git clone C:/Users/mjj/deployment deployment-clone
cd deployment-clone/
python check-recipy-import.py
recipy latest
```
```
...
Git: commit 6ee366b86b7f3beb9d943a2ff526a562bc692452, in repo C:\Users\mjj\deployment-clone, with origin C:/Users/mjj/deployment
...
```

### Uninstall

```
find Anaconda3/ -name "*recipy*"
```
```
Anaconda3/Lib/site-packages/recipy
Anaconda3/Lib/site-packages/recipy-0.2.3.dist-info
Anaconda3/Lib/site-packages/recipyCmd
Anaconda3/Lib/site-packages/recipyCmd/recipycmd.py
Anaconda3/Lib/site-packages/recipyCmd/__pycache__/recipycmd.cpython-35.pyc
Anaconda3/Lib/site-packages/recipyCommon
Anaconda3/Lib/site-packages/recipyGui
Anaconda3/Lib/site-packages/recipyGui/tests/test_recipyGui.py
Anaconda3/Lib/site-packages/recipyGui/tests/__pycache__/test_recipyGui.cpython-35.pyc
Anaconda3/Scripts/recipy.exe
```
```
pip uninstall recipy
```
```
Successfully uninstalled recipy-0.2.3
```
```
find Anaconda3/ -name "*recipy*"
```

### Deployment of recipy package 0.2.3 under other environments

The above steps were run on the other environments. Only information on where commands, outputs or behaviour deviated from the run above, and issues and suggestions arising are documented.

```
python --version
pip install recipy
pip freeze | grep recipy
recipy --version
mkdir deployment
cd deployment
Copy scripts to deployment/
```
```
python check-recipy-import.py
recipy search file-import.csv
recipy gui
* Run searches
* Click View details
* Click Save as JSON
cat ../Downloads/runs.json
* Enter Notes: "This was Mike's first use of recipy."
* Click Save notes
* Click Save as JSON
cat ../Downloads/runs.json
python check-recipy-import.py
recipy search file-import.csv
recipy search file-import.csv --all
recipy latest
recipy latest -j
recipy search -i 5f551f52-2e4b-429e-bd4e-0a22ae12f198
recipy search -i 5f551f52-2e4b-429e-bd4e-0a22ae12f19
recipy search -i 5f551f52-2e4b-429e-bd4e-0a22ae12f19 -j
recipy search -r ".*ile.*c.*"
recipy search -f "ile"
recipy search -f "il..c"
recipy annotate
EDITOR=notepad.exe
recipy annotate
export EDITOR=notepad.exe
recipy annotate
cd
recipy search C:/Users/mjj/deployment/file-import.csv
mv deployment tmp
recipy search C:/Users/mjj/deployment/file-import.csv
mv tmp deployment
```
```
cd deployment/
python -m recipy check-recipy.py
recipy latest
```
```
python check-recipy-open.py
recipy latest
```
```
git init
git config --global user.name "Mike Jackson"
git config --global user.email "michaelj@epcc.ed.ac.uk"
git add *.py
git commit -m "Added recipy scripts"
python check-recipy-import.py
recipy latest
Edit check-recipy-import.py and change first range to be range(5,9)
python check-recipy-import.py
cat file-import.csv
git commit -m "Changed check-recipy-import.py range to 5,9" .
recipy latest
recipy latest --diff
python check-recipy-import.py
recipy latest --diff
cd ..
git clone C:/Users/mjj/deployment deployment-clone
cd deployment-clone/
python check-recipy-import.py
recipy latest
```
```
find Anaconda3/ -name "*recipy*"
pip uninstall recipy
find Anaconda3/ -name "*recipy*"
```

Ubuntu 14.04.3 LTS + 2.7.6

Ubuntu 14.04.3 LTS + 3.4.0

Ubuntu 14.04.3 LTS + 2.7.6 + virtualenv 15.0.2)

Ubuntu 14.04.3 LTS + 3.4.0 + virtualenv 15.0.2)

Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)

Ubuntu 14.04.3 LTS + 2.7.4 (pyenv 05/08/2016)

Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 05/08/2016)

### Deployment of latest version under all environments

The latest version of recipy, from its GitHub repository, can be deployed as follows:

```
git clone https://github.com/recipy/recipy
cd recipy
python setup.py install
```

Uninstall using

```
python setup.py install --record install-files.txt
cat install-files.txt | sudo xargs rm -rf
```

**TODO**

Same steps as before.

Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)

Ubuntu 14.04.3 LTS + 2.7.6

Ubuntu 14.04.3 LTS + 3.4.0

Ubuntu 14.04.3 LTS + 2.7.6 + virtualenv 15.0.2)

Ubuntu 14.04.3 LTS + 3.4.0 + virtualenv 15.0.2)

Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)

Ubuntu 14.04.3 LTS + 2.7.4 (pyenv 05/08/2016)

Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 05/08/2016)

---

## Other examples

**TODO** Write and run one sample script per package recipy can log. These can form basis of test scripts.

**Suggestion** Provide guidelines on how to use recipy in a research workflow e.g. how to use recipy and Git to record provenance and recommended ways of archiving input/output files etc.

---

## Documentation

**TODO** Look at README.md sections:

* Configuration
* How it works

README.md comments that 

> If you want to log inputs and outputs of files read or written with built-in open, you need to do a little more work. Either use `recipy.open` (only requires import recipy at the top of your script), or add `from recipy import open` and just use `open`. This workaround is required, because many libraries use built-in open internally, and you only want to record the files you explicitly opened yourself.
> If you use Python 2, you can pass an `encoding` parameter to `recipy.open`. In this case `codecs` is used to open the file with proper encoding.

**Suggestion** Describe whether recipy.open has the same function signature as open (with the additional encoding parameter) or whether it changes it, in which case describe the altered signature.

---

### Set up virtual environments (notes to be cleaned)

```
$ virtualenv --python=/usr/bin/python3 --no-site-packages secret_ciphers
$ mkdir ~/Envs
```

Edit ~/.bash_profile and add the lines:

```
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
```

Set environment:

```
$ source ~/bash_profile
```

If using virtual environments, then create a virtual environment. For example:

```
$ mkvirtualenv prov
```

```
virtualenv -p /usr/bin/python2.6 <path/to/new/virtualenv/>
mkvirtualenv -p python2.6 env
python --version
```

Check version

OR

```
python3 -m virtualenv venv
```

---
