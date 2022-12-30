package main

import (
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 4 {
		os.Exit(1)
	} else if len(os.Args) == 4 {
		keySize, _ := strconv.Atoi(os.Args[1])
		fileName := os.Args[2]
		fileExtension := os.Args[3]
		GenerateKeys(keySize, fileName, fileExtension)
	} else {
		os.Exit(1)
	}
}
