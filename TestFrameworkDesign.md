# recipy test framework design

Mike Jackson, The Software Sustainability Institute / EPCC, The University of Edinburgh

14/09/16

---

## 1. Introduction

A design for a test framework which systematically checks that [recipy](https://github.com/recipy/recipy) correctly logs information about invocations of input and output functions of Python packages.

**Note**

Whether to use solely use Python modules or use classes has been omitted as an implementation detail - either can be used.

The recipy version used to refer to commands, outputs and database formats was 9c8c974177f9df899ee607e19eb79d98d0706eb0, Tuesday September 13 16:19:52 2016.

---

## 2. Key requirements

### 2.1 xUnit test framework integration

The test framework must be able to run within a Python xUnit test framework e.g. [py.test](http://doc.pytest.org/en/latest/):

```
$ py.test RecipyTest.py
```

or [nose2](https://nose2.readthedocs.io):

```
$ nose2 RecipyTest
```

This allows xUnit framework support for test logging and report generation to be exploited, including generation of xUnit-compliant XML test reports e.g.

```
$ py.test --junitxml results.xml RecipyTest.py
$ cat results.xml
<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="0" name="pytest" skips="0" tests="1" time="0.008">
  <testcase classname="xxx_test" file="xxx_test.py" line="0" name="test_sample" time="0.000306844711304">
  </testcase>
</testsuite>
```
```
$ nose2 --plugin nose2.plugins.junitxml --junit-xml RecipyTest
$ cat nose2-junit.xml 
<testsuite errors="0" failures="0" name="nose2-junit" skipped="0" tests="1" time="0.000">
  <testcase classname="" name="test_sample" time="0.000202">
    <system-err />
  </testcase>
</testsuite>
```

**Note** The predecessor of nose2, [nose](http://nose.readthedocs.io/en/latest/), is now deprecated. A comment on their web site states that:

> Nose has been in maintenance mode for the past several years and will likely cease without a new person/team to take over maintainership. New projects should consider using Nose2, py.test, or just plain unittest/unittest2.

### 2.2 Environments 

The test framework must run under any environment in which recipy can run. This includes:

* Operating systems e.g. Linux, Windows, Macintosh.
* Python environments e.g. [Anaconda](https://www.continuum.io), [virtualenv](https://pypi.python.org/pypi/virtualenv) or [pyenv](https://github.com/yyuu/pyenv).
* Continuous integration servers e.g. [Jenkins](https://jenkins.io/).
* Hosted continuous integration services, specifically [Travis CI](https://travis-ci.org/) and [AppVeyor](https://www.appveyor.com/).

### 2.3 Python 2 and 3

The test framework must run under Python 2.7+ and 3+, as recipy runs under both these Python versions.

---

## 3. Testing recipy's logging of packages and functions

### 3.1 Test cases

recipy can be invoked either via inclusion of an 'import recipy' command at the start of a Python script or via '-m recipy' when a Python script is run via the command-line. With this in mind, this test framework does not directly invoke the functions that recipy has been configured to log. Rather, it runs Python scripts, via the operating system, that, in turn, invoke these functions. This mimics how recipy is used in practice.

For each package that recipy can log, a script is written that exercises the functions of the package. Each script has the following API:

```
python SCRIPT.py -f FUNCTION [-i [INPUT1[,INPUT]*]  [-o [OUTPUT1[,OUTPUT]*] 
```

The 'FUNCTION' argument specifies the function of the package to execute, which corresponds to one of the package's functions which recipy can log.

A list of comma-separated input file names is given. The script is expected to use these input file names for functions that read files.

A list of comma-separated output file names is given. The script is expected to use these output file names for functions that write files.

The script creates input files of the given name that are suitable for testing the named function, invokes the function, and ensures that the output files are placed in the given output file names.

So long as the above interface and behaviour is respected, how the script implements this behaviour is undefined. For example, it might use existing input files, or create these on-the-fly.

Each unique combination of script, function, input and/or output files constitutes a unique test case. For example, test cases for numpy could include:

```
python -m recipy run_numpy.py -f loadtxt -i data.csv
python -m recipy run_numpy.py -f loadtxt -i data.gz
python -m recipy run_numpy.py -f loadtxt -i data.bz2
python -m recipy run_numpy.py -f savetxt -o result.csv
python -m recipy run_numpy.py -f savetxt -o result.gz
```

It is also useful to test scenarios including:

* Functions whose behaviour differs depending on their arguments.
* Overloaded functions.
* Scripts that import packages in diverse ways e.g.

```
import numpy as np
np.savetxt("file.csv", data, delimiter=",")

import numpy
numpy.savetxt("file.csv", data, delimiter=",")

import numpy as opaque
opaque.savetxt("file.csv", data, delimiter=",")

import numpy.savetxt as opaque
opaque("file.csv", data, delimiter=",")
```

* Use of 'recipy.open' or 'from recipy import open' plus 'open'.
* Multiple invocations of functions from the same or multiple packages e.g. loading some data, filtering it, then saving it.
* Different scripts for different versions of packages which may differ in terms of their input/output function names and arguments and input/output file formats.

The script API allows for such tests as it places no restriction on the nature of either 'SCRIPT.py' or 'FUNCTION', so, for example, one can have:

```
python -m recipy run_numpy_as_opaque.py -f loadtxt -i data.csv
python -m recipy run_numpy.py -f load_and_savetxt -i data.csv -o result.csv
python -m recipy run_numpy_matplotlib.py -f loadtxt -i data.csv -o plot.png
python -m recipy run_numpy1.11.1.py -f loadtxt -i data.csv -o plot.png
```

### 3.2 Test cases specification

Test cases are specified using [YAML](http://yaml.org/) (YAML Ain't Markup Language), a concise human-readable file format, which can express dictionaries and lists. YAML syntax is:

* `---` indicates the start of a document.
* `:` denotes a dictionary. `:` must be followed by a space.
* `-` denotes a list.

The test cases specification is:

```
---
tests:
  SCRIPT_1:       # Test cases for a specific script
    libraries:    # recipy-logged libraries used by the script
    - LIBRARY_i
    - LIBRARY_ii
    - ...
    functions:
      FUNCTION_A:   # Test cases for a specific test function
      - input:      # Test case 1 - reads input files
        - INPUT 
        - ...
      - input:      # Test case 2  reads input files
        - INPUT 
        - ...
      FUNCTION_B:   # Test cases for a specific test function
      - output:     # Test case 3 - writes output files
        - OUTPUT 
        - ...
      - output:     # Test case 4 - writes output files
        - OUTPUT 
        - ...
      FUNCTION_B:   # Test cases for a specific test function
      - input:      # Test case 5 - reads input and writes output files
        - INPUT 
        - ...
        output:
        - OUTPUT 
        - ...
      FUNCTION_B:
      - ...
  SCRIPT_2:
    ...
```

'libraries' may contain either generic names e.g. 'numpy' (compatible with any version of numpy) or version qualified names e.g. 'numpy v1.11.1' (compatible wity numpy v1.11.1+).

For example:

```
---
tests:
  run_numpy:
    libraries:
    - numpy
    functions:
      loadtxt:
      - input: 
        - sample_input.csv
      - input: 
        - sample_input.gz
      - input: 
        - sample_input.bz2
      savetxt:
      - output: 
        - sample_output.csv
      - output: 
        - sample_output.gz
      load_and_savetxt:
      - input:
        - data.csv
        output:
        - result.csv
```

YAML does not preclude the use of other notations e.g. [JSON](http://www.json.org/). JSON can be considered a subset of YAML (see [YAML version 1.2](http://yaml.org/spec/1.2/spec.html)). For example, the JSON corresponding to the YAML above is:

```
{
  "tests": {
    "run_numpy": {
      "libraries": [ "numpy" ],
      "functions": {
        "loadtxt": [
          { "input": [ "sample_input.csv" ] },
          { "input": [ "sample_input.gz" ] },
          { "input": [ "sample_input.bz2" ] }
        ],
        "savetxt": [
          { "output": [ "sample_output.csv" ] },
          { "output": [ "sample_output.gz" ] }
        ],
        "load_and_savetxt": [
          {
            "input": [ "data.csv" ],
            "output": [ "result.csv" ]
          }
        ]
      }
    }
  }
}
```

**Questions**

I run hot and cold on YAML indentation, especially the subtle difference between lists and dictionaries which isn't always clear when it's deeply indented. Just use JSON as a file format?

### 3.3 Running a single test case

A 'test_case' module provides the following function to run a single test case.

```
def run_test_case(test_cases_directory, test_case, libraries)
```

Run a single test case, where:

* 'test_cases_directory': directory containing test cases.
* 'test_case': test case consisting of:
  - 'script': a script e.g. 'run_numpy.py'.
  - 'function': a function e.g. 'loadtxt', 'load_and_savetxt'.
  - 'inputs': a list of zero or more input files e.g. ['data.csv'].
  - 'outputs': a list of zero or more output files e.g. ['result.csv'].
* 'libraries': a list of one or more libraries e.g. ['numpy'].

It operates as follows:

* If any path to a script, input, or output, is relative and 'test_cases_directory' is defined then the paths are prefxed by 'test_cases_directory'.
* The test case script is run via 'python -m recipy script -f function -i inputs -o outputs'.
* The ID and the log for the most recent run are retrieved from the database.
* The log is checked to ensure that information about the run has been recorded correctly.

recipy stores the following information about each test in its database:

```
"command": "/home/ubuntu/anaconda2/bin/python",
"command_args": "",
"libraries": ["recipy v0.3.0", "numpy v1.11.1"],
"script": "/home/ubuntu/run_numpy.py", 
"inputs": [ [
              "/home/ubuntu/data.txt", 
              "130a24d9b9d2cf2f0108c180ffa7f3398dc9c826"
          ] ], 
"outputs": [ [
              "/home/ubuntu/result.csv", 
              "130a24d9b9d2cf2f0108c180ffa7f3398dc9c826"
          ] ], 
"date": "{TinyDate}:2016-09-12T09:40:20", 
"exit_date": "{TinyDate}:2016-09-12T09:40:20", 
"author": "ubuntu",
"description": "", 
"warnings": [], 
"environment": [
  "Linux-3.19.0-25-generic-x86_64-with-debian-jessie-sid", 
  "python 2.7.12 |Anaconda custom (64-bit)| (default, Jul  2 2016, 17:42:40) "
  ],
"unique_id": "118311e9-0ceb-435a-a0d0-5d95749b9a51",
"gitrepo": "/home/ubuntu/samples",
"gitorigin": null, 
"gitcommit": "a10b155c1842ad12f4e6278c0acf7a8b5d914a18",
"diff": "\n\n\n@@ -4,4 +4,5 @@ import numpy as np\n data = np.array([list(range(4,8)), list(range(12,16))])\n np.savetxt(\"tmp.csv\", data, delimiter=\",\")\n np.loadtxt(\"tmp.txt\", delimiter=\",\")\n+np.loadtxt(\"tmp.csv\", delimiter=\",\")\n \n"
```

The following checks are done:

* There is only one new run in the database i.e. number of logs has increased by 1.
* 'unique_id' matches that returned from the database.
* Files listed in 'script', 'inputs', 'outputs', 'libraries' match those in 'test_case'.
* 'libraries' also includes 'recipy'.
* 'command_args' matches '-f ... -i ... -o ...', the arguments passed to the script by the 'shell' module (section 5.1).
* 'date' and 'exit_date' are valid dates, record the current year, month and day and 'date' <= 'exit_date'.
* 'author' holds the current user.
* 'description' is empty.
* 'warnings' is an empty list.
* 'command' holds the current Python interpreter.
* 'environment' holds the operating system and version of the current Python interpreter.

'gitrepo', 'gitorigin', 'gitcommit' and 'diff' are the remit of Git and diff-related tests described in section 4.3 below.

The recipy database is *not* cleared between test runs as this allows the check to be done that running a script adds a new log entry yet does not remove any existing ones.

How the test case runner accesses the database, via the 'database' module (Section 5.2), is implementation-specific.

### 3.4 Running all the test cases

Providing an xUnit test-framework compliant test function for each test case is unscalable due to the number of possible tests. It also results in a lot of duplicated code. Ideally, we want to run the following algorithm:

```
FOR EACH script_name IN test_cases_specification:
  script = test_cases_specification[script_name]
  libraries = script["libraries"] or [] if none
  functions = script["functions"]
  FOR EACH function_name IN functions:
    FOR EACH input_output IN functions[function_name]:
      test_case = {}
      test_case["script"] = script_name
      test_case["function"] = function_name
      test_case["inputs"] = input_output["inputs"] or [] if none
      test_case["outputs"] = input_output["outputs"] or [] if none
      run_test_case(test_cases_directory, test_case, libraries)
```

The algorithm should also filter test cases such that a test case is only generated if all its libraries are available within the current Python environment. For example, if libraries includes 'numpy' then numpy should be available, if it includes 'numpy v1.11.1' then this version, or later, should be available (see the 'environment' module, section 5.4).

A (naive) implementation of the test framework is to invoke each test case within a single test function, e.g.:

```
def run_test_cases():
  GET test_cases_directory
  GET test_cases_specification
  RUN test cases algorithm
```

This would be compliant with both py.test and nose2. However, the test function either passes, if every test case passes, or fails, if any test case fails. A successful run would be reported as follows:

```
$ py.test RecipyTest.py
============================= test session starts ==============================
platform linux2 -- Python 2.7.12, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
rootdir: /home/ubuntu/samples, inifile: 
collected 1 items 

RecipyTest.py .

=========================== 1 passed in 0.00 seconds ===========================
```

```
$ nose2 RecipyTest
.....
----------------------------------------------------------------------
Ran 1 test in 1.000s

OK
```

This approach is neither very useful - if one test case failure prevents the other tests from running - nor very informative. While verbose output could help a developer track down the failed test cases, this does not exploit the built-in support provided by xUnit test frameworks for report generation.

There are a number of approaches to ensuring that each of the test cases is treated as a separate test but without requiring writing test functions for each of these. These approaches are xUnit test framework-specific.

The following were evaluated using an example inspired by Python 3.4 [sub-tests](https://docs.python.org/dev/library/unittest.html#distinguishing-test-iterations-using-subtests), testing numbers from 0 to 5 inclusive for whether they are even, a test passing if a number is even, failing otherwise.

**Python 3.4 sub-tests**

Python 3.4 introduced [sub-tests](https://docs.python.org/dev/library/unittest.html#distinguishing-test-iterations-using-subtests) which allows a single test function to be run across multiple test cases. For example:

```
import unittest

class NumbersTest(unittest.TestCase):

    def test_even(self):
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

When run via 'python -m unittest' only one test function is reported having run.

When run via py.test or nose2 the first test case that fails results in the others not running. For py.test, this is currently subject of an open issue [Support for Python 3.4 unittest subtests #1367](https://github.com/pytest-dev/pytest/issues/1367).

As sub-tests are only supported in Python 3.4+ they're not a suitable option for the test framework.

**nose2 test generators**

nose2 supports [test generators](http://nose2.readthedocs.io/en/latest/plugins/generators.html) which dynamically generate test functions from a list of values (e.g. numbers, strings or tuples). For example:

```
def test_even():
    for i in range(0, 6):
        yield is_even, i

def check(i):
    assert i % 2 == 0
```

When run, test functions 'test_even:1', ..., 'test_even:6' are dynamically created and run. Individual tests can be run using these names e.g.

```
$ nose2 nose.test_generator.test_even:1
```

There is no relation between the numbers here and those in the range - if iterating over a list of strings or tuples, the test functions would still be numbered 1 to N. It is not clear how to define custom, more meaningful, test function names.

nose2 test generators can run under Python 2.6+ and 3.2+ and PyPy, and can also be used within the scope of Python 'unittest' classes.

**nose_parameterized**

[nose_parameterized](https://pypi.python.org/pypi/nose-parameterized/) is a package which dynamically generates test functions from a list of tuples. For example:

```
from nose_parameterized import parameterized

@parameterized.expand([ (0,), (1,), (2,), (3,), (4,), (5,) ])

def test_even(i):
    assert i % 2 == 0
```

When run, test functions 'test_even_0', ..., 'test_even_5' are dynamically created and run. Test function names are derived from the tuples. Individual tests can be run using these names e.g.

```
$ nose2 nose_params.test_params.test_even_4
```

Developers can define a callback function to define their own custom names. Here is an example of such a callback function and providing the tuples via another callback function:

```
from nose_parameterized import parameterized

def even_case_name(testcase_func, param_num, param):
  (value,) =  param.args
  return parameterized.to_safe_name(str(testcase_func.__name__ + "_custom_" + str(value)))

def get_values():
    return [ (0,), (1,), (2,), (3,), (4,), (5,) ]

@parameterized.expand(get_values(),
                      testcase_func_name=even_case_name)
def test_even(i):
    assert i % 2 == 0
```

```
$ nose2 nose_params.test_params_custom.test_even_custom_4 
```

nose_parameterized can run under Python 2.6+ and 3.2+ and PyPy, and can also be used within the scope of Python 'unittest' classes.

**py.test test parameterization**

py.test supports [parameterization](http://doc.pytest.org/en/latest/parametrize.html) which dynamically generates test functions from a list of values (e.g. numbers, strings or tuples). For example:

```
import pytest

@pytest.mark.parametrize("i", [0, 1, 2, 3, 4, 5])
def test_even(i):
    assert i % 2 == 0
```

When run, test functions 'test_even[0]', ..., 'test_even[5]' are dynamically created and run. Test function names are derived from the list elements. Individual tests can be run using these names e.g.

```
$ py.test pytest/test_parameterize.py::test_even\[5\] 
```

As for nose_parameterized, developers can define a callback function to define their own custom names. Here is an example of such a callback function and providing the values via another callback function:

```
import pytest

def get_values():
    return [ 0, 1, 2, 3, 4, 5 ]

def even_case_name(value):
    return "custom_" + str(value)

@pytest.mark.parametrize("i", get_values(), ids=even_case_name)
def test_even(i):
    assert i % 2 == 0
```

```
$ py.test pytest/test_parameterize_custom.py::test_even\[custom_5\]
```

Stacked parametization is also supported, to run the Cartesian product of sets of parameters e.g.

```
def a_case_name(value):
    return "a_" + str(value)

def b_case_name(value):
    return "b_" + str(value)

@pytest.mark.parametrize("i", get_values(), ids=a_case_name)
@pytest.mark.parametrize("j", get_values(), ids=b_case_name)
def test_equals_stacked(i, j):
    assert i == j
```

generates test functions for 'test_equals_stacked[b_0-a_0]', ..., 'test_equals_stacked[b_5-a_5]'.

py.test parameterized tests can run under Python 2.6+ and 3.3+ and PyPy, and can also be used within the scope of py.test test classes.

**Choosing a test framework**

nose2 test generators, nose_parameterized and py.test parameterized tests all support dynamic creation of test functions, which are run, and reported, as separate tests. py.test and nose_parameterized further support customised test function names which can contribute to informative test reports. 

An informal search online gives the impression that py.test is preferred to nose2 by developers, so that will be adopted. The differences from nose2 test generators or nose_parameterized are not so great as to preclude a straightforward transition in future, if desired. 

**Bootstrapping dynamic creation of parameterized tests**

As the test functions are dynamically created when the py.test module is loaded, there is a need for the test cases specification to be loaded when the module is loaded, or before it is loaded (as module upon which the test module is dependent) so that its contents are available to py.test so it can generate functions using the test cases specification to create parameters. This is possible and a simple example is as follows. This code reads script names from a configuration file, provided via an environment variable:

```
import os
import pytest

def get_scripts():
    with open(config_file) as f:
        scripts = [line.strip('\n') for line in f.readlines()]
    return scripts

config_file = os.environ["RECIPY_TEST_CASES_CONFIG"]

def case_name(value):
    return "script_" + str(value)

@pytest.mark.parametrize("script", get_scripts(), ids=case_name)
def test_script(script):
    if script == "sklearn":
        pytest.fail(script, " failed its test")
    else:
        pass
```

Using a configuration file, scripts.txt:

```
numpy
pandas
skimage
sklearn
bs4
```

here is a test run, with py.test's '-v', verbose, mode enabled to print the test functions as they are run:

```
$ RECIPY_TEST_CASES_CONFIG=pytest/scripts.txt py.test -v pytest/test_parameterize_bootstrap.py 
============================= test session starts ==============================
platform linux -- Python 3.5.2, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /home/ubuntu/anaconda3/bin/python
cachedir: pytest/.cache
rootdir: /home/ubuntu/recipy-test/test-frameworks/pytest, inifile: 
collected 5 items 

pytest/test_parameterize_bootstrap.py::test_script[script_numpy] PASSED
pytest/test_parameterize_bootstrap.py::test_script[script_pandas] PASSED
pytest/test_parameterize_bootstrap.py::test_script[script_skimage] PASSED
pytest/test_parameterize_bootstrap.py::test_script[script_sklearn] FAILED
pytest/test_parameterize_bootstrap.py::test_script[script_bs4] PASSED

=================================== FAILURES ===================================
_________________________ test_script[script_sklearn] __________________________

script = 'sklearn'

    @pytest.mark.parametrize("script", get_scripts(), ids=case_name)
    def test_script(script):
        if script == "sklearn":
>           pytest.fail(script, " failed its test")
E           Failed: sklearn

pytest/test_parameterize_bootstrap.py:17: Failed
====================== 1 failed, 4 passed in 0.03 seconds ======================
```

### 3.5 Configuring the test framework

The test framework expects the following configuration:

* recipy database, default '~/.recipy/recipyDB.json'.
* Test case scripts directory, default 'test-cases'.
* Test cases configuration file, default 'test-cases.yaml'.

These can be specified via the following environment variables:

* 'RECIPY_DATABASE'
* 'RECIPY_TEST_CASES'
* 'RECIPY_TEST_CASES_CONFIG'

A 'configuration' module configures the test framework. It:

* Checks whether the environment variables are defined and, if so, extracts their values.
* Caches the locations of the recipy database, test case scripts directory and test cases configuration file.
* Loads the test cases configuration file, via the 'yaml_utils' module (section 5.3), and caches the configuration.
* Opens a connection to the recipy database, and caches this connection, via the 'database' module (section 5.2).
* Acceses information on the Python interpreter, libraries, environment (operating system and Python version) and current user, via the 'environment' module (section 5.4).

How this module caches environment variable values, test cases configuration, and database connection, and environment information is implementation specific.

**Implementation**

Python's [os](https://docs.python.org/2/library/os.html) module provides functions to access environment variables. For example:

```
import os
os.environ["RECIPY_TEST_CASES_CONFIG"]
```

---

## 4. Testing other aspects of recipy

The following tests are each implemented as one or more xUnit test framework-compliant modules. These tests use:

* A Python script that uses a package and functions logged by recipy and both inputs and outputs files and which is run as a pre-requisite of each test (except those that test recipy's '-h' and '--version' flags).
* The 'shell' (section 5.1) module to run this script.
* The 'database' (section 5.2) module to access information from the recipy database.
* The 'environment' (section 5.4) and 'version_control' (section 5.5) modules to access environment and Git information.

### 4.1 'import recipy' test

A tests for scripts using 'import recipy':

* 'python -m recipy script.py ...' is run.
* The database is queried for the most recent log entry.
* 'import recipy' is added to the start of the script.
* 'python script.py ...' is run.
* The database is queried for the most recent log entry.
* The log entries are compared for equality. All their entries should be equal except those for 'unique_id', 'date', and 'exit_date'.

### 4.2 Command-line parameters tests

Tests for recipy's command-line parameters include the following:

* 'recipy' exits with exit code 1.
* 'recipy -h'.
* 'recipy --version'.
* 'recipy latest' exits with exit code 1 if there is no entries in the database.
* 'recipy latest' prints text matching the following template, with entries corresponding to the latest log in the database.

```
Run ID: HASH
Created by AUTHOR on DATE
Ran SCRIPT using COMMAND
Git: commit COMMIT, in repo REPOSITORY, with origin ORIGIN
Environment: OPERATING_SYSTEM, PYTHON
Libraries: NAME vVERSION, ...
Inputs:
  INPUT (FILE_HASH)
  ...
Outputs:
  OUTPUT (FILE_HASH)
  ...
```

* 'recipy latest -j' prints a JSON document matching that corresponding to the latest log in the database.
* 'recipy latest --diff' prints the same as 'recipy latest'.
  - Git and diff-related tests are described in section 4.3 below.
* 'recipy search -i HASH' prints text matching the template above.
* 'recipy search -i HASH_SUBSTRING', as above.
* 'recipy search -i HASH -j' prints a JSON document matching that corresponding to the log for HASH in the database.
* 'recipy search -i nosuchid' prints 'No results found' on standard output.
* 'recipy search -i HASH stuff' fails with exit code 1.
* 'recipy search -p file.txt', as for 'recipy search -i HASH'.
* 'recipy search -p file.txt -a', as for 'recipy search -i HASH' but with multiple occurrences of the template.
* 'recipy search -f file.txt' prints 'No results found' on standard output.
* 'recipy search -f ile.t', as for 'recipy search -i HASH'.
* 'recipy search -f aile.t' prints 'No results found' on standard output.
* 'recipy search -r "file.txt"', as for 'recipy search -i HASH'.
* 'recipy search -r ".*ile.*"', as for 'recipy search -i HASH'.
* 'recipy search -r ".*aile.*"' prints 'No results found' on standard output.
* 'recipy search file.txt stuff' fails with exit code 1.

Additional tests, which are variants of the above:

* Requesting JSON outputs using '-j', for 'recipy latest' and 'recipy search'.
* Requests for all matching outputs using '-a', for 'recipy search'.
* Long-form versions of flags '--help', '--json', '--id', '--file-path, '--fuzzy', '--regexp', '-all'.
* Running commands with '--debug'.

All recipy invocations are expected to return an exit code of 0 except where noted.

Results are checked by capturing standard output, then either performing pattern matching in the output or parsing it into JSON document(s), depending upon the test.

**Note**

Testing 'recipy annotate; is problematic as it requires interaction with an editor.

It is not clear what this recipy flag does:

```
-v --verbose  Be verbose
```

**Questions**

Is this too much? Is there a need to perform pattern matching on the output? Would parsing the JSON equivalents be sufficient?

### 4.3 'recipy --diff' and Git tests

Tests for 'recipy --diff' and Git require that the Python script that is logged by recipy has been commited to a Git repository.

To test this command if the script is unchanged:

* 'python -m recipy script.py ...' is run.
* 'recipy latest' is run and standard output captured.
* 'recipy latest --diff' is run and standard output captured.
* Standard output from both runs of recipy is checked, it should be equal.
* The database is queried for the most recent log entry, and the 'diff' section is checked for equality with "".

To test this command if the script is changed:

* "print('hello')" is appended to script.py.
* 'recipy latest --diff' is run and standard output captured.
* Standard output is checked to ensure it has lines matching:

```
-
+print("Hello")
```

* The database is queried for the most recent log entry, and the 'diff' section is checked for equality with "\n+print(\"Hello\")\n".

### 4.4 'recipyrc' tests

Tests of recipy configuration, provided via 'recipyrc' configuration files, include the following. For each, 'recipyrc' configuration files are created on a test-by-test basis.

Configuration file precedence:

* If neither '.recipyrc', 'recipy' nor '~/recipyrc' exist then recipy uses its default configuration.
* If '~/recipy/recipyrc' is present. then its configuration is used.
* If both '.recipyrc' and '~/recipy/recipyrc' are present then the former's configuration is used.
* If both 'recipyrc' and '~/recipy/recipyrc' are present then the former's configuration is used.
* If both 'recipyrc' and '.recipyrc' are present then the former's configuration is used.
* One way of testing these is to use the '[database]path' configuration value and set it to a different location in each file, then check that the database is created in the location specified by the file that is expected to take precedence.

Unknown configuration:

* If an unknown configuration section, e.g. '[unknown]', is in the file then it is ignored and the script and 'recipy latest' successfully run.
* If an unknown configuration value, e.g. 'unknown', is in the file then it is ignored and the script and 'recipy latest' successfully run.

[general] configuration:

* If 'debug' is present then running the script prints text matching the following template, with entries corresponding to the latest log in the database:

```
recipy run inserted, with ID HASH
Patching PACKAGE
Patching input function: INPUT_FUNCTION
Patching input function: ...
Patching output function: OUTPUT_FUNCTION
Patching output function: ...
Output to OUTPUT using PACKAGE
...
Input from INPUT using PACKAGE
...
recipy run complete
```

* If 'quiet' is present then running the script prints nothing.

[data] configuration:

* If 'file_diff_outputs' is present then creating empty files with names identical to those created by a script will result in the most recent log entry having a 'filediffs' entry matching the following template, where 'run_id' matches the numerical index of the latest log entry:

```
{"FILE_DIFFS_NUMBER": 
  {"diff": "--- before this run\n+++ after this run\n@@ ... ... ...\n",
  "filename": "OUTPUT_FILE",
  "tempfilename": "TMP_FILE_NAME",
  "run_id": RUN_NUMBER}
}
```

* If 'file_diff_outputs' is present then running the script twice, will result in the most recent log entry having a 'filediffs' entry matching the following template, where 'run_id' matches the numerical index of the latest log entry:

```
{"FILE_DIFFS_NUMBER": 
  {"diff": "",
  "filename": "OUTPUT_FILE",
  "tempfilename": "TMP_FILE_NAME",
  "run_id": RUN_NUMBER}
}
```

[database] configuration:

* If 'path' is valid, then the script successfully runs and a database is created at 'path'.
* If 'path' is invalid or includes a path that does not exist then the script fails with exit code 1.
* If 'path' is not present then the script successfully runs and a database is created at '~/.recipy/recipyDB.json'.

[ignored metadata] configuration:

* If 'diff' is present, and the script has been commited to a Git repository, then the most recent log entry has no 'diff' entry.
* If 'git' is present, and the script has been commited to a Git repository, then the most recent log entry has no 'gitrepo', 'gitorigin' or 'gitcommit' entries.
* If 'input_hashes' is present, then there are no hashes recorded for input files.
* If 'output_hashes' is present, then there are no hashes recorded for output files.

[ignored inputs] configuration:

* If this includes a package used by the script (e.g. numpy) then the most recent log entry has no members in its 'input' entry for the files loaded using the functions of that package.
* If this is 'all' then the most recent log entry has 'input' entry equal to [].

[ignored outputs] configuration:

* If this includes a package used by the script (e.g. numpy) then the most recent log entry has no members in its 'output' entry for the files loaded using the functions of that package.
* If this is 'all' then the most recent log entry has 'input' entry equal to [].

**Questions**

Again, is this too much?

---

## 5. Utility modules

### 5.1 Running Python scripts

A 'shell' module provides the following functions to run Python scripts.

```
def execute(python, script, function, inputs, outputs)
```

Execute a Python script and return its standard output, standard error and exit code, where:

* 'python': a list of strings constituting the commands to run the script e.g. ['python'] or ['python', '-m', 'recipy'].
* 'script': a script e.g. 'run_numpy.py'.
* 'function': a function e.g. 'loadtxt', 'load_and_savetxt'.
* 'inputs': a list of zero or more input files e.g. ['data.csv'].
* 'outputs': a list of zero or more output files e.g. ['result.csv'].

Paths may be absolute or relative.

'execute' uses its arguments to create a command-line command for execution e.g.

```
python -m recipy run_numpy.py -f loadtxt -i data.csv
python run_numpy.py -f load_andsavetxt -i data.csv -o result.csv
```

The '-f', '-i' and '-o' flags are passed in by the caller as part of the input and output lists, to avoid hard-coding these here.

The command is invoked and standard output and standard error captured.

If any problems arise, then an exception is raised:

```
class ScriptError(Exception)
```

**Implementation**

Python's [subprocess](https://docs.python.org/2/library/subprocess.html) module can invoke command-line tools and capture return codes, output and error streams e.g.

```
cmd = ['python', 'run_numpy.py', '-f', 'loadtxt', '-i', 'data.csv']
stdout = open("stdout.txt", "a")
stderr = open("stderr.txt", "a")
result = subprocess.call(cmd, stdout=stdout, stderr=stderr)
stdout.close()
stderr.close()
```

### 5.2 Querying the recipy database

A 'database' module provides the following functions to query the recipy database.

```
def open(connection)
```

Open a connection to a database, where 'connection' is a dictionary of information needed to open a connection to the database. The dictionary contents are database-specific.

```
def get_latest_id()
```

Get the ID of the most recent log.

```
def get_log(id)
```

Get a Python dictionary with the log with the given ID, where 'id' is a log ID.

```
def number_of_logs()
```

Get the number of logs in the database.

```
def close()
```

Close the connection to the database.

If any problems arise, then an exception is raised:

```
class DatabaseError(Exception)
```

How this module caches database connection information and the connection itself, and exposes these to the rest of the test framework, is implementation specific.

### 5.3 Loading YAML files

A 'yaml_utils' module provides the following functions to load YAML files.

```
def load_yaml(file_name = None)
```

Load a YAML file and return its contents as a Python dictionary, where 'file_name' is the name of the YAML file to load.

If there are any problems then an error is raised:

```
class YamlError(Exception)
```

**Implementation**

[PyYAML](http://pyyaml.org/wiki/PyYAML) is a Python package for parsing YAML strings or files into Python dictionaries.

An example of of using PyYAML, and Python's [json](https://docs.python.org/2/library/json.html) module:

```
import yaml
import json

with open('file.yaml','r') as f:
    data = yaml.load(f)
yaml_doc = yaml.dump(data)
json_doc = json.dumps(data)
data = yaml.load(json_doc)
```

### 5.4 Accessing environment information

An 'environment' module provides the following functions to access information about the execution environment.

```
def get_str_as_date(date)
```

Convert string to date object, where 'date' is a date string e.g. '2016-09-12T09:40:20'.

```
def get_tinydatestr_as_date(date)
```

Convert TinyDate string to date object, where 'date' is a date string e.g. '{TinyDate}:2016-09-12T09:40:20'.

```
def get_user()
```

Get current user.

```
def get_python_exe()
```

Get Python executable path.

```
def get_python_version()
```

Get Python version.

```
def get_os()
```

Get operating system.

```
def is_package_installed(package)
```

Is a package installed, where 'package' is a Python package name e.g. 'numpy'.

```
def get_package_version(package)
```

Get a package version, where 'package' is a Python package name e.g. 'numpy'. If there is no recorded version then "" is returned. If the package is not installed then 'None' is returned.

**Implementation**

[python-dateutil](https://pypi.python.org/pypi/python-dateutil) is a Python package with date-time utilities. For example:

```
from dateutil.parser import parse
date = '2016-09-12T09:40:20'
parse(date)
date = '{TinyDate}:2016-09-12T09:40:20'.replace('{TinyDate}:', '')
parse(date)
```

Python's [getpass](https://docs.python.org/2/library/getpass.html) module provides a function to get the current user:

```
import getpass
getpass.getuser()
```

Python's [sys](https://docs.python.org/2/library/sys.html) and [platform](https://docs.python.org/2/library/platform.html) modules provide functions to get the Python executable path, version and platform:

```
import sys
import platform
sys.executable
sys.version
platform.platform()
```

recipy uses these functions.

Python's [pip](https://pypi.python.org/pypi/pip) package provides information about installed Python packages. For example:

```
import pip
packages = pip.get_installed_distributions()
packages_dict = {}
for package in packages:
    packages_dict[package.key] = package

packages_dict['numpy'].key
packages_dict['numpy'].has_version()
packages_dict['numpy'].version
```

### 5.5 Accessing Git information

A 'version_control' module provides the following functions to provide information about a Git repository.

```
def get_repository()
```

Get local repository path.

```
def get_commit()
```

Get current commit ID.

```
def get_origin()
```

Get current repository origin.

```
def hash_file(path)
```

Get hash of file, where:

* path: path to file.

**Implementation**

[gitpython](https://pypi.python.org/pypi/GitPython/) is a Python package to interact with Git. For example:

```
from git import Repo
script_path = os.path.realpath('script.py')
repository = Repo(script_path, search_parent_directories=True)
repository.working_dir
repository.head.commit.hexsha
repository.remotes.origin.url
```

recipy uses these functions. recipy's recipyCommon/version_control.py has a suitable hash_file implementation.

---

## 6. Validating that recipy does not change behaviour of user scripts

It is important that recipy does not change the behaviour of the scripts it is used to log. However, it is hard to see how this can be tested as it is hard to envisage the multiplicity of scripts which recipy could be used in conjunction with. This is a challenge faced by the developers of any software library.

I'd suggest making this a support issue, and specifically highlighting it to users along the lines below.

### 6.1 Sample help and support statement

If you find that your script's behaviour changes as a result of using recipy (e.g. produces different results or unexpectedly fails), then please contact us. 

Provide us with information on:

* Operating system and version.
* Python version. You can find this via:
 
```
python --version
```

* recipy version. 

  - If you are using a recipy package, installed via pip, you can find this via:
 
    ```
    recipy --version
    ```

  - If you are using a version of recipy from Git, you can find this via:

    ```
    git rev-parse HEAD
    ```

* Python libraries. You can find this via:

```
pip freeze
```

* Any error messages and exceptions that you see.
  - If providing exceptions then provide these exactly as displayed in a terminal window.
  - Do not provide a vague textual summary like "It threw an error".
* Your script itself, if possible. If you do not wish to share your script via a GitHub issue, then please contact us directly or provide a short Python program for repeating the problem.
* Provide any other information you think will help.
* Clearly separate fact from speculation.

---

## 7. Python 2 and 3 compliance

All Python files will include:

```
from __future__ import (nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals)
```

as described in the Python 2 [__future__](https://docs.python.org/2/library/__future__.html) library.

All changes proposed by the Python [2to3](https://docs.python.org/2/library/2to3.html) tool will be applied.

[Supporting Python 2 and 3 without 2to3 conversion](http://python3porting.com/noconv.html) provides information useful for developing code compliant with both Python 2 and 3.

---

## 8. Co-locating the test framework with recipy

It is recommended that the test framework code be co-located with recipy's source code, in [recipy](https://github.com/recipy/recipy):

* Any developer who gets recipy, gets the test framework.
* Changes commited to recipy can automatically be detected and trigger a run of the tests within a continuous integration server (e.g. Travis CI or AppVeyor).

This incurs the following changes to recipy:

* Packages required by this test framework are added to test_requirements.txt.
* A module, 'integration_test' is created to hold the test framework modules and 'test_cases'.
* Documentation is added on how to run the test framework, and add tests for packages logged by recipy.

Development of the test framework can take place in a separate branch until stable.
