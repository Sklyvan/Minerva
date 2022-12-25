#!/bin/sh

# Remove all the files ending in .pem or .db from the current directory and all subdirectories
find . -name "*.pem" -exec rm -f {} \;
find . -name "*.db" -exec rm -f {} \;

# Remove also all the files matching User_*.json
find . -name "User_*.json" -exec rm -f {} \;