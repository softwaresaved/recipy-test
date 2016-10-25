# recipy scripts

Mike Jackson, The Software Sustainability Institute / EPCC, The University of Edinburgh

## Overview

A set of small scripts have been written to invoke every input and output function logged by the current release of recipy, in addition to `scikit-image` even though, as noted earlier, these are currently commented out. These were written so that I'd have code that can be evolved into automated tests.

gdal

* Open
* Driver.Create, Driver.CreateCopy

nibabel

* nifti1.Nifti1Image.from_filename, nifti2.Nifti2Image.from_filename, freesurfer.mghformat.MGHImage.from_filename, spm99analyze.Spm99AnalyzeImage.from_filename, minc1.Minc1Image.from_filename, minc2.Minc2Image.from_filename, analyze.AnalyzeImage.from_filename, parrec.PARRECImage.from_filename, spm2analyze.Spm2AnalyzeImage.from_filename
* nifti1.Nifti1Image.to_filename, nifti2.Nifti2Image.to_filename, freesurfer.mghformat.MGHImage.to_filename, spm99analyze.Spm99AnalyzeImage.to_filename, minc1.Minc1Image.to_filename, minc2.Minc2Image.to_filename, analyze.AnalyzeImage.to_filename, parrec.PARRECImage.to_filename, spm2analyze.Spm2AnalyzeImage.to_filename

skimage (currently commented out of recipy)

* io.imread, io.load_sift, io.load_surf, external.tifffile.imread
* io.imsave, external.tifffile.imsave

sklearn

* datasets.load_svmlight_file
* datasets.dump_svmlight_file

These scripts, and accompanying data files, can be seen in [scripts/](./scripts/).

## Script failures

Running the scripts under various environments shows issues that arise in terms of Python package versioning - both between Python versions and between versions installed via `pip` or `easy_install` and those provided via third-party packages e.g. within Ubuntu `python-` packages or Anaconda.

The environments used were:

* Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 3.4.3
* Docker 1.12.0 and Ubuntu 14.04.4 LTS + 3.4.3
* Ubuntu 14.04.3 LTS + 2.7.12 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 2.7.6 (pyenv 20160726)
* Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)

### NiBabel `AttributeError`

```
$ python run_nibabel.py nifti2.Nifti2Image.from_filename data/nibabel/nifti2_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 55, in invoke_nifti2_Nifti2Image_from_filename
    data = nib.Nifti2Image.from_filename(file_name)
AttributeError: 'module' object has no attribute 'Nifti2Image'

$ python run_nibabel.py nifti2.Nifti2Image.to_filename tmp/nibabel/nifti2_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 61, in invoke_nifti2_Nifti2Image_to_filename
    img = nib.Nifti2Image(get_data(), get_affine())
AttributeError: 'module' object has no attribute 'Nifti2Image'

$ python run_nibabel.py minc1.Minc1Image.from_filename data/nibabel/minc1_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 97, in invoke_minc1_Minc1Image_from_filename
    data = nib.minc1.Minc1Image.from_filename(file_name)
AttributeError: 'module' object has no attribute 'minc1'

$ python run_nibabel.py minc1.Minc1Image.to_filename tmp/nibabel/minc1_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 103, in invoke_minc1_Minc1Image_to_filename
    img = nib.minc1.Minc1Image(get_data(), np.eye(4))
AttributeError: 'module' object has no attribute 'minc1'

$ python run_nibabel.py minc2.Minc2Image.from_filename data/nibabel/minc2_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 111, in invoke_minc2_Minc2Image_from_filename
    data = nib.minc2.Minc2Image.from_filename(file_name)
AttributeError: 'module' object has no attribute 'minc2'

$ python run_nibabel.py minc2.Minc2Image.to_filename tmp/nibabel/minc2_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 117, in invoke_minc2_Minc2Image_to_filename
    img = nib.minc2.Minc2Image(get_data(), np.eye(4))
AttributeError: 'module' object has no attribute 'minc2'

$ python run_nibabel.py parrec.PARRECImage.from_filename data/nibabel/parrec_image.PAR
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 139, in invoke_parrec_PARRECImage_from_filename
    data = nib.parrec.PARRECImage.from_filename(file_name)
AttributeError: 'module' object has no attribute 'parrec'

$ python run_nibabel.py parrec.PARRECImage.to_filename data/nibabel/parrec_image.PAR tmp/nibabel/parrec_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 146, in invoke_parrec_PARRECImage_to_filename
    img = nib.parrec.PARRECImage.from_filename(in_file_name)
AttributeError: 'module' object has no attribute 'parrec'
````

Fails on:

* Ubuntu 14.04.3 LTS + 2.7.6

Cause: changes to package API. These use NiBabel 1.2.2. Others use 2.0.2.

### NiBabel `NotImplementedError`

```
$ python run_nibabel.py minc1.Minc1Image.to_filename tmp/nibabel/minc1_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 105, in invoke_minc1_Minc1Image_to_filename
    img.to_filename(file_name)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\nibabel\spatialimages.py", line 781, in to_filename
    self.to_file_map()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\nibabel\spatialimages.py", line 790, in to_file_map
    raise NotImplementedError
NotImplementedError

$ python run_nibabel.py minc2.Minc2Image.to_filename tmp/nibabel/minc2_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 119, in invoke_minc2_Minc2Image_to_filename
    img.to_filename(file_name)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\nibabel\spatialimages.py", line 781, in to_filename
    self.to_file_map()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\nibabel\spatialimages.py", line 790, in to_file_map
    raise NotImplementedError
NotImplementedError

$ python run_nibabel.py parrec.PARRECImage.to_filename data/nibabel/parrec_image.PAR tmp/nibabel/parrec_image
Traceback (most recent call last):
  File "run_nibabel.py", line 174, in <module>
    function(arguments)
  File "run_nibabel.py", line 148, in invoke_parrec_PARRECImage_to_filename
    img.to_filename(out_file_name)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\nibabel\spatialimages.py", line 781, in to_filename
    self.to_file_map()
  File "C:\Users\mjj\Anaconda3\lib\site-packages\nibabel\spatialimages.py", line 790, in to_file_map
    raise NotImplementedError
NotImplementedError
```

Fails on:

* Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 3.4.3
* Docker 1.12.0 and Ubuntu 14.04.4 LTS + 3.4.3
* Ubuntu 14.04.3 LTS + 2.7.12 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 2.7.6 (pyenv 20160726)
* Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)

Cause: NiBabel interface functions not implemented by sub-classes.

### skimage `NameError`

```
$ python run_skimage.py io.load_sift data/skimage/sift.key 
Loading SIFT: data/skimage/sift.key
Traceback (most recent call last):
  File "run_skimage.py", line 80, in <module>
    function(arguments)
  File "run_skimage.py", line 29, in invoke_io_load_sift
    data = io.load_sift(file_name)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\skimage\io\sift.py", line 62, i
n load_sift
    return _sift_read(f, mode='SIFT')
  File "C:\Users\mjj\Anaconda3\lib\site-packages\skimage\io\sift.py", line 40, in _sift_read
    f = file(f, 'r')
NameError: name 'file' is not defined

$ python run_skimage.py io_load_surf data/skimage/image.surf 
Loading SURF: data/skimage/image.surf
Traceback (most recent call last):
  File "run_skimage.py", line 80, in <module>
    function(arguments)
  File "run_skimage.py", line 37, in invoke_io_load_surf
    data = io.load_surf(file_name)
  File "C:\Users\mjj\Anaconda3\lib\site-packages\skimage\io\sift.py", line 66, in load_surf
    return _sift_read(f, mode='SURF')
  File "C:\Users\mjj\Anaconda3\lib\site-packages\skimage\io\sift.py", line 40, in _sift_read
    f = file(f, 'r')
NameError: name 'file' is not defined
```

Fails on:

* Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 3.4.3
* Docker 1.12.0 and Ubuntu 14.04.4 LTS + 3.4.3
* Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
* Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)

Cause: `file()` built-in removed in Python 3 (see [Builtins](https://docs.python.org/release/3.0/whatsnew/3.0.html#builtins)).

### skimage `ImportError`

All `run_skimage.py` examples fail with:

```
Traceback (most recent call last):
  File "run_skimage.py", line 13, in <module>
    from skimage import external
ImportError: cannot import name 'external'
```

Commenting out:

```
from skimage import external
```

allows the non external.tifffile examples to run.

Fails on:

* Ubuntu 14.04.3 LTS + 2.7.6
* Ubuntu 14.04.3 LTS + 3.4.3
* Docker 1.12.0 and Ubuntu 14.04.4 LTS + 3.4.3

Cause: changes to package API. These use skimage 0.9.3. Others use 0.12.3.
