#!/bin/sh

# Compile the RSA GoLang script and copy it to the test directory.
go build GenerateRSA.go
cp GenerateRSA ../testing/GenerateRSA