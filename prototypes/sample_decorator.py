# http://thecodeship.com/patterns/guide-to-python-function-decorators/

from functools import wraps
import numpy as np

# Experiments with func, args, kwargs
#
# http://stackoverflow.com/questions/817087/call-a-function-with-argument-list-in-python

def caller_args(func, args):
    print("==== caller_args:")
    print(func)
    print(args)
    func(*args)

def caller_args_kwargs(func, *args, **kwargs):
    print("==== caller_args_kwargs:")
    print(args)
    print(kwargs)
    func(*args, **kwargs)

def caller_args_list(func, args):
    print("==== caller_args_list:")
    print(args)
    func(*tuple(args))

def caller_args_list_kwargs_dict(func, args, kwargs):
    print("==== caller_args_list_kwargs_dict:")
    print(args)
    print(kwargs)
    func(*tuple(args), **kwargs)

data = [[1, 2, 3]]
caller_args(np.savetxt, ["ca.csv", data])
caller_args_kwargs(np.savetxt, "cak.csv", data, delimiter=',')
caller_args_list(np.savetxt, ["cal.csv", data])
caller_args_list_kwargs_dict(np.savetxt, ["calkd.csv", data], {"delimiter": "_"})

# Calling functions via func, args and kwargs with input and output
# files wrapped in classes so they can be auto-detected.

class Wrapper:
    def __init__(self, obj):
        self._obj = obj
    @property
    def obj(self):
        return self._obj
    
class InputWrapper(Wrapper):
    def __init__(self, obj):
        self._obj = obj

class OutputWrapper(Wrapper):
    def __init__(self, obj):
        self._obj = obj

# Global variables to record input and output files - need a nicer way
# of doing this!

INPUTS = []
OUTPUTS = []

def filter(func, *args, **kwargs):
    print("==== filter")
    list_args = list(args)
    filter_args = []
    inputs = []
    outputs = []
    # Any inputs or outputs that are wrapped are unpacked from their
    # wrapper and recorded in inputs or outputs.
    for arg in args:
        if isinstance(arg, InputWrapper):
            inputs.append(str(arg.obj))
            filter_args.append(arg.obj)
        elif isinstance(arg, OutputWrapper):
            outputs.append(str(arg.obj))
            filter_args.append(arg.obj)
        else:
            filter_args.append(arg)
    for key in kwargs.keys():
        if isinstance(kwargs[key], InputWrapper):
            inputs.append(str(kwargs[key].obj))
            kwargs[key] = kwargs[key].obj
        elif isinstance(kwargs[key], OutputWrapper):
            outputs.append(str(kwargs[key].obj))
            kwargs[key] = kwargs[key].obj
    INPUTS.append(inputs)
    OUTPUTS.append(outputs)
    print("==== filter recorded inputs/outputs:", inputs, outputs)
    return func(*tuple(filter_args), **kwargs)

# A recipy test script developer could call functions that they want
# to test are logged by recipy, as follows:

filter(np.savetxt, InputWrapper("filter.csv"), data, delimiter=',')
print("Inputs:", INPUTS)
print("Outputs:", OUTPUTS)

# In this way the inputs and outputs are automatically captured, with
# little extra coding for the developer.

# The following is decorator to annotate a function with information
# about what it is expected will end up in the recipy logs: libraries,
# input files and output files.
#
# The input files and output files complement those captured by
# filter, above. These are intended for functions that do not
# explicitly take an input or output file name, but create these
# derived from other arguments. For example, something like a function
# convert("data.csv", "tsv") which could implicitly save a "data.tsv"
# file.
#
# Question: how does recipy itself handle such functions?
# Question: how does recipy itself detect which function arguments are
# files and which are not?

# Global variables - need a nicer way of doing this, especially
# since we want to keep information about decorated functions
# separate.
# Use of same variables as for filter is intentional, so INPUTS
# and OUTPUTS hold both the input and output files logged via
# filter and the implicit files provided via the decorator.

INPUTS = []
OUTPUTS = []
LIBRARIES = []

def recipy_test(libraries, inputs, outputs):
    print("=== recipy_test decorator")
    def recipy_run(func):
        print(func.__name__)
        @wraps(func)
        def func_wrapper():
            LIBRARIES.append(libraries)
            INPUTS.append(inputs)
            OUTPUTS.append(outputs)
            return func()
        return func_wrapper
    return recipy_run

@recipy_test(libraries=["numpy"], inputs=["someinput.csv"], outputs=["someoutput.csv"])
def run_numpy():
    print("==== run_numpy")
    filter(np.savetxt, InputWrapper("run1.csv"), data, delimiter=',')
    filter(np.savetxt, InputWrapper("run2.csv"), data, delimiter=',')
    return 123

print(run_numpy())
print("Libraries:", LIBRARIES)
print("Inputs:", INPUTS)
print("Outputs:", OUTPUTS)

# For the desired configuration e.g.

# 'script': 'run_numpy.py'
# 'libraries' ['numpy', 'matplotlib.pyplot', 'numpy v1.11.1']
# 'arguments': ['-f', 'loadtxt', '-i', 'data.csv']
# 'inputs': ['population.csv']
# 'outputs': ['population.jpg']

# the above filter and decorators can provide libraries, inputs,
# outputs as a side-effect of running the script itself (e.g. in a
# script.recipy.json file - constructing this can be the
# responsibility of a super-class constructor or decorator). The test
# framework could then read this in and use it for validation.

# But what about?
# * script
# * arguments
# So the test framework knows how to run the script in the first
# place?
# script could be provided in a configuration file. If there are no
# arguments, libraries, inputs, outputs entries then the test
# framework assumes it's a recipy test script which uses the above
# decorators and creates its own validation configuration (otherwise,
# for arbitrary third-party scripts this can be written manually).
#
# But what about specifying the arguments of these test scripts? These
# could be written manually along with the script name. However,
# recipy test scripts could take a --recipy-tests flag that
# provides a list of command-line flags. Each corresponds to a
# distinct invocation of one or more functions logged by recipy
# e.g. loadtxt, savetxt, load_and_savetxt. The test framework runs
# each of these in turn 
# e.g.
# python some_script.py loadtxt
# python some_script.py savetxt
# python some_script.py loadandsavetxt
# ...
# and, for each run, the libraries/inputs/outputs data is read (as
# mentioned above) and used for validation.
#
# What about input and output files? Make this the responsibility of
# the test script itself. It must create its own input and output
# files, or read these in from somewhere (but it is not expected that
# the caller (i.e. the test framework) provide these. So long as it
# outputs the libraries/inputs/outputs configuration, then the test
# framework can access these.

# So, if wanting the test framework to run a 'real world' script which
# reads some data and outputs a plot, they provide full configuration
# e.g.:

# 'script': 'plot_analysis.py'
# 'libraries' ['numpy', 'matplotlib.pyplot']
# 'arguments': ['--title=Results', '--d=population.csv', '--format==jpg']
# 'inputs': ['population.csv']
# 'outputs': ['population.jpg']

# For a recipy test script they specify:

# 'script': 'run_numpy.py'

# For such scripts, the test framework:
# * Assumes that: 'arguments': []
# * Runs 'python run_numpy.py --recipy-tests' to get a list of
#   function names, each of which corresponds to a specific invocation
#   of one or more functions logged by recipy.
# * For each function in the list of functions:
#   - Run 'python run_numpy.py function-name'
#   - Read script.recipy.json to get libraries, inputs, outputs
#   - Validate against recipy database


