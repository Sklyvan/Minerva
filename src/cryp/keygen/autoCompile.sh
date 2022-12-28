#!/bin/sh

compilationName=${PWD##*/} # Current directory name
compilationName=${compilationName:-/} # Remove trailing slash

go build .
# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    echo "RSA script compiled successfully."
    mv $compilationName RSA.bin # Change the file name to RSA
    cp RSA.bin ../../testing/RSA.bin # Copy the file to the testing directory
    mv RSA.bin .. # Move out the file from the GoLang directory
else
    echo "RSA script failed to compile."
fi
