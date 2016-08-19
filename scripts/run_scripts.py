from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os.path
import subprocess

def run(python, script, package_function, files):
  command_line = [python]
  command_line.append(script)
  command_line.append(package_function)
  command_line = command_line + files
  print((" ".join(command_line)))
  return_code = subprocess.call(command_line)
  if return_code != 0:
    print("Oops: " + " ".join(command_line) + \
          "returned " + str(return_code))

OUTPUT = 'OUTPUT'
os.mkdir("tmp/")
with open('config.json') as config_file:
    config = json.load(config_file)
    for package in config:
      script = "run_" + package + ".py"
      package_dir = os.path.join("tmp", package)
      os.mkdir(package_dir)
      package_functions = config[package]
      for package_function in package_functions:
        files = package_functions[package_function]
        files = [f.replace(OUTPUT, package_dir) for f in files]
        run("python", script, package_function, files), 
        print("")

