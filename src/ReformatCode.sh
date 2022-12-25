#!/bin/sh

# For all the files inside the current directory and all subdirectories that end in .py: run "black File.py"
find . -name "*.py" -exec black {} \;
