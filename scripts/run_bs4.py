"""
Usage:

    python -m recipy run_bs4.py BeautifulSoup data/index.html
"""
from __future__ import print_function
from bs4 import BeautifulSoup
import sys


def invoke_BeautifulSoup(arguments):
    file_name = arguments[0]
    print("Parsing: ", file_name)
    with open(file_name, "r") as f:
        soup = BeautifulSoup(f, "lxml")
        print("Pretty-printed data:")
        print(soup.prettify())


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
