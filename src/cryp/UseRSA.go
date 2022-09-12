package main

import (
	"bufio"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
	"strconv"
)

func importPublicKey(fileName string) *rsa.PublicKey {
	publicKeyFile, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	pemFileInfo, _ := publicKeyFile.Stat()
	var size int64 = pemFileInfo.Size()
	pemBytes := make([]byte, size)

	buffer := bufio.NewReader(publicKeyFile)
	_, err = buffer.Read(pemBytes)

	data, _ := pem.Decode([]byte(pemBytes))
	publicKeyFile.Close()

	pub, err := x509.ParsePKCS1PublicKey(data.Bytes)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	return pub
}

func importPrivateKey(fileName string) *rsa.PrivateKey {
	privateKeyFile, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	pemFileInfo, _ := privateKeyFile.Stat()
	var size int64 = pemFileInfo.Size()
	pemBytes := make([]byte, size)

	buffer := bufio.NewReader(privateKeyFile)
	_, err = buffer.Read(pemBytes)

	data, _ := pem.Decode([]byte(pemBytes))
	privateKeyFile.Close()

	priv, err := x509.ParsePKCS1PrivateKey(data.Bytes)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	return priv
}

func importKeyInfo(fileName string) (int, int64) {
	infoFile, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	scanner := bufio.NewScanner(infoFile)
	scanner.Scan()
	keySize, err := strconv.Atoi(scanner.Text())

	scanner.Scan()
	creationTime, err := strconv.ParseInt(scanner.Text(), 10, 64)

	return keySize, creationTime
}

func importFromPEMFormat(fileName string) RSAKey {
	importedKey := RSAKey{}

	importedKey.PrivateKey = importPrivateKey(fileName + "-Priv.pem")
	importedKey.PublicKey = importPublicKey(fileName + "-Publ.pem")
	importedKey.KeySize, importedKey.CreationTime = importKeyInfo(fileName + "-Info.pem")

	return importedKey
}

func encrypt(message string, key *rsa.PublicKey) []byte {
	ciphertext, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, key, []byte(message), nil)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	return ciphertext
}

func decrypt(ciphertext []byte, key *rsa.PrivateKey) string {
	plaintext, err := rsa.DecryptOAEP(sha256.New(), rand.Reader, key, ciphertext, nil)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	return string(plaintext)
}

func sign(message string, key *rsa.PrivateKey) []byte {
	signature, err := rsa.SignPKCS1v15(nil, key, 0, []byte(message))
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	return signature
}

func verify(message string, signature []byte, key *rsa.PublicKey) bool {
	err := rsa.VerifyPKCS1v15(key, 0, []byte(message), signature)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		return false
	}
	return true
}
