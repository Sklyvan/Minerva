package main

import (
	"encoding/base64"
	"fmt"
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
		keyFileName := os.Args[1]
		operation := os.Args[2]
		message := os.Args[3]
		for i := 4; i < len(os.Args); i++ {
			// Read all the next arguments as a single string
			message += " " + os.Args[i]
		}

		// KEY := importFromPEMFormat(keyFileName)

		if operation == "ENC" {
			KEY := importPublicKey(keyFileName + "-Publ.pem")
			ciphertext := encrypt(message, KEY)
			// The ciphertext is a byte array, so we need to convert it to a base64 string
			out := base64.StdEncoding.EncodeToString(ciphertext)
			fmt.Println(out)
		} else if operation == "DEC" {
			KEY := importPrivateKey(keyFileName + "-Priv.pem")
			// The ciphertext is a base64 string, so we need to convert it to a byte array
			ciphertext, _ := base64.StdEncoding.DecodeString(message)
			out := decrypt([]byte(ciphertext), KEY)
			fmt.Println(out)
		} else if operation == "SIG" {
			KEY := importPrivateKey(keyFileName + "-Priv.pem")
			signature := sign(message, KEY)
			// The signature is a byte array, so we need to convert it to a base64 string
			out := base64.StdEncoding.EncodeToString(signature)
			fmt.Println(out)
		} else if operation == "VER" {
			KEY := importPublicKey(keyFileName + "-Publ.pem")
			// The signature is a base64 string, so we need to convert it to a byte array
			signature, _ := base64.StdEncoding.DecodeString(message)
			out := verify(message, []byte(signature), KEY)
			fmt.Println(out)
		} else {
			fmt.Println("Invalid Operation:", operation)
			os.Exit(2)
		}

	}

}
