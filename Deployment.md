# recipy deployment and usage

Mike Jackson, The Software Sustainability Institute / EPCC, The University of Edinburgh

## Introduction

This report reviews recipy, a provenance framework for Python. This report summarises experiences of, and makes recommendations relating to, deploying and using recipy. It was written as a side-effect of familiarising myself with recipy.

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

By default, Ubuntu 14.04.3 LTS comes with Python 2.7.6 and 3.4.3.

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

**virtualenv 15.0.2**

[virtualenv](https://pypi.python.org/pypi/virtualenv) is a tool that creates isolated Python environments with all the executables and packages that that specific environment needs.

```
sudo su -
pip install virtualenv
pip3 install virtualenv
```

**virtualenvwrapper 4.7.1**

[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) extends virtualenv with wrappers to make creating and managing virtual environments easier:

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

Create `use-anaconda2.sh` to set up environment (usually this goes into `.bashrc`, but I don't want its paths to interfere with Anaconda Python 3 or pyenv):

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

The current version of GDAL, 2.1.0, needs libgdal 1.11.0 or greater. apt-get installs version 1.9.0-1~. Running `apt-get install python-gdal`, on the default Python users VM, showed it to install Python GDAL 1.10.1. easy_install failed to find 1.10.1. `pip install GDAL=1.10.0` showed that the closest match was 1.10.0.

Install Anaconda, Python 3.5.2 and packages:

```
wget http://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh
bash Anaconda3-4.1.1-Linux-x86_64.sh
```

Create `use-anaconda3.sh` to set up environment:

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

**pyenv 20160726**

[pyenv](https://github.com/yyuu/pyenv) allows users to deploy multiple versions of Python within thier own directory, and to switch between these versions.

```
sudo su -
apt-get install git
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

Create `use-pyenv.sh` to set up environment (usually this goes into `.bash_profile`, but I don't want its paths to interfere with Anaconda Python 3 or virtualenv):

```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

```
source use-pyenv.sh
pyenv update
pyenv --version
```
```
pyenv 20160726
```
```
pyenv install -l
pyenv install 2.7.6
pyenv install 3.4.0
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

#### Docker

**TODO** is there any point in doing this? It's just another VM in effect!

---

## Summary of deployment environments

This summarises the environments into which recipy was deployed, which are described in the following sections. The default package location for each Python version was used, except for the virtualenv and virtualenvwrapper environments where recipy was installed into a virtual environment in the user's local directory.

| Operating System         | Python                          | Deployed |
| ------------------------ | ------------------------------- | -------- |
| Windows 7 Enterprise SP1 |                                 |          |
|                          | 3.5.2 (Anaconda 4.1.1)          | Yes      |
| Ubuntu 14.04.3 LTS       |                                 |          |
| (default Python users)   |                                 |          |
|                          | 2.7.6                           | Yes      |
|                          | 3.4.3                           | Yes      |
|                          | 2.7.6 + virtualenv 15.0.2       |          |
|                          | 3.4.3 + virtualenv 15.0.2       | Yes      |
|                          | 2.7.6 + virtualenvwrapper 4.7.1 |          |
|                          | 3.4.3 + virtualenvwrapper 4.7.1 | Yes      |
| Ubuntu 14.04.3 LTS       |                                 |          |
| (local Python users)     |                                 |          |
|                          | 3.5.2 (Anaconda 4.1.1)          | Yes      |
|                          | 2.7.4 (pyenv 20160726)          |          |
|                          | 3.4.0 (pyenv 20160726)          | Yes      |

Possible environments for future deployments include:

* Pre-installed Python on Mac OS X.
* Current [production releases](http://legacy.python.org/download/releases/) of Python 3.4.0 and 2.7.6 for Mac OS X and Windows.
* Anaconda 4.1.1 for Mac OS X.
* Enthought [Canopy](https://www.enthought.com/products/canopy/) 1.7.4 for Windows, Linux and Mac. Canopy is a scientific Python bundle with Python 2.7.11 and 200+ Python packages including numpy, pandas, matplotlib, Pillow, scikit-learn, scikit-image, GDAL (of the packages logged by recipy, only NiBabel is not present).
* pyenv [deployment on Mac OS X](https://github.com/yyuu/pyenv#homebrew-on-mac-os-x) via the [HomeBrew](http://brew.sh/) package manager.
* [conda](http://conda.pydata.org/docs/) 4.1. conda is both a package manager and, like virtualenv, a virtual environment manager. It can be used with Python 2.7, 3.4 or 3.5 under Windows, Linux and Mac. Unlike virtualenv, conda can be used to create virtual environments if using Anaconda.

---

## Deploy recipy and run simple script

The following scripts were used to check that a recipy deployment was operating correctly with numpy.

`check-recipy.py`:

```
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file.csv", data, delimiter=",")
```

`check-recipy-import.py`:

```
import recipy
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file-import.csv", data, delimiter=",")
```

The following script was used to check recipy's wrapper's for Python's `open` command:

`check-recipy-open.py`:

```
import recipy
with recipy.open('file-open.txt', 'w') as f:
    f.write("This is a test")
```

### Install recipy package 0.2.3 under Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)

In the following, the Git Bash prompt was used.

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

Copy scripts to `deployment/`.

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

**Suggestion** `README.md` states that:

> it will produce an output called test.npy. To find out the details of the run which created this file you can search using
> recipy search test.npy

Rephrase this to:

> The sample script above will produce...

to reinforce that it's the sample script, and not recipy, that produces `test.npy`.

**Suggestion** Log the versions of the libraries (e.g. numpy) used too. **Deprecated:** The current version of recipy on GitHub now does this.

### Use GUI

```
recipy gui
```

A browser appears.

**Issue** The searches did not work. I tried it using `mjj`, `file-import.csv`, `C:\Users\mjj\deployment\file` for Windows and `/home/ubuntu/deployment/file` for Ubuntu and for each got a `HTTP 500 Interal Server Error`.

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

* Enter Notes: `This was Mike's first use of recipy.`
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

**Suggestion** Explain the difference between `fuzzy` and `regex` searching in the documentation, and provide examples of fuzzy and regular expression patterns.

### Annotate information

```
recipy annotate
```
```
'$EDITOR' is not recognized as an internal or external command, operable program or batch file.
No annotation entered, exiting.
```

**Suggestion** Document the need to set the `EDITOR` variable and that user can override their default e.g. if they want nano rather than vi on Ubuntu.

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

**Issue** Under Windows, I tried using `.bashrc` and `.bash_profile` to set `EDITOR`, and also tried running these commands within the Anaconda Python Prompt, rather than the Git Bash prompt, but with no success.

**Suggestion** Resolve this issue or, if it cannot be resolved, recommend that Windows/Git Bash/Anaconda users use `recipy gui`.

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

**Suggestion** This gives rise to a different error when using the current version on GitHub (see below). It looks like this feature and information was added to recipy and `README.md` since the 0.2.3 package was created. Add a link to the recipy [pypi](https://pypi.python.org/pypi/recipy) page to point to the `README.md` corresponding to the version in the [v0.2.3](https://github.com/recipy/recipy/releases/tag/v0.2.3) tag.

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

Edit `check-recipy-import.py` and change first `range` function call to be `range(5,9)`.

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

**Suggestion** Describe how and when `--diff` will show the `diff` i.e. if the commit is newer than the most recent files is what it seems to do. I found an example by trial and error.

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
cd
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
```
pip freeze | grep recipy
```
```
```
```
rm -rf ~/.recipy
```

### Install recipy latest version under Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)

The latest version of recipy, from GitHub, can be deployed as follows:

```
git clone https://github.com/recipy/recipy
cd recipy
git log -1 --format="%ai %H"
```
```
2016-05-31 15:48:50 +0200 dd2b7ae96b99ca6d3678f8236ca97ec5ad672454
```

```
python setup.py install
```

The previous steps were re-run. Only information on where commands, outputs or behaviour deviated from the run above (i.e. commands succeeded where they formerly failed or vice versa), and issues and suggestions arising are documented.

```
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

**Suggestion** The recipy 0.2.3 package was [tagged](https://github.com/recipy/recipy/releases/tag/v0.2.3) on 17/11/2015. There have been many commits since then, so the current state of the repository, on GitHub, is no longer version 0.2.3 but, at least, 0.2.4. I'd recommend upping the version number in setup.py immediately after you tag a release, or at the first time you make a commit after tagging the release.

```
recipy search file-import.csv
```
```
Traceback (most recent call last):
  File "C:\Users\mjj\Anaconda3\Scripts\recipy-script.py", line 9, in <module>
    load_entry_point('recipy==0.2.3', 'console_scripts', 'recipy')()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 116, in main
    search(args)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 255, in search
    lambda x: listsearch(os.path.abspath(filename), x)))
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\database.py", line 407,
in search
    elements = [element for element in self.all() if cond(element)]
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\database.py", line 407,
in <listcomp>
    elements = [element for element in self.all() if cond(element)]
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\queries.py", line 45, in __call__
    return self.test(value)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\queries.py", line 136, in impl
    return test(value)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\queries.py", line 305, in <lambda>
    return self._generate_test(lambda value: _cmp(value),
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\queries.py", line 299, in _cmp
    return is_sequence(value) and any(cond(e) for e in value)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\queries.py", line 299, in <genexpr>
    return is_sequence(value) and any(cond(e) for e in value)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 255, in <lambda>
    lambda x: listsearch(os.path.abspath(filename), x)))
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCommon\tinydb_utils.py", line 45, in listsearch
    return bool(re.search(query, item) or
  File "C:\Users\mjj\Anaconda3\lib\re.py", line 173, in search
    return _compile(pattern, flags).search(string)
  File "C:\Users\mjj\Anaconda3\lib\re.py", line 293, in _compile
    p = sre_compile.compile(pattern, flags)
  File "C:\Users\mjj\Anaconda3\lib\sre_compile.py", line 536, in compile
    p = sre_parse.parse(p, flags)
  File "C:\Users\mjj\Anaconda3\lib\sre_parse.py", line 829, in parse
    p = _parse_sub(source, pattern, 0)
  File "C:\Users\mjj\Anaconda3\lib\sre_parse.py", line 437, in _parse_sub
    itemsappend(_parse(source, state))
  File "C:\Users\mjj\Anaconda3\lib\sre_parse.py", line 524, in _parse
    code = _escape(source, this, state)
  File "C:\Users\mjj\Anaconda3\lib\sre_parse.py", line 388, in _escape
    raise source.error("incomplete escape %s" % escape, len(escape))
sre_constants.error: incomplete escape \U at position 2
```

**Issue** Under Windows `recipy search file-import.csv` raises `sre_constants.error: incomplete escape \U at position 2` using Git Bash and Anaconda Python prompts.

```
cat ../Downloads/runs.json
```
```
[
  {
    "exit_date": "{TinyDate}:2016-08-12T08:30:23",
    ...
    "libraries": [
      "recipy v0.2.3",
      "numpy v1.11.1"
    ],
    ...
    "warnings": []
  }
]
```

Note the additional fields, not in the 0.2.3 package release.

`recipy gui` searches for `mjj` and `file-import.csv` now worked.

**Issue** The search did not work for `C:\Users\mjj\deployment\file`, but did for `C:\\Users\\mjj\\deployment\\file`. Update the search code to escape `\` in file paths.

While `recipy search` failed, above, `recipy latest` worked.

```
recipy latest -j
```
```
Traceback (most recent call last):
  File "C:\Users\mjj\Anaconda3\Scripts\recipy-script.py", line 9, in <module>
    load_entry_point('recipy==0.2.3', 'console_scripts', 'recipy')()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 118, in main
    latest(args)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 228, in latest
    output = dumps(run, indent=2, sort_keys=True)
  File "C:\Users\mjj\Anaconda3\lib\json\__init__.py", line 237, in dumps
    **kw).encode(obj)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 200, in encode
    chunks = list(chunks)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 429, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 403, in _iterencode_dict
    yield from chunks
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 436, in _iterencode
    o = _default(o)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 179, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: datetime.datetime(2016, 8, 12, 8, 49, 22) is not JSON serializable
```
```
recipy search -i 35eb0a07-d136-4a9e-835c-d84f108ec89 -j
```
```
Traceback (most recent call last):
  File "C:\Users\mjj\Anaconda3\Scripts\recipy-script.py", line 9, in <module>
    load_entry_point('recipy==0.2.3', 'console_scripts', 'recipy')()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 116, in main
    search(args)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCmd\recipycmd.py", line 267, in search
    output = dumps(res_to_output, indent=2, sort_keys=True)
  File "C:\Users\mjj\Anaconda3\lib\json\__init__.py", line 237, in dumps
    **kw).encode(obj)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 200, in encode
    chunks = list(chunks)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 427, in _iterencode
    yield from _iterencode_list(o, _current_indent_level)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 324, in _iterencode_list
    yield from chunks
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 403, in _iterencode_dict
    yield from chunks
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 436, in _iterencode
    o = _default(o)
  File "C:\Users\mjj\Anaconda3\lib\json\encoder.py", line 179, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: datetime.datetime(2016, 8, 12, 8, 49, 22) is not JSON serializable
```

**Issue** `recipy latest -j` and `recipy search -i 5f551f52-2e4b-429e-bd4e-0a22ae12f19 -j` both raise `TypeError: datetime.datetime(2016, 8, 12, 8, 49, 22) is not JSON serializable` using Git Bash and Anaconda Python prompts in Windows, and default Python 2.7.6 in Ubuntu 14.04.3 LTS.

```
recipy annotate
```
```
'$EDITOR' is not recognized as an internal or external command,
operable program or batch file.
No annotation entered, exiting.
```

**Issue** Under Windows, I tried using `.bashrc` and `.bash_profile` to set `EDITOR`, and also tried running these commands within the Anaconda Python Prompt, rather than the Git Bash prompt, but with no success.

**Suggestion** Resolve this issue or, if it cannot be resolved, recommend that Windows/Git Bash/Anaconda users use `recipy gui`.

```
python check-recipy-open.py
```
```
recipy run inserted, with ID 02c4d038-6934-4057-9c85-41d717ab6052
Traceback (most recent call last):
  File "check-recipy-open.py", line 2, in <module>
    with recipy.open('file-open.txt', 'w') as f:
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipy\utils.py", line 20, in open
    mode = kwargs['mode']
KeyError: 'mode'
```

**Issue** `with recipy.open('file-open.txt', 'w') as f:` gives a `KeyError: 'mode'` error.

Edit `check-recipy-open.py` and change:

```
with recipy.open('file-open.txt', 'w') as f:
```

to

```
with recipy.open('file-open.txt', mode='w') as f:
```

so that the `mode` parameter is named.

```
python check-recipy-open.py
```
```
recipy run inserted, with ID c306c23b-9f24-4781-83e3-a4c9b19ea309
C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipyCommon\libraryversions.py:30: UserWarning: requesting version of a module that has not been imported (recipy.open)
  'imported ({})'.format(modulename))
Traceback (most recent call last):
  File "check-recipy-open.py", line 2, in <module>
    with recipy.open('file-open.txt', mode='w') as f:
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipy\utils.py", line 35, in open
    log_output(args[0], 'recipy.open')
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipy\log.py", line 177, in log_output
    db.update(append("libraries", get_version(source), no_duplicates=True), eids=[RUN_ID])
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\database.py", line 377,
in update
    cond, eids
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\database.py", line 230,
in process_elements
    data = self._read()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\database.py", line 277,
in _read
    return self._storage.read()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\database.py", line 31, in read
    raw_data = (self._storage.read() or {})[self._table_name]
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb_serialization\__init__.py", line 139, in read
    data = self.storage.read()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\tinydb\storages.py", line 93, in read
    self._handle.seek(0, 2)
ValueError: I/O operation on closed file.
```

**Issue** `with recipy.open('file-open.txt', mode='w') as f:` gives an `ValueError: I/O operation on closed file` error.

**Issue** `recipy.open` does not seem to support the same signature as Python `open`. I would expect it would support the same signature.

Uninstall:

```
cd
find Anaconda3/ -name "*recipy*"
rm -rf Anaconda3/Lib/site-packages/recipy-0.2.3-py3.5.egg
rm -f Anaconda3/Scripts/recipy-script.py
rm -f Anaconda3/Scripts/recipy.exe
pip freeze | grep recipy
```
```
```

---

## Install recipy under other environments

The previous steps were re-run under the other environments. Only information on where commands, outputs or behaviour deviated from the run above (i.e. commands succeeded where they formerly failed or vice versa), and issues and suggestions arising are documented.

### Ubuntu 14.04.3 LTS + 2.7.6

**recipy package 2.3.0**

```
sudo pip install recipy
```

**Suggestion** Document that, if default/system-wide Python distributions are being used on Linux then `sudo` access is required when running `pip`.

```
cat /usr/local/bin/recipy
```
```
#!/usr/bin/python
```

Script uses default Python, Python 2.7.6.

```
recipy annotate
```
```
sh: 1: /tmp/tmpEk9ykM: Permission denied
No annotation entered, exiting.
```
```
ls -l /tmp/tmpEk9ykM 
```
```
-rw------- 1 ubuntu ubuntu 475 Aug 12 03:43 /tmp/tmpEk9ykM
```
```
echo $EDITOR
EDITOR=nano
recipy annotate
```
```
sh: 1: /tmp/tmpEk9ykM: Permission denied
No annotation entered, exiting.
```
```
export EDITOR=nano
recipy annotate
```

**Suggestion** Document need for `EDITOR` variable to be set.

Enter `This is Mike's first annotation`.

```
recipy latest
```
```
...
Notes:
This is Mike's first annotation.
...
```
```
recipy annotate
```

Enter `This is Mike's second annotation`.

```
recipy latest
```
```
...
Notes:
This is Mike's second annotation.
...
```

**Suggestion** Document that only the latest run can be annotated via `recipy annotate`.

**Suggestion** Document that the notes are completely overwritten, so if the user wants to retain their current notes they should copy them from the lower-half of the editor.

**Suggestion** Have editor show current notes so these can be edited without the need for the user to copy then as suggested above.

```
find /usr/local -name "*recipy*"
```
```
/usr/local/lib/python2.7/dist-packages/recipyCmd
/usr/local/lib/python2.7/dist-packages/recipyCmd/recipycmd.pyc
/usr/local/lib/python2.7/dist-packages/recipyCmd/recipycmd.py
/usr/local/lib/python2.7/dist-packages/recipyGui
/usr/local/lib/python2.7/dist-packages/recipyGui/tests/test_recipyGui.pyc
/usr/local/lib/python2.7/dist-packages/recipyGui/tests/test_recipyGui.py
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3.egg-info
/usr/local/lib/python2.7/dist-packages/recipy
/usr/local/lib/python2.7/dist-packages/recipyCommon
/usr/local/bin/recipy
```
```
sudo pip uninstall recipy
```
```
find /usr/local -name "*recipy*"
```

**recipy latest version*

```
sudo python setup.py install
```

**Suggestion** Document that, if default/system-wide Python distributions are being used on Linux then `sudo` access is required when running `python setup.py install`.

```
$ recipy search file-import.csv
```
```
...shows data...
```

```
python check-recipy-open.py
```
```
recipy run inserted, with ID 817359aa-69ef-4d33-a062-026f343231c4
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyCommon/libraryversions.py:30: UserWarning: requesting version of a module that has not been imported (recipy.open)
  'imported ({})'.format(modulename))
Traceback (most recent call last):
  File "check-recipy-open.py", line 2, in <module>
    with recipy.open('file-open.txt', 'w') as f:
  File "/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipy/utils.py", line 35, in open
    log_output(args[0], 'recipy.open')
  File "/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipy/log.py", line 177, in log_output
    db.update(append("libraries", get_version(source), no_duplicates=True), eids=[RUN_ID])
  File "/usr/local/lib/python2.7/dist-packages/tinydb/database.py", line 377, in update
    cond, eids
  File "/usr/local/lib/python2.7/dist-packages/tinydb/database.py", line 230, in process_elements
    data = self._read()
  File "/usr/local/lib/python2.7/dist-packages/tinydb/database.py", line 277, in _read
    return self._storage.read()
  File "/usr/local/lib/python2.7/dist-packages/tinydb/database.py", line 31, in read
    raw_data = (self._storage.read() or {})[self._table_name]
  File "/usr/local/lib/python2.7/dist-packages/tinydb_serialization/__init__.py", line 139, in read
    data = self.storage.read()
  File "/usr/local/lib/python2.7/dist-packages/tinydb/storages.py", line 93, in read
    self._handle.seek(0, 2)
ValueError: I/O operation on closed file
```

**Issue** `with recipy.open('file-open.txt', 'w') as f:` gives an `ValueError: I/O operation on closed file` error under Ubuntu 14.04.3 LTS and Python 2.7.6 and recipy latest version. This differs from Ubuntu 14.04.3 LTS and Python 3.4.3 and Windows 7 Enterprise SP1 + Python 3.5.2 (Anaconda 4.1.1) which give `KeyError: 'mode'`, and only give this current error if `mode='w'` is provided.

```
find /usr/local -name "*recipy*"
```
```
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyCmd
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyCmd/recipycmd.py
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyGui
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyGui/tests/test_recipyGui.py
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipy
/usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg/recipyCommon
```
```
sudo rm -rf /usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg
sudo rm -f /usr/local/bin/recipy
find /usr/local -name "*recipy*"
```
```
```

### Ubuntu 14.04.3 LTS + 3.4.3

For this run, `python3` and `pip3` were used instead of `python` and `pip`.

**recipy package 2.3.0**

```
python3 --version
```
```
Python 3.4.3
```
```
sudo pip3 install recipy
```

**Suggestion** Document that, if default/system-wide Python 2 and 3 distributions co-exist on Linux, then the user may need to use `pip3` and `python3`.

```
cat /usr/local/bin/recipy
```
```
#!/usr/bin/python3
```

Script uses Python 3.4.3.

**recipy latest version**

```
sudo python3 setup.py install
```

**Suggestion** Document that, if default/system-wide Python distributions are being used on Linux then `sudo` access is required when running `python3 setup.py install`.

```
find /usr/local -name "*recipy*"
```
```
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyCmd
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyCmd/recipycmd.py
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyGui
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/test_recipyGui.py
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipy
/usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg/recipyCommon
```
```
sudo rm -rf /usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg
sudo rm -f /usr/local/bin/recipy
find /usr/local -name "*recipy*"
```
```
pip3 freeze | grep recipy
```
```
```

### Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2

Create a new virtualenv environment:

```
mkdir recipy-venv
cd recipy-venv
virtualenv venv --python=/usr/bin/python3 --system-site-packages
```

Activate virtualenv:

```
source recipy-venv/venv/bin/activate
which python
```
```
/home/ubuntu/recipy-venv/venv/bin/python
```
```
python --version
```
```
Python 3.4.3
```
```
which pip
```
```
/home/ubuntu/recipy-venv/venv/bin/pip
```
```
pip --version
```
```
pip 8.1.2 from /home/ubuntu/recipy-venv/venv/lib/python3.4/site-packages (python 3.4)
```

**recipy package 2.3.0**

```
find recipy-venv/ -name "*recipy*"
```
```
recipy-venv/
recipy-venv/venv/lib/python3.4/site-packages/recipyCmd
recipy-venv/venv/lib/python3.4/site-packages/recipyCmd/recipycmd.py
recipy-venv/venv/lib/python3.4/site-packages/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
recipy-venv/venv/lib/python3.4/site-packages/recipyGui
recipy-venv/venv/lib/python3.4/site-packages/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
recipy-venv/venv/lib/python3.4/site-packages/recipyGui/tests/test_recipyGui.py
recipy-venv/venv/lib/python3.4/site-packages/recipy
recipy-venv/venv/lib/python3.4/site-packages/recipyCommon
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3.dist-info
recipy-venv/venv/bin/recipy
```
```
pip uninstall recipy
```
```
find recipy-venv/ -name "*recipy*"
```
```
```

Deactivate virtualenv:

```
deactivate
```

**recipy latest version**

```
source recipy-venv/venv/bin/activate
```

```
find recipy-venv/ -name "*recipy*"
```
```
recipy-venv/
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/recipycmd.py
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/test_recipyGui.py
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipy
recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCommon
recipy-venv/venv/bin/recipy
```
```
rm -rf recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f recipy-venv/venv/bin/recipy
```
```
find recipy-venv/ -name "*recipy*"
```
```
recipy-venv/
```

Deactivate virtualenv:

```
deactivate
```

### Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper

Create a new virtualenv environment:

```
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv recipy-wrapper-env --python=/usr/bin/python3 --system-site-packages
```

Activate virtualenv:

```
workon recipy-wrapper-env
```
```
python --version
```
```
Python 3.4.3
```

Only the following commands were run:

```
pip install recipy
recipy --version
python check-recipy-import.py
python -m check-recipy.py
python check-recipy-open.py
recipy latest
recipy gui
```

**recipy package 2.3.0**

```
find Envs/ -name "*recipy*"
```
```
Envs/recipy-wrapper-env
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyCmd
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyCmd/recipycmd.py
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyGui
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyGui/tests/test_recipyGui.py
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipyCommon
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3.dist-info
Envs/recipy-wrapper-env/bin/recipy
```
```
pip uninstall recipy
```
```
find Envs/ -name "*recipy*"
```
```
Envs/recipy-wrapper-env
```

**recipy latest version**

```
find Envs/ -name "*recipy*"
```
```
Envs/recipy-wrapper-env
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/recipycmd.py
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/test_recipyGui.py
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipy
Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCommon
Envs/recipy-wrapper-env/bin/recipy
```
```
rm -rf Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f Envs/recipy-wrapper-env/bin/recipy
```
```
find Envs/ -name "*recipy*"
```
```
Envs/recipy-wrapper-env
```

### Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1

Configure use of Anaconda 4.1.1:

```
source use-anaconda3.sh 
which python
```
```
/home/ubuntu/anaconda3/bin/python
```
```
python --version
```
```
Python 3.5.2 :: Anaconda 4.1.1 (64-bit)
```
```
which pip
```
```
/home/ubuntu/anaconda3/bin/pip
```
```
pip --version
```
```
pip 8.1.2 from /home/ubuntu/anaconda3/lib/python3.5/site-packages (python 3.5)
```

**recipy package 2.3.0**

```
find anaconda3/ -name "*recipy*"
```
```
anaconda3/lib/python3.5/site-packages/recipy
anaconda3/lib/python3.5/site-packages/recipyGui
anaconda3/lib/python3.5/site-packages/recipyGui/tests/__pycache__/test_recipyGui.cpython-35.pyc
anaconda3/lib/python3.5/site-packages/recipyGui/tests/test_recipyGui.py
anaconda3/lib/python3.5/site-packages/recipyCmd
anaconda3/lib/python3.5/site-packages/recipyCmd/__pycache__/recipycmd.cpython-35.pyc
anaconda3/lib/python3.5/site-packages/recipyCmd/recipycmd.py
anaconda3/lib/python3.5/site-packages/recipyCommon
anaconda3/lib/python3.5/site-packages/recipy-0.2.3.dist-info
anaconda3/bin/recipy
```
```
pip uninstall recipy
find anaconda3/ -name "*recipy*"
```
```
```

**recipy latest version**

```
find anaconda3/ -name "*recipy*"
```
```
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipy
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyGui
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-35.pyc
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyGui/tests/test_recipyGui.py
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCmd
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCmd/__pycache__/recipycmd.cpython-35.pyc
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCmd/recipycmd.py
anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCommon
anaconda3/bin/recipy
```
```
rm -rf anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg
rm -f anaconda3/bin/recipy
```
```
find anaconda3/ -name "*recipy*"
```
```
```

### Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726

Configure use of pyenv:

```
source use-anaconda3.sh 
pyenv local 3.4.0
which python
```
```
/home/ubuntu/.pyenv/shims/python
```
```
python --version
```
```
Python 3.4.0
```
```
which pip
```
```
/home/ubuntu/.pyenv/shims/pip
```
```
pip --version
```
```
pip 1.5.4 from /home/ubuntu/.pyenv/versions/3.4.0/lib/python3.4/site-packages (python 3.4)
```

**recipy package 2.3.0**

```
find .pyenv -name "*recipy*"
```
```
.pyenv/shims/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyGui
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyGui/tests/test_recipyGui.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCmd
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCmd/recipycmd.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCommon
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg-info
.pyenv/versions/3.4.0/bin/recipy
```
```
pip uninstall recipy
```
```
find .pyenv -name "*recipy*"
```
```
```

**recipy latest version**

```
pip freeze | grep recipy
```
```
recipy==0.2.3
```
```
recipy --version
```
```
bash: /home/ubuntu/.pyenv/shims/recipy: No such file or directory
```
```
which recipy
```
```
```
```
find .pyenv -name "*recipy*"
```
```
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/test_recipyGui.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/recipycmd.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCommon
.pyenv/versions/3.4.0/bin/recipy
```

Compare to locations of recipy package installed using `pip`:

```
.pyenv/shims/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyGui
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyGui/tests/test_recipyGui.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCmd
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCmd/recipycmd.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipyCommon
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg-info
.pyenv/versions/3.4.0/bin/recipy
```

The difference is `.pyenv/shims/recipy`. StackOverflow [Pyenv shim not created when installing package using setup.py](http://stackoverflow.com/questions/29753592/pyenv-shim-not-created-when-installing-package-using-setup-py) comments thatL

> Versions of pyenv before v20141211 do not automatically "rehash" (that is, update shims) when a new package is installed. To get pyenv to automatically rehash, either upgrade to a newer version of pyenv, or install the pyenv-pip-refresh plugin.
> To rehash manually, use this command for bash:
> `pyenv rehash && hash -r`

My pyenv is newer than this:

```
pyenv --version
```
```
pyenv 20160726
```

Try the manual solution:

```
pyenv rehash && hash -r
which recipy
```
```
/home/ubuntu/.pyenv/shims/recipy
```
```
recipy --version
```
```
recipy v0.2.3
```

**Issue** `python setup.py install` and pyenv do not make the `recipy` executable available. Document the workaround command `pyenv rehash && hash -r` in the short-term and track down a possible automated solution in the longer term.

```
find .pyenv -name "*recipy*"
```
```
.pyenv/shims/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipy
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/__pycache__/test_recipyGui.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyGui/tests/test_recipyGui.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/__pycache__/recipycmd.cpython-34.pyc
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCmd/recipycmd.py
.pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg/recipyCommon
.pyenv/versions/3.4.0/bin/recipy
```
```
rm -f .pyenv/shims/recipy
rm -rf .pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f .pyenv/versions/3.4.0/bin/recipy
```
```
find .pyenv -name "*recipy*"
```
```
```

---

## Documentation

**TODO** Look at README.md sections:

* Configuration
* How it works

README.md comments that 

> If you want to log inputs and outputs of files read or written with built-in open, you need to do a little more work. Either use `recipy.open` (only requires import recipy at the top of your script), or add `from recipy import open` and just use `open`. This workaround is required, because many libraries use built-in open internally, and you only want to record the files you explicitly opened yourself.
> If you use Python 2, you can pass an `encoding` parameter to `recipy.open`. In this case `codecs` is used to open the file with proper encoding.

**Suggestion** Describe whether `recipy.open` has the same function signature as `open` (with the additional `encoding` parameter) or whether it changes it, in which case describe the altered signature.

---

## Other examples

**TODO** check if this information is auto-generated. If so then suggest it auto-generate a .md file for the repository (yes, an auto-generated artefact in the repository!)

From `recipy gui` at http://127.0.0.1:9000/patched_modules, the packages, input and output functions logged by the current version are:

pandas:

* read_csv, read_table, read_excel, read_hdf, read_pickle, read_stata, read_msgpack
* DataFrame.to_csv, DataFrame.to_excel, DataFrame.to_hdf, DataFrame.to_msgpack, DataFrame.to_stata, DataFrame.to_pickle, Panel.to_excel, Panel.to_hdf, Panel.to_msgpack, Panel.to_pickle, Series.to_csv, Series.to_hdf, Series.to_msgpack, Series.to_pickle

matplotlib.pyplot:

* None
* savefig

numpy:

* genfromtxt, loadtxt, fromfile
* save, savez, savez_compressed, savetxt

<td>lxml.etree</td>
parse, iterparse
None

<td>bs4</td>
BeautifulSoup
None

gdal:

* Open
* Driver.Create, Driver.CreateCopy

sklearn:

* datasets.load_svmlight_file
* datasets.dump_svmlight_file

nibabel:

* nifti1.Nifti1Image.from_filename, nifti2.Nifti2Image.from_filename, freesurfer.mghformat.MGHImage.from_filename, spm99analyze.Spm99AnalyzeImage.from_filename, minc1.Minc1Image.from_filename, minc2.Minc2Image.from_filename, analyze.AnalyzeImage.from_filename, parrec.PARRECImage.from_filename, spm2analyze.Spm2AnalyzeImage.from_filename
* nifti1.Nifti1Image.to_filename, nifti2.Nifti2Image.to_filename, freesurfer.mghformat.MGHImage.to_filename, spm99analyze.Spm99AnalyzeImage.to_filename, minc1.Minc1Image.to_filename, minc2.Minc2Image.to_filename, analyze.AnalyzeImage.to_filename, parrec.PARRECImage.to_filename, spm2analyze.Spm2AnalyzeImage.to_filename

**TODO** Ask where Pillow and scikit-image are. Add Suggestion that this be clarified on README.md.

**TODO** Ask what bs4 and lxml.etree are. Add Suggestion that this be added to README.md.


**TODO** Write and run one sample script for more package/function recipy can log (look at the recipy source code) These can form basis of test scripts.

**Suggestion** Provide a list of the functions for each package that recipy logs. While these are visible via `recipy gui` at http://127.0.0.1:9000/patched_modules, documenting them so they can be viewed online would be useful for users and developers.

**Suggestion** Develop a tool that uses reflection to traverse the functions of a package and print out the names of functions (and, if possible, their "help" information) that may be input/output functions that should be logged by recipy (e.g. functions with names such as `input/output`, `read/write`, `load/save`). This could help those who want to develop recipy wrappers for additional packages.

---

## General

**Suggestion** Provide guidelines on how to use recipy in a research workflow e.g. how to use recipy and Git to record provenance and recommended ways of archiving input/output files etc.

**TODO** Restructure foregoing into command-list, deviations for each platform, and issues (with list of versions to which each issue applied)

---

# Appendix - commands run for each deployment

In what follows `python3` and `pip3` were used instead of `python` and `pip` on Ubuntu 14.04.3 LTS + 3.4.3.

Commands run to check Python and pip versions:

```
which python
python --version

which pip
pip --version
```

Commands run to install recipy 0.2.3:

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1
# Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726
pip install recipy

# Ubuntu 14.04.3 LTS + 2.7.6
sudo pip install recipy

# Ubuntu 14.04.3 LTS + 3.4.3
sudo pip3 install recipy

pip freeze | grep recipy
which recipy
recipy --version
```

Commands run to install recipy latest version:

```
git clone https://github.com/recipy/recipy
cd recipy
git log -1 --format="%ai %H"

# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1
# Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726
python setup.py install

# Ubuntu 14.04.3 LTS + 2.7.6
sudo python setup.py install

# Ubuntu 14.04.3 LTS + 3.4.3
sudo python3 setup.py install
```

`recipy` commands run:

```
recipy --version
python check-recipy-import.py
recipy search file-import.csv
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
EDITOR=notepad.exe # Windows only
EDITOR=notepad.exe # Ubuntu only
recipy annotate
export EDITOR=notepad.exe # Windows only
export EDITOR=nano # Ubuntu only
recipy annotate

python -m recipy check-recipy.py
python check-recipy-open.py

recipy gui
```

`recipy` commands to see behaviour if `deployment` directory, in which scripts have been run, no longer exists:

```
cd ..
mv deployment tmp
recipy search C:/Users/mjj/deployment/file-import.csv # Windows only
recipy search /home/ubuntu/deployment/file-import.csv # Ubuntu only
mv tmp deployment
```

`recipy` commands to see behaviour within Git repositories:

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
recipy latest --diff
git commit -m "Changed check-recipy-import.py range to 5,9" .
recipy latest --diff
python check-recipy-import.py
recipy latest --diff

cd ..
git clone C:/Users/mjj/deployment deployment-clone # Windows only
git clone /home/ubuntu/deployment/ /home/ubuntu/deployment-clone # Ubuntu only
cd deployment-clone/
python check-recipy-import.py
recipy latest
cd
```

`recipy gui` commands run:

* Search for mjj, file-import.csv, C:\Users\mjj\deployment\file-import.csv (Windows), C:\\Users\\mjj\\deployment\\file-import.csv (Windows)
* Search for ubuntu, file-import.csv, /home/ubuntu/deployment/file-import.csv (Ubuntu)
* Click View details
* Click Save as JSON
* Enter Notes: `This was Mike's first use of recipy.`
* Click Save notes
* Click Save as JSON
* Look at JSON files.

Commands run to find recipy files, before and after uninstall:

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
find Anaconda3/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 2.7.6
# Ubuntu 14.04.3 LTS + 3.4.3
find /usr/local -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
find recipy-venv/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
find Envs/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1
find anaconda3/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726
find .pyenv -name "*recipy*"
```

Commands run to uninstall recipy 0.2.3:

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1
# Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726
pip uninstall recipy

# Ubuntu 14.04.3 LTS + 2.7.6
sudo pip uninstall recipy

# Ubuntu 14.04.3 LTS + 3.4.3
sudo pip3 uninstall recipy
```

Commands run to uninstall recipy latest version:

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
rm -rf Anaconda3/Lib/site-packages/recipy-0.2.3-py3.5.egg
rm -f Anaconda3/Scripts/recipy-script.py
rm -f Anaconda3/Scripts/recipy.exe

# Ubuntu 14.04.3 LTS + 2.7.6
sudo rm -rf /usr/local/lib/python2.7/dist-packages/recipy-0.2.3-py2.7.egg
sudo rm -f /usr/local/bin/recipy

# Ubuntu 14.04.3 LTS + 3.4.3
sudo rm -rf /usr/local/lib/python3.4/dist-packages/recipy-0.2.3-py3.4.egg
sudo rm -f /usr/local/bin/recipy

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
rm -rf recipy-venv/venv/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f recipy-venv/venv/bin/recipy

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
rm -rf Envs/recipy-wrapper-env/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f Envs/recipy-wrapper-env/bin/recipy

# Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1
rm -rf anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg
rm -f anaconda3/bin/recipy

# Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726
rm -f .pyenv/shims/recipy
rm -rf .pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f .pyenv/versions/3.4.0/bin/recipy

pip freeze | grep recipy
```

Commands run to clean up environment:

```
unset EDITOR
rm -rf ~/.recipy
```
