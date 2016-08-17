"""
Usage:

    python run_matplotlib.pyplot.py savefig plot.png
"""
from __future__ import print_function
import matplotlib
import matplotlib.pyplot as plt
import sys


def invoke_savefig(arguments):
    file_name = arguments[0]
    # Set non-interactive matplotlib back-end.
    matplotlib.use('Agg')
    plt.plot([1,2,3])
    print("Saving plot: ", file_name)
    plt.savefig(file_name)


if len(sys.argv) < 3:
    print(__doc__, file=sys.stderr)
    sys.exit(1)
function_name = "invoke_" + sys.argv[1].replace(".", "_")
arguments = sys.argv[2:]
if function_name not in locals():
    print(__doc__, file=sys.stderr)
    sys.exit(1)
function = locals()[function_name]
function(arguments)
