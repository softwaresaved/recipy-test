"""
Usage: 

    python run_lxml.etree.py parse data/data.xml
    python run_lxml.etree.py iterparse data/data.xml
"""
from __future__ import print_function
from lxml import etree
import sys


def invoke_parse(arguments):
    file_name = arguments[0]
    print("Parsing: ", file_name)
    with open(file_name, "r") as f:
        tree = etree.parse(f)
        print("Tree: ", etree.tostring(tree))
        print("Tag: ", tree.getroot().tag)


def invoke_iterparse(arguments):
    file_name = arguments[0]
    print("Iteratively parsing: ", file_name)
    with open(file_name, "r") as f:
        for event, element in etree.iterparse(file_name,
                                              events=("start", "end")):
            print("%5s, %4s, %s" % (event, element.tag, element.text))


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
