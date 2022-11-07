package main

import (
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 3 {
		os.Exit(1)
	} else if len(os.Args) == 3 {
		keySize, _ := strconv.Atoi(os.Args[1])
		fileName := os.Args[2]
		GenerateKeys(keySize, fileName)
	} else {
		os.Exit(1)
	}
}
