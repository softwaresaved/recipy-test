# recipy deployment and usage

Mike Jackson, The Software Sustainability Institute / EPCC, The University of Edinburgh

## Introduction

This report reviews recipy, a provenance framework for Python. This report summarises experiences of, and makes recommendations relating to, deploying and using recipy. It was written as a side-effect of familiarising myself with recipy and identifying possible issues with respect to developing an automated test framework for recipy.

The review used the following resources:

* [recipy](https://github.com/recipy/recipy) GitHub repository.
* [recipy 0.2.3](https://pypi.python.org/pypi/recipy) package on PyPI (Python Package Index).

Suggestions and issues arising are marked in **bold**.

---

## Deployment environments

The deployment environments were virtual machines running on:

* VMWare Player 7.1.3 ([download page](https://my.vmware.com/en/web/vmware/free#desktop_end_user_computing/vmware_workstation_player)).
* Dell Latitude E7440:
  - 64-bit Intel Core i5-4310U CPU 2GHz, 2.60GHz 2 core.
  - 8GB RAM.
  - 185GB hard disk.
  - Windows 7 Enterprise Service Pack 1.

The following summarises the environments into which recipy was deployed.

| Operating System         | Python                          |
| ------------------------ | ------------------------------- |
| Windows 7 Enterprise SP1 |                                 |
|                          | 3.5.2 (Anaconda 4.1.1)          |
| Ubuntu 14.04.3 LTS       |                                 |
| (default Python users)   |                                 |
|                          | 2.7.6                           |
|                          | 3.4.3                           |
|                          | 3.4.3 + virtualenv 15.0.2       |
|                          | 3.4.3 + virtualenvwrapper 4.7.1 |
| Docker 1.12.0            |                                 |
| (Ubuntu 14.04.4 LTS)     |                                 |
|                          | 3.4.3                           |
| Ubuntu 14.04.3 LTS       |                                 |
| (local Python users)     |                                 |
|                          | 3.5.2 (Anaconda 4.1.1)          |
|                          | 3.4.0 (pyenv 20160726)          |

The default Python package location for each Python version was used, except for the virtualenv environment where recipy was installed into a virtual environment in the user's local directory.

The following Python environments were used:

* [Anaconda](https://www.continuum.io), a scientific Python distribution which provides Python, the SciPy stack and other scientific Python packages, including (from [Anaconda package list](https://docs.continuum.io/anaconda/pkg-docs)): numpy, pandas, matplotlib, scikit-learn, scikit-image, pillow, beautifulsoup and lxml. Anaconda can be deployed within a user's own directory.
* Default Python 2.7.6 and 3.4.3 versions provided in Ubuntu 14.04.3 LTS and Ubuntu 14.04.4 LTS.
* [virtualenv](https://pypi.python.org/pypi/virtualenv), a tool that creates isolated Python environments with all the executables and packages that that specific environment needs. It allows users to use centrally-installed packages, but also to install additional packages without the need for administrator access.
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/), a wrapper for virtualenv  to make creating and managing virtual environments easier.
* [pyenv](https://github.com/yyuu/pyenv), a tool which allows users to deploy multiple versions of Python within their own directory, and to switch between these versions.

Currently all of the input/output functions for the following Python packages are wrapped by recipy:

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).
* [Geospatial Data Abstraction Library](https://pypi.python.org/pypi/GDAL/). Note that Windows requires installing GDAL Windows binaries, modifying system paths and creating environment variables.
* [lxml](http://lxml.de/). See [Installing lxml](http://lxml.de/installation.html).
* [matplotlib](http://matplotlib.org/). This can be installed as part of SciPy.
* [NiBabel](http://nipy.org/nibabel/) (only the data formats in submodules imported by default). See [Installation](http://nipy.org/nibabel/installation.html).
* [numpy](http://www.numpy.org/). This can be installed as part of [SciPy](https://www.scipy.org/) ([Installing the SciPy Stack](https://www.scipy.org/install.html))
* [pandas](http://pandas.pydata.org/). This can be installed as part of SciPy.
* [Pillow](https://python-pillow.org/). See [Installation](https://pillow.readthedocs.io/en/latest/installation.html).
* [scikit-image](http://scikit-image.org). See [Installing scikit-image](http://scikit-image.org/docs/dev/install.html).
* [scikit-learn](http://scikit-learn.org/stable/). See [Installing scikit-learn](http://scikit-learn.org/stable/install.html). They comment that "We don't recommend installing scipy or numpy using pip on linux".

For information on how virtual machines were set up and these packages installed, see Appendix - setting up deployment environments.

### Environments for future consideration

* Pre-installed Python on Mac OS X.
* Current [production releases](http://legacy.python.org/download/releases/) of Python 3.4.0 and 2.7.6 for Mac OS X and Windows.
* Anaconda 4.1.1 for Mac OS X.
* Enthought [Canopy](https://www.enthought.com/products/canopy/) 1.7.4 for Windows, Linux and Mac. Canopy is a scientific Python bundle with Python 2.7.11 and 200+ Python packages including numpy, pandas, matplotlib, Pillow, scikit-learn, scikit-image, GDAL (of the packages logged by recipy, only NiBabel is not present).
* [Jupyter Notebook](https://ipython.org/notebook.html) interactive computation environment (already logged as recipy issue [106](https://github.com/recipy/recipy/issues/106)).
* pyenv [deployment on Mac OS X](https://github.com/yyuu/pyenv#homebrew-on-mac-os-x) via the [HomeBrew](http://brew.sh/) package manager.
* [conda](http://conda.pydata.org/docs/) 4.1. conda is both a package manager and, like virtualenv, a virtual environment manager. It can be used with Python 2.7, 3.4 or 3.5 under Windows, Linux and Mac. Unlike virtualenv, conda can be used to create virtual environments if using Anaconda.

---

## Checking recipy deployments

The following versions of recipy were used:

* [recipy 0.2.3](https://pypi.python.org/pypi/recipy) package.
* recipy [dd2b7ae96b99ca6d3678f8236ca97ec5ad672454](https://github.com/recipy/recipy/commit/dd2b7ae96b99ca6d3678f8236ca97ec5ad672454) of 31/05/2016, the current version at the time of writing.

The following [scripts](./scripts) were used to check that a recipy deployment was operating correctly, using numpy as an example of a package logged by recipy.

[check-recipy.py](./scripts/check-recipy.py):

```
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file.csv", data, delimiter=",")
```

[check-recipy-import.py](./scripts/check-recipy-import.py):

```
import recipy
import numpy as np

data = np.array([list(range(4,8)), list(range(12,16))])
np.savetxt("file-import.csv", data, delimiter=",")
```

The following script was used to check recipy's wrappers for Python's `open` command:

[check-recipy-open.py](./scripts/check-recipy-open.py):

```
import recipy
with recipy.open('file-open.txt', 'w') as f:
    f.write("This is a test")
```

For the commands run to deploy recipy and check its deployment, see Appendix - commands run for each deployment.

---

## Suggestions

Suggestions arising from the deployment and use of recipy are as follows.

### Functionality

**Suggestion:** During `recipy annotate`, configure the editor to show the current notes so these can be edited without the need for the user to copy them from the bottom of the file.

**Suggestion:** If `~/.recipy/recipyrc` is created of form:

```
[data]
file_diff_outputs
```

then file diffs between runs are visible within `recipy gui`. But, they are not visible via the command line. Provide some way for these to be returned.

**Suggestion:** `recipy gui` page http://127.0.0.1:9000/patched_modules shows the packages, input and output functions logged by recipy. These are queried by `recipyGui/views.py` from the recipy database, from within its `patches` table. This table is populated when the `recipy` package is first used (via `__init.py__` and `PatchWarnings.py`, `PatchBaseScientific.py`, `PatchScientific.py`). Write a script that runs comparable commands to create a MarkDown page of the packages and functions that can then form part of the user documentation. Users would be able to see a list of the packages and functions, without having to install recipy and run `recipy gui`.

**Suggestion:** Develop a tool that uses reflection to traverse the functions of a package and print out the names of functions (and, if possible, their "help" information) that might be candidate input/output functions that should be logged by recipy (e.g. functions with names such as `input/output`, `read/write`, `load/save`). Such a tool could help those who want to develop recipy wrappers for additional packages.

### Documentation

**Suggestion:** Provide a list of the packages, and their functions, that are logged by recipy, so users can see these without having to install recipy and run `recipy gui`.

**Suggestion:** `README.md` states that:

> it will produce an output called test.npy. To find out the details of the run which created this file you can search using
> recipy search test.npy

Rephrase this to:

> The sample script above will produce...

to reinforce that it's the sample script, and not recipy, that produces `test.npy`.

**Suggestion:** Provide examples of `recipy gui` search strings.

**Suggestion:** As not all command-line options apply to all commands, provide information, via the usage information and in the documentation, on which options apply to which commands.

**Suggestion:** Explain the difference between `fuzzy` and `regex` searching, and provide examples of fuzzy and regular expression patterns.

**Suggestion:** Provide examples of using absolute paths with `recipy search`.

**Suggestion:** Add a note that files can be searched for even if they no longer exist, and a complementary caution that just because a file exists in the recipy database it does not necessarily exist in reality.

**Suggestion:** Describe how and when `--diff` will show the `diff` i.e. if the commit is newer than the most recent files is what it seems to do.

**Suggestion:** Provide brief descriptions, with sample inputs and outputs for every command.

**Suggestion:** Document the need to set the `EDITOR` variable, using `export EDITOR=...`, and that user can override their default e.g. if they want nano rather than vi.

**Suggestion:** Provide troubleshooting information that if the user sees a message like:

```
$ recipy annotate
sh: 1: /tmp/tmpEk9ykM: Permission denied
No annotation entered, exiting.

$ EDITOR=nano
$ recipy annotate
sh: 1: /tmp/tmpEk9ykM: Permission denied
No annotation entered, exiting.
```

on Linux, then they should set the `EDITOR` variable.

**Suggestion:** State that only the latest run can be annotated via `recipy annotate`.

**Suggestion:** State that annotations are completely overwritten when running `recipy annotate`, and that if the user wants to retain their current notes they should copy them from the lower-half of the editor.

**Suggestion:** State that, if default/system-wide Python distributions are being used on Linux then `sudo` access is required when running `pip` or `python setup.py install`.

**Suggestion:** State that, if default/system-wide Python 2 and 3 distributions co-exist on Linux, then the user needs to use `pip3` and `python3` for Python 3-related operations.

**Suggestion:** `README.md` comments that:

> If you want to log inputs and outputs of files read or written with built-in open, you need to do a little more work. Either use `recipy.open` (only requires import recipy at the top of your script), or add `from recipy import open` and just use `open`. This workaround is required, because many libraries use built-in open internally, and you only want to record the files you explicitly opened yourself.
> If you use Python 2, you can pass an `encoding` parameter to `recipy.open`. In this case `codecs` is used to open the file with proper encoding.

Describe whether `recipy.open` has the same function signature as `open` (with the additional `encoding` parameter) or whether it changes it, in which case describe the altered signature.

**Suggestion:** State whether `git` is needed on Windows or Linux to use recipy. It is clear that it is needed for its Git-related functionality, and the `hash_inputs`, `hash_outputs` and `diff` configuration options, but not for other functionality.

**Suggestion:** If `~/.recipy/recipyrc` is created of form:

```
[data]
file_diff_outputs
```

then file diffs between runs are visible within `recipy gui`. It is not clear how to view these at the command-line, so clarify this.

**Suggestion:** Provide guidelines on how to use recipy in a research workflow e.g. how to use recipy and Git to record provenance and recommended ways of archiving input/output files etc.

**Suggestion:** Document how to install dependencies and run tests e.g.

```
$ pip install -r requirements.txt
$ pip install -r test_requirements.txt 
```

and:

```
$ python setup.py test
```

or:

```
$ py.test test
$ py.test recipyGui/tests
```

---

## Issues

Issues arising from the deployment and use of recipy are as follows.

### recipy 0.2.3 and dd2b7ae96b99ca6d3678f8236ca97ec5ad672454

**Issue:** Allow use of full IDs when searching and also provide a `recipy get ID` command. It feels counter-intuitive that a partial match succeeds:

```
$ recipy search -i 23bf2fd2-b67a-46c1-9fd8-960e71d32f2
...shows details...
```

but a full match does not:

```
$ recipy search -i 23bf2fd2-b67a-46c1-9fd8-960e71d32f2f
No results found
```

**Issue:** Under Windows, I tried using `.bashrc` and `.bash_profile` to set `EDITOR`, and also tried running these commands within the Anaconda Python Prompt, rather than the Git Bash prompt, but with no success:

```
$ recipy annotate
'$EDITOR' is not recognized as an internal or external command, operable program or batch file.
No annotation entered, exiting.
$ EDITOR=notepad.exe
$ recipy annotate
...as above...
$ export EDITOR=notepad.exe
$ recipy annotate
...as above...
```

Resolve this issue or, if it cannot be resolved, recommend that Windows/Git Bash/Anaconda users use `recipy gui` (already logged as recipy issue [98](https://github.com/recipy/recipy/issues/98)).

**Issue:** `recipy latest` raises `IndexError: list index out of range` if there are no runs:

```
$ recipy latest
Traceback (most recent call last):
  File "/home/ubuntu/anaconda3/bin/recipy", line 9, in <module>
    load_entry_point('recipy==0.2.3', 'console_scripts', 'recipy')()
  File "/home/ubuntu/anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCmd/recipycmd.py", line 118, in main
    latest(args)
  File "/home/ubuntu/anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCmd/recipycmd.py", line 225, in latest
    run = get_latest_run()
  File "/home/ubuntu/anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg/recipyCmd/recipycmd.py", line 220, in get_latest_run
    return results[-1]
IndexError: list index out of range
```

Catch this error and print a suitable error message e.g. `You have not recorded any runs` (already logged as recipy issue [118](https://github.com/recipy/recipy/issues/118))

### recipy 2.3.0

**Issue:** Searches of the `recipy gui` web pages did not work. I tried using `mjj`, `file-import.csv`, `C:\Users\mjj\deployment\file` for Windows and `/home/ubuntu/deployment/file` for Ubuntu and, for each, got a `HTTP 500 Interal Server Error`.

**Issue:** `recipy.open` seems to be unsupported in 0.2.3:

```
$ python check-recipy-open.py
recipy run inserted, with ID 3e5b0039-b611-44b7-b027-de241e4d4a4b
Traceback (most recent call last):
  File "check-recipy-open.py", line 2, in <module>
    with recipy.open('file-open.txt', 'w') as f:
AttributeError: module 'recipy' has no attribute 'open'

$ recipy latest
Run ID: 3e5b0039-b611-44b7-b027-de241e4d4a4b
Created by mjj on 2016-08-11T15:12:47 UTC
Ran C:\Users\mjj\deployment\check-recipy-open.py using C:\Users\mjj\Anaconda3\python.exe
Environment: Windows-7-6.1.7601-SP1, python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
Exception: (AttributeError) module 'recipy' has no attribute 'open'
Inputs: none
Outputs: none
```

It looks like this feature and information was added to recipy and `README.md` since the 0.2.3 package was created. Add a link to the recipy [pypi](https://pypi.python.org/pypi/recipy) page to point to the `README.md` corresponding to the version in the [v0.2.3](https://github.com/recipy/recipy/releases/tag/v0.2.3) tag. Likewise, adopt this practice for future releases, or make it clear in the documentation what features are supported by what versions.

### recipy dd2b7ae96b99ca6d3678f8236ca97ec5ad672454

**Issue:** The recipy 0.2.3 package was [tagged](https://github.com/recipy/recipy/releases/tag/v0.2.3) on 17/11/2015. There have been many commits since then, so the current state of the repository, on GitHub, is no longer version 0.2.3 but, at least, 0.2.4. I'd recommend upping the version number in `setup.py` immediately after you tag a release, or at the first time you make a commit after tagging the release.

**Issue:** There is inconsistency between `README.md` and `recipy gui` in terms of logged packages:

* `recipy gui` statues that `lxml.etree` and `bs4` packages are logged (which is the case as `recipy gui` gets this information from the recipy database which is, in turn, populated by the recipy components that do this logging.
* `README.md` states that `scikit-image` and `pillow` are logged. However, this code is commented out in `recipy/PatchScientific.py` (in both the current version and in version 0.2.3)

Adopting the earlier suggestion of auto-generating user documentation would reduce the risk of such inconsistency.

If the `scikit-image` and `pillow` in `recipy/PatchScientific.py` was accidently commented out then restore it. If it needs to be fixed then add a comment stating such and create an associated GitHub issue. Otherwise, just remove it from the file.

**Issue:** Under Windows `recipy search file-import.csv` raises `sre_constants.error: incomplete escape \U at position 2` using Git Bash and Anaconda Python prompts:

```
$ recipy search file-import.csv
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

**Issue:** `recipy latest -j` and other commands supporting `j`  raise `TypeError: datetime.datetime(2016, 8, 12, 8, 49, 22) is not JSON serializable`:

```
$ recipy latest -j
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

Note that JSON documents can be downloaded via `recipy gui`.

**Issue:** Under Windows, a `recipy gui` search for `C:\Users\mjj\deployment\file` fails, but succeeds for `C:\\Users\\mjj\\deployment\\file`. Update the search code to escape `\` in file paths.

**Issue:** Using `recipy.open` (`with recipy.open('file-open.txt', 'w') as f:`) gives a gives an `ValueError: I/O operation on closed file`, with Python 2:

```
$ python check-recipy-open.py
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

Using `recipy.open` (as `with recipy.open('file-open.txt', 'w') as f:`) gives a `KeyError: 'mode'` error, with Python 3:

```
$ python check-recipy-open.py
recipy run inserted, with ID 02c4d038-6934-4057-9c85-41d717ab6052
Traceback (most recent call last):
  File "check-recipy-open.py", line 2, in <module>
    with recipy.open('file-open.txt', 'w') as f:
  File "C:\Users\mjj\Anaconda3\lib\site-packages\recipy-0.2.3-py3.5.egg\recipy\utils.py", line 20, in open
    mode = kwargs['mode']
KeyError: 'mode'
```

Editing `check-recipy-open.py` and changing:

```
with recipy.open('file-open.txt', 'w') as f:
```

to

```
with recipy.open('file-open.txt', mode='w') as f:
```

so that the `mode` parameter is named, then re-running, gives:

```
$ python check-recipy-open.py
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

The above implies that `recipy.open` does not seem to support the same signature as Python `open`. I would expect it would support the same signature.

**Issue:** Investigate how to access a `recipy gui` service running within a Docker container, from within the container's host. Using

```
$ docker run -it -v $HOME/docker-shared:/home/ubuntu/shared -p 9000:9000 --rm mikej888/recipy:2.3.0 
```

I could not access the port exposed by `recipy gui`, 9000, from within the host, either via `wget` or via a web browser. I ran a simple Flask application code from [Dockerize Simple Flask App](http://containertutorials.com/docker-compose/flask-simple-app.html) as a stand-alone Python program called `service.py` in a running container:

```
$ docker run -it -v $HOME/docker-shared:/home/ubuntu/shared -p 9000:9000 -p 5000:5000 --rm mikej888/recipy:github
$ python shared/service.py 
```
```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 173-554-812
```

Then, in my host, I ran:

```
$ wget 127.0.0.1:5000
```

The container showed:

```
172.17.0.1 - - [15/Aug/2016 12:42:27] "GET / HTTP/1.1" 200 -
```

And the response was returned to the host:

```
--2016-08-15 05:43:32--  http://127.0.0.1:5000/
Connecting to 127.0.0.1:5000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 16 [text/html]
Saving to: "index.html"

100%[======================================>] 16          --.-K/s   in 0s      

2016-08-15 05:43:32 (799 KB/s) - "index.html" saved [16/16]
```

```
$ cat index.html 
Flask Dockerized
```

Similarly if the URL http://127.0.0.1:5000 was pinged from the host.

Maybe this has to do with how the Flask framework, which is used to implement `recipy gui` is configured.

**Issue:** When the command `python3 setup.py install` is run when creating the Docker container, an error arises:

```
Flask-WTF 0.12 is already the active version in easy-install.pth

Installed /usr/local/lib/python3.4/dist-packages/Flask_WTF-0.12-py3.4.egg
error: Could not find required distribution Flask
```

If the command is re-run then installation succeeds:

```
Flask-Script 2.0.5 is already the active version in easy-install.pth

Using /usr/local/lib/python3.4/dist-packages/Flask_Script-2.0.5-py3.4.egg
Finished processing dependencies for recipy==0.2.3
```

This arises when running the command within a Docker file or within a Docker container. The Dockerfile in the Appendix solves this by running the command twice:

```
# Attempt the installation twice as the first attempt fails with:
# error: Could not find required distribution Flask
# but the second attempt succeeds. The "ls" ensures that the
# first command returns 0 so the rest of the Dockerfile is
# executed.
RUN cd recipy && python3 setup.py install; ls
RUN cd recipy && python3 setup.py install
```

but this is hacky!

**Issue:** Running `python setup.py install` with pyenv does not result in the `recipy` executable being available:

```
$ recipy --version
bash: /home/ubuntu/.pyenv/shims/recipy: No such file or directory
$ which recipy

```

Comparing the recipy files within pyenv installed using `python setup.py install` to those installed using `pip` shows that the former end up in:

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

and the latter in:

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

The difference is `.pyenv/shims/recipy`. StackOverflow [Pyenv shim not created when installing package using setup.py](http://stackoverflow.com/questions/29753592/pyenv-shim-not-created-when-installing-package-using-setup-py) comments that:

> Versions of pyenv before v20141211 do not automatically "rehash" (that is, update shims) when a new package is installed. To get pyenv to automatically rehash, either upgrade to a newer version of pyenv, or install the pyenv-pip-refresh plugin.
> To rehash manually, use this command for bash:
> `pyenv rehash && hash -r`

My pyenv is newer than this:

```
$ pyenv --version
pyenv 20160726
```

but I tried the manual solution which solved the problem:

```
$ pyenv rehash && hash -r
$ which recipy
/home/ubuntu/.pyenv/shims/recipy
$ recipy --version
recipy v0.2.3
```

Document the workaround `pyenv rehash && hash -r` in the short-term and track down a possible automated solution in the longer term.

**Issue:** `python setup.py test` seems to find no tests under Python 2.7.6 e.g.:

```
$ python setup.py test
running test
running egg_info
writing requirements to recipy.egg-info/requires.txt
writing recipy.egg-info/PKG-INFO
writing top-level names to recipy.egg-info/top_level.txt
writing dependency_links to recipy.egg-info/dependency_links.txt
writing entry points to recipy.egg-info/entry_points.txt
reading manifest file 'recipy.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
writing manifest file 'recipy.egg-info/SOURCES.txt'
running build_ext

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
```

whereas 

```
$ py.test test
$ py.test recipyGui/tests
```

both succeed. Try and find the reason for, and a solution to, this.

**Issue:** Running:

```
$ py.test test
```

under Python 2 or 3 shows a test failure:

```
============================= test session starts ==============================
platform linux -- Python 3.5.2, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
rootdir: /home/ubuntu/recipy, inifile: 
collected 14 items / 1 errors 

test/test_libraryversions.py ..
test/test_tinydb_utils.py .........
test/test_utils.py ...

==================================== ERRORS ====================================
_____________________ ERROR collecting test/test_config.py _____________________
test/test_config.py:3: in <module>
    import fake_filesystem_unittest
E   ImportError: No module named 'fake_filesystem_unittest'
====================== 14 passed, 1 error in 0.39 seconds ======================
```

This seems to arise due to changes in [pyfakefs](https://github.com/jmcgeheeiv/pyfakefs), one of the requirements listed in `test_requirements.txt`. A fix is to edit test/test_config.py and replace

```
import fake_filesystem_unittest
```

with

```
from pyfakefs import fake_filesystem_unittest
```

```
$ py.test test
============================= test session starts ==============================
platform linux -- Python 3.5.2, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
rootdir: /home/ubuntu/recipy, inifile: 
collected 15 items 

test/test_config.py .
test/test_libraryversions.py ..
test/test_tinydb_utils.py .........
test/test_utils.py ...

========================== 15 passed in 0.52 seconds ===========================
```

**Issue:** Running `py.test recipyGui/tests/` shows test failures under Python 3.5.2:

```
$ py.test recipyGui/tests/
============================= test session starts ==============================
platform linux -- Python 3.5.2, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
rootdir: /home/ubuntu/recipy, inifile: 
collected 9 items 

recipyGui/tests/test_filters.py ...
recipyGui/tests/test_recipyGui.py F.F...

=================================== FAILURES ===================================
__________________ TestRecipyGui.test_dbfile_is_set_in_views ___________________

self = <recipyGui.tests.test_recipyGui.TestRecipyGui testMethod=test_dbfile_is_set_in_views>

    def test_dbfile_is_set_in_views(self):
        """The database file should be displayed in the index, and run_details
            views.
            """
        eid = self.db.insert(self.testRuns[0])
    
        views = ['/', '/run_details?id={}'.format(eid)]
    
        for v in views:
            response = self.client.get(v)
            dbfile2 = self.get_context_variable('dbfile')
            # is the right value set?
            self.assertEqual(recipyGui.config.get('tinydb'), dbfile2)
            # is the value displayed?
>           assert recipyGui.config.get('tinydb') in response.data
E           TypeError: a bytes-like object is required, not 'str'

recipyGui/tests/test_recipyGui.py:202: TypeError
_________________ TestRecipyGui.test_display_warnings_in_views _________________

self = <recipyGui.tests.test_recipyGui.TestRecipyGui testMethod=test_display_warnings_in_views>

    def test_display_warnings_in_views(self):
        """If the run contains warnings, they must be displayed in the index
            and run_details view.
            """
        for run in self.testRuns:
            eid = self.db.insert(run)
            response = self.client.get('/run_details?id={}'.format(eid))
            if 'warnings' in run.keys():
                if run['warnings'] != []:
                    for w in run['warnings']:
                        assert w['message'] in response.data
                else:
                    assert 'Warnings' not in response.data
            else:
>               assert 'Warnings' not in response.data
E               TypeError: a bytes-like object is required, not 'str'

recipyGui/tests/test_recipyGui.py:218: TypeError
====================== 2 failed, 7 passed in 0.64 seconds =====================
```

Under Python 3.4.0 there are two slightly different errors but from the same source:

```
__________________ TestRecipyGui.test_dbfile_is_set_in_views ___________________

...

>           assert recipyGui.config.get('tinydb') in response.data
E           TypeError: Type str doesn't support the buffer API

recipyGui/tests/test_recipyGui.py:202: TypeError
_________________ TestRecipyGui.test_display_warnings_in_views _________________

...

>               assert 'Warnings' not in response.data
E               TypeError: Type str doesn't support the buffer API

recipyGui/tests/test_recipyGui.py:218: TypeError
```

Under Python 2.7.12 they pass:

```
$ py.test recipyGui/tests
============================= test session starts ==============================
platform linux2 -- Python 2.7.12, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
rootdir: /home/ubuntu/recipy, inifile: 
collected 9 items 

recipyGui/tests/test_filters.py ...
recipyGui/tests/test_recipyGui.py ......

=========================== 9 passed in 0.58 seconds ===========================
```

The problem arises due to a change in types. In Python 2 `response.data` has type `str`, but in Python 3 it has type `bytes`. One fix is to change the lines:

```
assert recipyGui.config.get('tinydb') in response.data

assert w['message'] in response.data

assert 'Warnings' not in response.data

assert 'Warnings' not in response.data
```

to:

```
assert recipyGui.config.get('tinydb') in response.data.decode()

assert w['message'] in response.data.decode()

assert 'Warnings' not in response.data.decode()

assert 'Warnings' not in response.data.decode()
```

---

## An observation on versioning

A general observation is that recipy logs packages which may currently exist in various versions depending upon how a researcher has installed them and into what environment. For example a package may run under Python 2 but not Python 3, an Ubuntu package installed via `apt-get python-*` may lag behind more recent versions, as may those bundled in distributions such as Anaconda or Canopy. Complicating matters futher, input/ouput functions logged by recipy may be deprecated by package developers and new input/output functions written to replace these. recipy should document not only what packages and functions it logs but also what versions of packages it has been tested against. Whether a single version of recipy can support multiple versions of the same package, differing in their input/ouput functions should also be explored and documented.

---

## Appendix - setting up deployment environments

### Windows 7 Enterprise Service Pack 1 virtual machine

Install Git and Anaconda:

* [Git for Windows](https://git-for-windows.github.io/) 2.9.2
* Anaconda 4.1.1 and Python 3.5.2.

Install packages logged by recipy:

```
pip install nibabel
```

Check package versions:

```
pip freeze
```
```
beautifulsoup4==4.4.1
lxml==3.6.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.2.0
scikit-image==0.12.3
scikit-learn==0.17.1
```

I didn't install GDAL due to an additional Windows-specific install process. 

### Ubuntu 14.04.3 LTS virtual machine (default Python users)

By default, Ubuntu 14.04.3 LTS comes with Python 2.7.6 and 3.4.3.

Install Python 2 packages:

```
sudo su -
apt-get install -y python-numpy python-scipy python-matplotlib python-pandas python-nose
apt-get install -y python-pip
apt-get install -y python-setuptools
```

Install packages logged by recipy:

```
apt-get install -y python-pillow
apt-get install -y python-sklearn
apt-get install -y python-skimage
apt-get install -y python-nibabel
apt-get install -y python-gdal
```

lxml and bs4 are installed as side-effects of the above.

Check package versions:

```
pip freeze
```
```
GDAL==1.10.1
Pillow==2.3.0
beautifulsoup4==4.2.1
lxml==3.3.3
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
apt-get install -y python3-numpy python3-scipy python3-matplotlib python3-pandas python3-nose
apt-get install -y python3-pip
apt-get install -y python3-setuptools
pip3 install xlwt
apt-get install -y python3-h5py
```

Install packages logged by recipy:

```
apt-get install -y python3-pillow
pip3 install scikit-learn
apt-get install -y python3-skimage
pip3 install nibabel
apt-get install -y python3-gdal
```

lxml and bs4 are installed as side-effects of the above.

Check package versions:

```
pip3 freeze
```
```
GDAL==1.10.1
Pillow==2.3.0
beautifulsoup4==4.2.1
lxml==3.3.3
matplotlib==1.3.1
nibabel==2.0.2
numpy==1.8.2
pandas==0.13.1
scikit-image==0.9.3
scikit-learn==0.17.1
```

I used pip for scikit-learn and nibabel as there are no python3-sklearn or python3-nibabel packages.

**virtualenv 15.0.2**

Install virtualenv:

```
sudo su -
pip install virtualenv
pip3 install virtualenv
```

**virtualenvwrapper 4.7.1**

Install virtualenvwrapper:

```
sudo su -
pip install virtualenvwrapper
pip3 install virtualenvwrapper
```

### Docker 1.12.0 and Ubuntu 14.04.4 LTS 

Install Docker:

```
curl -fsSL https://get.docker.com/ | sh
sudo usermod -aG docker ubuntu
sudo service docker start
```

Log out and in again.

Create a directory for a `Dockerfile`:

```
mkdir recipy-docker
cd recipy-docker
```

Write a [Dockerfile](./docker/Dockerfile) to install the packages that recipy can log and other useful tools:

```
FROM ubuntu:trusty-20160217
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y nano
RUN apt-get install -y git
RUN apt-get install -y python3-numpy
RUN apt-get install -y python3-scipy
RUN apt-get install -y python3-matplotlib
RUN apt-get install -y python3-pandas
RUN apt-get install -y python3-nose
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-pillow
RUN pip3 install scikit-learn
RUN apt-get install -y python3-skimage
RUN pip3 install nibabel
RUN apt-get install -y python3-gdal
RUN pip3 install xlwt # For pandas
RUN apt-get install -y python3-h5py # For nibabel
RUN pip3 freeze
# Default command to run as part "docker run" if no command is given.
CMD ["/bin/bash"]
```

lxml and bs4 are installed as side-effects of the above.

Build image, remembering to put in the `.`:

```
docker build -t mikej888/recipy:dependencies .
```

(note the tag of the image is consistent with that expected by Docker Hub `username / repository : version label or tag`)

Check image is now available:

```
docker images
```
```
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
mikej888/recipy     dependencies        b310a01f57a9        7 seconds ago       722.1 MB
ubuntu              trusty-20160217     14b59d36bae0        5 months ago        188 MB
```

Create a directory to be shared with the running image:

```
mkdir $HOME/docker-shared
chmod o+w $HOME/docker-shared
```

If `docker-shared` is not created beforehand, then it will be created by Docker and will have `root` owner and group in both the running container and on the host.

If `docker-shared` is created beforehand, then it will have `1000` owner and group in the running container and a user within a running container cannot access it. Hence, setting the `other` file permission is required.

Run the image in a container, mounting `docker-shared` to `/tmp/shared`:

```
docker run -it -v $HOME/docker-shared:/tmp/shared --rm mikej888/recipy:dependencies
```

The other flags are as follows:

* `-i` keeps `STDIN` open even if the host is not attached to the container when running.
* `-t` allocates a pseudo-terminal to the container.
* `--rm` automatically removes the container when it exits. This does not remove the image.

In another terminal window, view the available containers:

```
docker ps
```
```
CONTAINER ID        IMAGE                 COMMAND             CREATED             STATUS              PORTS               NAMES
a510f396a25c        mikej888/recipy:dependencies   "/bin/bash"         26 seconds ago      Up 25 seconds                           desperate_davinci
```

Check container operating system:

```
lsb_release -a
```
```
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 14.04.4 LTS
Release:	14.04
Codename:	trusty
```

Check container's Python:

```
python3
import matplotlib
# Set non-interactive matplotlib back-end.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.plot([1,2,3])
plt.savefig("/tmp/shared/plot.png")
CTRL-D
```

Check `docker-shared/plot.png` exists on the host and holds a graph.

Check container's package versions:

```
pip3 freeze
```
```
GDAL==1.10.1
Pillow==2.3.0
beautifulsoup4==4.2.1
lxml==3.3.3
matplotlib==1.3.1
nibabel==2.0.2
numpy==1.8.2
pandas==0.13.1
scikit-image==0.9.3
scikit-learn==0.17.1
```

Exit container:

```
CTRL-D
```

### Ubuntu 14.04.3 LTS virtual machine (local Python users)

**Anaconda 4.1.1**

Install Anaconda with Python 2.7.12 and packages:

```
wget http://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh
bash Anaconda2-4.1.1-Linux-x86_64.sh
```

Create `use-anaconda2.sh` to set up environment (usually this goes into `.bashrc`, but I didnt't want its paths to interfere with Anaconda Python 3):

```
export PATH=/home/ubuntu/anaconda2/bin:$PATH
```

Install packages logged by recipy:

```
source use-anaconda2.sh

pip install nibabel
conda install gdal
```

Check package versions:

```
pip freeze
```
```
beautifulsoup4==4.4.1
GDAL==2.1.0
lxml==3.6.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.2.0
scikit-image==0.12.3
scikit-learn==0.17.1
```

Install Anaconda with Python 3.5.2 and packages:

```
wget http://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh
bash Anaconda3-4.1.1-Linux-x86_64.sh
```

Create `use-anaconda3.sh` to set up environment:

```
export PATH=/home/ubuntu/anaconda3/bin:$PATH
```

Install packages logged by recipy:

```
source use-anaconda3.sh

pip install nibabel
conda install gdal
```

Check package versions:

```
pip freeze
```
```
beautifulsoup4==4.4.1
GDAL==2.1.0
lxml==3.6.0
matplotlib==1.5.1
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.2.0
scikit-image==0.12.3
scikit-learn==0.17.1
```

**pyenv 20160726**

Install GDAL, as the package available via `apt-get libgdal-dev` can't be used with the latest Python `GDAL` package, so build from scratch:

```
wget http://download.osgeo.org/gdal/2.1.0/gdal-2.1.0.tar.gz
tar xvf gdal-2.1.0.tar.gz
cd gdal-2.1.0/
./configure
make # This takes about an hour!
sudo make install
# This is necessary so Python finds the correct library.
export LD_PRELOAD=/usr/local/lib/libgdal.so.20.1.0 
```

Install pyenv:

```
sudo apt-get install -y git
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

Create `use-pyenv.sh` to set up environment (usually this goes into `.bash_profile`) and add `LD_PRELOAD` for GDAL:

```
export LD_PRELOAD=/usr/local/lib/libgdal.so.20.1.0 
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Install Python 2.7.6 and 3.4.0 within pyenv:

```
source use-pyenv.sh
pyenv update
pyenv install -l
pyenv install 2.7.6
pyenv install 3.4.0
```

Install Python 2 packages logged by recipy:

```
source use-pyenv.sh 
pyenv local 2.7.6
pip install numpy
pip install scipy
sudo apt-get install -y libfreetype6-dev
pip install matplotlib
sudo apt-get install -y libhdf5-dev
pip install xlrd
pip install tables
pip install pandas
pip install nose
pip install pillow
pip install scikit-learn
pip install scikit-image
pip install h5py
pip install nibabel
sudo apt-get install -y libxslt1-dev
pip install lxml
pip install beautifulsoup4
easy_install GDAL
```

Check package versions:

```
pip freeze
```
```
beautifulsoup4==4.5.1
GDAL==2.1.0
matplotlib==1.5.2
nibabel==2.0.2
numpy==1.11.1
pandas==0.18.1
Pillow==3.3.1
scikit-image==0.12.3
scikit-learn==0.17.1
```

Install Python 3 packages logged by recipy:

```
source use-pyenv.sh 
pyenv local 3.4.0
pip install numpy
sudo apt-get install -y libblas-dev liblapack-dev gfortran
pip install scipy
pip install matplotlib
pip install xlrd
# Avoid error: ISO C90 forbids mixed declarations 
# and code [-Werror=declaration-after-statement]
# See http://stackoverflow.com/questions/25587039/error-compiling-rpy2-on-python3-4-due-to-werror-declaration-after-statement
export CFLAGS="-Wno-error=declaration-after-statement"
pip install tables
pip install pandas
pip install nose
pip install pillow
pip install scikit-learn
pip install cython
pip install scikit-image
pip install h5py
pip install nibabel
pip install lxml
pip install beautifulsoup4
easy_install GDAL
pip install xlwt
```

Check package versions:

```
pip freeze
```
```
GDAL==2.1.0
Pillow==3.3.1
beautifulsoup4==4.5.1
lxml==3.6.3
matplotlib==1.5.2
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

which has been [noted by others](https://github.com/python-pillow/Pillow/issues/2017). So I installed the same version as for Python 2 (3.2.0) as suggested by others.

---

## Appendix - commands run for each deployment

In what follows `python3` and `pip3` were used instead of `python` and `pip` on Ubuntu 14.04.3 LTS + 3.4.3 and Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3 (via Dockerfiles).

### Set up environment

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 2.7.6
# Ubuntu 14.04.3 LTS + 3.4.3
# Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3
# ...not applicable...

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
mkdir recipy-venv
cd recipy-venv
virtualenv venv --python=/usr/bin/python3 --system-site-packages
cd
source recipy-venv/venv/bin/activate

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv recipy-wrapper-env --python=/usr/bin/python3 --system-site-packages
workon recipy-wrapper-env

# Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
export PATH=/home/ubuntu/anaconda3/bin:$PATH

# Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### Install recipy 0.2.3

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)
pip install recipy

# Ubuntu 14.04.3 LTS + 2.7.6
sudo pip install recipy

# Ubuntu 14.04.3 LTS + 3.4.3
sudo pip3 install recipy

# Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3
cat > Dockerfile-recipy-2.3.0 << EOF
FROM mikej888/recipy:dependencies
RUN pip3 install recipy
# Create group and user so image is not used as root.
RUN groupadd -r ubuntu
RUN useradd -r -g ubuntu -m -s /sbin/nologin -c "Image user" ubuntu
RUN chown -R ubuntu:ubuntu /home/ubuntu
# Run commands as ubuntu within /home/ubuntu.
USER ubuntu
WORKDIR /home/ubuntu
# Set non-interactive matplotlib back-end. If this is not defined
# then showing matplotlib plots gives an error:
# _tkinter.TclError: no display name and no $DISPLAY environment variable
RUN mkdir -p .config/matplotlib
RUN echo "backend : Agg" >> .config/matplotlib/matplotlibrc
# Default command to run as part "docker run" if no command is given.
CMD ["/bin/bash"]
EOF
docker build -t mikej888/recipy:2.3.0 -f Dockerfile-recipy-2.3.0 .
docker run -it -v $HOME/docker-shared:/home/ubuntu/shared -p 9000:9000 --rm mikej888/recipy:2.3.0 
```

(see [Dockerfile-recipy-2.3.0](./docker/Dockerfile-recipy-2.3.0))

### Install recipy latest version

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 2.7.6
# Ubuntu 14.04.3 LTS + 3.4.3
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)
git clone https://github.com/recipy/recipy
cd recipy
git log -1 --format="%ai %H"

# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)
python setup.py install

# Ubuntu 14.04.3 LTS + 2.7.6
sudo python setup.py install

# Ubuntu 14.04.3 LTS + 3.4.3
sudo python3 setup.py install

# Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3
cat > Dockerfile-recipy-github << EOF
FROM mikej888/recipy:dependencies
RUN git clone https://github.com/recipy/recipy
RUN cd recipy && git log -1 --format="%ai %H"
# Attempt the installation twice as the first attempt fails with:
# error: Could not find required distribution Flask
# but the second attempt succeeds. The "ls" ensures that the
# first command returns 0 so the rest of the Dockerfile is
# executed.
RUN cd recipy && python3 setup.py install; ls
RUN cd recipy && python3 setup.py install
RUN python3 setup.py install
# Create group and user so image is not used as root.
RUN groupadd -r ubuntu
RUN useradd -r -g ubuntu -m -s /sbin/nologin -c "Image user" ubuntu
RUN chown -R ubuntu:ubuntu /home/ubuntu
# Run commands as ubuntu within /home/ubuntu.
USER ubuntu
WORKDIR /home/ubuntu
# Set non-interactive matplotlib back-end. If this is not defined
# then showing matplotlib plots gives an error:
# _tkinter.TclError: no display name and no $DISPLAY environment variable
RUN mkdir -p .config/matplotlib
RUN echo "backend : Agg" >> .config/matplotlib/matplotlibrc
# Default command to run as part "docker run" if no command is given.
CMD ["/bin/bash"]
EOF
docker build -t mikej888/recipy:2.3.0 -f Dockerfile-recipy-github .
docker run -it -v $HOME/docker-shared:/home/ubuntu/shared -p 9000:9000 --rm mikej888/recipy:github 
```

(see [Dockerfile-recipy-github](./docker/Dockerfile-recipy-github))

### Check Python and pip versions

```
which python
python --version
which pip
pip --version
```

### Run `recipy`

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
EDITOR=nano # Ubuntu only
recipy annotate
export EDITOR=notepad.exe # Windows only
export EDITOR=nano # Ubuntu only
recipy annotate

python -m recipy check-recipy.py
python check-recipy-open.py

recipy gui
```

### See behaviour if `deployment` directory, in which scripts have been run, no longer exists

```
cd ..
mv deployment tmp
recipy search C:/Users/mjj/deployment/file-import.csv # Windows only
recipy search /home/ubuntu/deployment/file-import.csv # Ubuntu only
mv tmp deployment
```

### See behaviour within Git repositories

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

### Run `recipy gui`

* Search for mjj, file-import.csv, C:\Users\mjj\deployment\file-import.csv (Windows), C:\\Users\\mjj\\deployment\\file-import.csv (Windows)
* Search for ubuntu, file-import.csv, /home/ubuntu/deployment/file-import.csv (Ubuntu)
* Click View details
* Click Save as JSON
* Enter Notes: `This was Mike's first use of recipy.`
* Click Save notes
* Click Save as JSON
* Look at JSON files.

### Find recipy files, before and after uninstall

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
find Anaconda3/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 2.7.6
# Ubuntu 14.04.3 LTS + 3.4.3
find /usr/local -name "*recipy*"

# Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3
...not applicable...

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
find recipy-venv/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
find Envs/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
find anaconda3/ -name "*recipy*"

# Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)
find .pyenv -name "*recipy*"
```

### Uninstall recipy 0.2.3:

```
# Windows 7 Enterprise SP1 + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2
# Ubuntu 14.04.3 LTS + 3.4.3 + virtualenv 15.0.2 + virtualenvwrapper
# Ubuntu 14.04.3 LTS + 3.5.2 (Anaconda 4.1.1)
# Ubuntu 14.04.3 LTS + 3.4.0 (pyenv 20160726)
pip uninstall recipy

# Ubuntu 14.04.3 LTS + 2.7.6
sudo pip uninstall recipy

# Ubuntu 14.04.3 LTS + 3.4.3
sudo pip3 uninstall recipy

# Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3
...not applicable...
```

### Uninstall recipy latest version

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

# Docker 1.12.0 + Ubuntu 14.04.4 LTS + 3.4.3
...not applicable...

# Ubuntu 14.04.3 LTS + 3.5.2 + Anaconda 4.1.1
rm -rf anaconda3/lib/python3.5/site-packages/recipy-0.2.3-py3.5.egg
rm -f anaconda3/bin/recipy

# Ubuntu 14.04.3 LTS + 3.4.0 + pyenv 20160726
rm -f .pyenv/shims/recipy
rm -rf .pyenv/versions/3.4.0/lib/python3.4/site-packages/recipy-0.2.3-py3.4.egg
rm -f .pyenv/versions/3.4.0/bin/recipy
```

### Check recipy has been uninstalled

```
pip freeze | grep recipy
```

### Clean up environment

```
unset EDITOR
rm -rf ~/.recipy
```
