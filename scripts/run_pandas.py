"""
Usage:

    python run_pandas.py read_csv dataframe.csv
    python run_pandas.py read_table dataframe.csv
    python run_pandas.py read_excel dataframe.xls
    python run_pandas.py read_hdf dataframe.hdf
    python run_pandas.py read_pickle dataframe.pickle
    python run_pandas.py read_stata dataframe.dta
    python run_pandas.py read_msgpack dataframe.mpack

    python run_pandas.py Panel.to_excel panel.xls
    python run_pandas.py Panel.to_hdf panel.hdf
    python run_pandas.py Panel.to_msgpack panel.mpack
    python run_pandas.py Panel.to_pickle panel.pickle

    python run_pandas.py DataFrame.to_csv dataframe.csv
    python run_pandas.py DataFrame.to_excel dataframe.xls
    python run_pandas.py DataFrame.to_hdf dataframe.hdf
    python run_pandas.py DataFrame.to_msgpack dataframe.mpack
    python run_pandas.py DataFrame.to_stata dataframe.dta
    python run_pandas.py DataFrame.to_pickle dataframe.pickle

    python run_pandas.py Series.to_csv series.csv
    python run_pandas.py Series.to_hdf series.hdf
    python run_pandas.py Series.to_msgpack series.mpack
    python run_pandas.py Series.to_pickle series.pickle
"""
from __future__ import print_function
import pandas as pd
from pandas import DataFrame
from pandas import Panel
from pandas import Series
import string
import sys


def invoke_read_csv(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_csv(file_name)
    print("Data:")
    print(data)


def invoke_read_table(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_table(file_name)
    print("Data:")
    print(data)


def invoke_read_excel(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_excel(file_name)
    print("Data:")
    print(data)


def invoke_read_hdf(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_hdf(file_name)
    print("Data:")
    print(data)


def invoke_read_pickle(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_pickle(file_name)
    print("Data:")
    print(data)


def invoke_read_stata(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_stata(file_name)
    print("Data:")
    print(data)


def invoke_read_msgpack(arguments):
    file_name = arguments[0]
    print("Loading data:", file_name)
    data = pd.read_msgpack(file_name)
    print("Data:")
    print(data)


def get_data(i, j, offset = 0):
    return {string.ascii_lowercase[y]:(y + offset) for y in range(i,j)}


def get_series(i, j, offset = 0):
    series = pd.Series(get_data(i, j, offset))
    print("Series:")
    print(series)
    return series


def get_dataframe():
    data = {'seriesOne': pd.Series(get_data(0, 5)),
            'seriesTwo': pd.Series(get_data(0, 5, 10))}
    frame = pd.DataFrame(data)
    print("DataFrame:")
    print(frame)
    return frame


def get_panel():
    data1 = {'seriesOne': pd.Series(get_data(0, 5)),
            'seriesTwo': pd.Series(get_data(0, 5, 10))}
    frame1 = pd.DataFrame(data1)
    data2 = {'seriesThree': pd.Series(get_data(6, 10)),
            'seriesFour': pd.Series(get_data(6, 10, 10))}
    frame2 = pd.DataFrame(data2)
    data = {'frameOne': frame1, 'frameTwo': frame2}
    panel = pd.Panel(data)
    print("Panel:")
    print(panel)
    return panel


def invoke_Panel_to_excel(arguments):
    file_name = arguments[0]
    panel = get_panel()
    print("Saving data:", file_name)
    panel.to_excel(file_name)


def invoke_Panel_to_hdf(arguments):
    file_name = arguments[0]
    panel = get_panel()
    print("Saving data:", file_name)
    panel.to_hdf(file_name, key="Sample", mode="w")


def invoke_Panel_to_msgpack(arguments):
    file_name = arguments[0]
    panel = get_panel()
    print("Saving data:", file_name)
    panel.to_msgpack(file_name)


def invoke_Panel_to_pickle(arguments):
    file_name = arguments[0]
    panel = get_panel()
    print("Saving data:", file_name)
    panel.to_pickle(file_name)


def invoke_DataFrame_to_csv(arguments):
    file_name = arguments[0]
    frame = get_dataframe()
    print("Saving data:", file_name)
    frame.to_csv(file_name)


def invoke_DataFrame_to_excel(arguments):
    file_name = arguments[0]
    frame = get_dataframe()
    print("Saving data:", file_name)
    frame.to_excel(file_name, sheet_name="SampleSheet")


def invoke_DataFrame_to_hdf(arguments):
    file_name = arguments[0]
    frame = get_dataframe()
    print("Saving data:", file_name)
    frame.to_hdf(file_name, key="Sample", mode="w")


def invoke_DataFrame_to_msgpack(arguments):
    file_name = arguments[0]
    frame = get_dataframe()
    print("Saving data:", file_name)
    frame.to_msgpack(file_name)


def invoke_DataFrame_to_stata(arguments):
    file_name = arguments[0]
    frame = get_dataframe()
    print("Saving data:", file_name)
    frame.to_stata(file_name)


def invoke_DataFrame_to_pickle(arguments):
    file_name = arguments[0]
    frame = get_dataframe()
    print("Saving data:", file_name)
    frame.to_pickle(file_name)


def invoke_Series_to_csv(arguments):
    file_name = arguments[0]
    series = get_series(0, 4)
    print("Saving data:", file_name)
    series.to_csv(file_name)


def invoke_Series_to_hdf(arguments):
    file_name = arguments[0]
    series = get_series(0, 4)
    series.to_hdf(file_name, key="Sample", mode="w")
    print("Saving data:", file_name)


def invoke_Series_to_msgpack(arguments):
    file_name = arguments[0]
    series = get_series(0, 4)
    series.to_msgpack(file_name)
    print("Saving data:", file_name)


def invoke_Series_to_pickle(arguments):
    file_name = arguments[0]
    series = get_series(0, 4)
    series.to_pickle(file_name)
    print("Saving data:", file_name)


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
