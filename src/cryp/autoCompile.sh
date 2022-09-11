#!/bin/sh

compilationName=${PWD##*/} # Current directory name
compilationName=${compilationName:-/} # Remove trailing slash

go build .
# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    echo "RSA script compiled successfully."
    mv $compilationName RSA
    cp RSA ../testing/RSA
else
    echo "RSA script failed to compile."
fi
