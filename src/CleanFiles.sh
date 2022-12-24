#!/bin/sh

# Remove all the files ending in .pem or .db from the current directory and all subdirectories

find . -name "*.pem" -exec rm -f {} \;
find . -name "*.db" -exec rm -f {} \;