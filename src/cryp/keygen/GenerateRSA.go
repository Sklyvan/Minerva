package main

import (
	"C"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
	"strconv"
	"time"
)

/*
This methods are not used anymore, the encryption/decription is done in the Python
scripts since they are faster due to the overhead of changing from Python to Go.
*/

type RSAKey struct {
	KeySize      int
	PublicKey    *rsa.PublicKey
	PrivateKey   *rsa.PrivateKey
	CreationTime int64
}

func GenerateRSAKeyPair(keySize int) RSAKey {
	privateKey, _ := rsa.GenerateKey(rand.Reader, keySize)
	publicKey := &privateKey.PublicKey
	creationTime := time.Now().Unix()
	keysPair := RSAKey{keySize, publicKey, privateKey, creationTime}
	return keysPair
}

func savePublicKeyToPEM(fName string, pubkey *rsa.PublicKey) {
	// Converts an RSA public key to PKCS#1, ASN.1 DER form.
	var pemkey = &pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: x509.MarshalPKCS1PublicKey(pubkey),
	}
	pemfile, err := os.Create(fName)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	defer func(pemfile *os.File) {
		err := pemfile.Close()
		if err != nil {
			fmt.Println("Fatal error ", err.Error())
			os.Exit(1)
		}
	}(pemfile)
	err = pem.Encode(pemfile, pemkey)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
}

func savePrivateKeyToPEM(fName string, key *rsa.PrivateKey) {
	outFile, err := os.Create(fName)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	defer func(outFile *os.File) {
		err := outFile.Close()
		if err != nil {
			fmt.Println("Fatal error ", err.Error())
			os.Exit(1)
		}
	}(outFile)
	//converts a private key to ASN.1 DER encoded form.
	var privateKey = &pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(key),
	}
	err = pem.Encode(outFile, privateKey)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
}

func exportToPEMFormat(keys RSAKey, fileName string, fileExtension string) {
	/*
		This function exports the keys.PublicKey to the fileName-Publ.pem file
		and the keys.PrivateKey to the fileName-Priv.pem file. It also exports
		the key size and the creation time to the fileName-Info.pem file.
	*/
	savePublicKeyToPEM(fileName+"-Publ."+fileExtension, keys.PublicKey)
	savePrivateKeyToPEM(fileName+"-Priv."+fileExtension, keys.PrivateKey)
	infoFile, err := os.Create(fileName + "-Info." + fileExtension)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	defer func(infoFile *os.File) {
		err := infoFile.Close()
		if err != nil {
			fmt.Println("Fatal error ", err.Error())
			os.Exit(1)
		}
	}(infoFile)
	_, err = infoFile.WriteString(strconv.FormatInt(int64(keys.KeySize), 10))
	if err != nil {
		return
	}
	_, err = infoFile.WriteString("\n")
	if err != nil {
		return
	}
	_, err = infoFile.WriteString(strconv.FormatInt(keys.CreationTime, 10))
	if err != nil {
		return
	}
}

func verifyKeys(keys RSAKey) bool { // Debugging function
	// Checks if Dec(Enc(m)) = m
	message := []byte("Hello World!")
	ciphertext, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, keys.PublicKey, message, nil)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	plaintext, err := rsa.DecryptOAEP(sha256.New(), rand.Reader, keys.PrivateKey, ciphertext, nil)
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
		os.Exit(1)
	}
	return string(plaintext) == string(message)
}

func areEqual(keys1 RSAKey, keys2 RSAKey) bool { // Debugging function
	return keys1.KeySize == keys2.KeySize &&
		keys1.CreationTime == keys2.CreationTime &&
		keys1.PublicKey.E == keys2.PublicKey.E &&
		keys1.PublicKey.N.Cmp(keys2.PublicKey.N) == 0 &&
		keys1.PrivateKey.D.Cmp(keys2.PrivateKey.D) == 0 &&
		keys1.PrivateKey.Primes[0].Cmp(keys2.PrivateKey.Primes[0]) == 0 &&
		keys1.PrivateKey.Primes[1].Cmp(keys2.PrivateKey.Primes[1]) == 0
}

func GenerateKeys(keySize int, fileName string, fileExtension string) {
	keysPair := GenerateRSAKeyPair(keySize)
	exportToPEMFormat(keysPair, fileName, fileExtension)
}
