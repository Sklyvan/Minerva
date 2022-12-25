from src.cryp.Imports import *


class RSAKeys:
    def __init__(
        self, keySize: int = 2048, fileName: str = "UserKeys", toImport: bool = False
    ):
        """
        Creates the class to store a PK and SK of RSA keys,
        the generation is done by a GoLang script.
        :param fileName: Name of the keys file.
        :param keySize: Bite size of the keys.
        :param toImport: If this is True, then we just import PEM files.
        """
        self.filename = fileName
        self.secretKey = None
        self.publicKey = None
        self.keySize = None
        self.creationTime = None
        self.cipherDec = None
        self.cipherSig = None
        if not toImport:  # Create the RSA keys
            system(f"../cryp/RSA {keySize} {fileName}")
        self.importKeys(fileName)

    def updateKeys(self, keySize: int = 2048):
        system(f"../cryp/RSA {keySize} {fileName}")
        self.importKeys(self.filename)

    def canEncrypt(self, inputSize: int, keySize: int) -> bool:
        """
        Checks if the input can be encrypted with the key.
        :param inputSize: Size of the input in bytes.
        :param keySize: Size of the key in bits.
        :return: Boolean value of the verification.
        """
        keyBytes = int(keySize / 8)
        if inputSize > keyBytes - 2 - 2 * SHA256.digest_size:
            return False
        return True

    def canDecrypt(self, inputSize: int, keySize: int) -> bool:
        """
        Checks if the input can be decrypted with the key.
        :param inputSize: Size of the input in bytes.
        :param keySize: Size of the key in bits.
        :return: Boolean value of the verification.
        """
        keyBytes = int(keySize / 8)
        if inputSize > keyBytes:
            return False
        return True

    def splitMessage(self, message: bytes, keySize: int) -> [bytes]:
        """
        Splits a message into chunks that can be encrypted with the given key.
        :param message: Bytes to be split.
        :param keySize: Size of the key in bits.
        :return: List of bytes objects of the chunks.
        """
        keyBytes = int(keySize / 8)
        chunkSize = keyBytes - 2 - 2 * SHA256.digest_size
        return [message[i : i + chunkSize] for i in range(0, len(message), chunkSize)]

    def splitCipher(self, cipher: bytes, keySize: int) -> [bytes]:
        """
        Splits a cipher into chunks that can be decrypted with the given key.
        :param cipher: Bytes to be split.
        :param keySize: Size of the key in bits.
        :return: List of bytes objects of the chunks.
        """
        keyBytes = int(keySize / 8)
        chunkSize = keyBytes
        return [cipher[i : i + chunkSize] for i in range(0, len(cipher), chunkSize)]

    def encrypt(
        self, text: bytes, withKey: RSA.RsaKey, ignoreWarning: bool = False
    ) -> bytes:
        """
        Encrypts a text using the given Public Key.
        :param text: Bytes to be encrypted.
        :param withKey: Public Key to be used to encrypt the text.
        :param ignoreWarning: Inform or not the user if the text is not bytes.
        :return: Bytes object of the cipher text.
        """
        if type(text) not in [bytes, bytearray]:
            if not ignoreWarning:
                print("WARNING: RSAKeys.encrypt() was passed a non-bytes object.")
            text = text.encode()
        if not self.canEncrypt(len(text), withKey.size_in_bits()):
            messageParts = self.splitMessage(text, withKey.size_in_bits())
            cipher = b""
            for part in messageParts:
                cipher += self.encrypt(part, withKey)
            return cipher
        cipherEnc = PKCS1_OAEP.new(withKey, hashAlgo=SHA256)
        return cipherEnc.encrypt(text)

    def decrypt(self, cipher: bytes, ignoreWarning: bool = False) -> bytes:
        """
        Decrypts a cipher using the stored Private Key.
        :param cipher: Bytes/Array of bytes to be decrypted.
        :param ignoreWarning: Inform or not the user if the cipher is not bytes.
        :return: Bytes object of the plain text.
        """
        if type(cipher) not in [bytes, bytearray]:
            if not ignoreWarning:
                print("WARNING: RSAKeys.decrypt() was passed a non-bytes object.")
            cipher = cipher.encode()
        if not self.canDecrypt(len(cipher), self.keySize):
            cipherParts = self.splitCipher(cipher, self.keySize)
            plain = b""
            for part in cipherParts:
                plain += self.decrypt(part)
            return plain
        try:
            return self.cipherDec.decrypt(cipher)
        except ValueError:
            raise WrongSecretKeyError(
                "Wrong Secret Key. Please check if the Secret Key is correct."
            )
            return False

    def decrypt_(self, cipher: bytes, ignoreWarning: bool = False) -> bytes:
        """
        Decrypts a cipher using the stored Private Key.
        :param cipher: Bytes/Array of bytes to be decrypted.
        :param ignoreWarning: Inform or not the user if the cipher is not bytes.
        :return: Bytes object of the plain text.
        """
        if type(cipher[0]) not in [bytes, bytearray]:
            if not ignoreWarning:
                print("WARNING: RSAKeys.decrypt() was passed a non-bytes object.")
            cipher = cipher.encode()
        try:
            return self.cipherDec.decrypt(cipher)
        except ValueError:
            raise WrongSecretKeyError(
                "Wrong Secret Key. Please check if the Secret Key is correct."
            )
            return False

    def sign(self, text: bytes, ignoreWarning: bool = False) -> bytes:
        """
        Signs a text using the stored Private Key.
        :param text: Bytes to be signed.
        :param ignoreWarning: Inform or not the user if the text is not bytes.
        :return: Bytes object of the signature.
        """
        if type(text) not in [bytes, bytearray]:
            if not ignoreWarning:
                print("WARNING: RSAKeys.sign() was passed a non-bytes object.")
            text = text.encode()
        hashedText = SHA256.new(text)
        # Raise error if the hash is not valid.
        try:
            return self.cipherSig.sign(hashedText)
        except ValueError:
            raise WrongSecretKeyError(
                "Wrong Secret Key. Please check if the Secret Key is correct."
            )
            return False

    def verify(
        self,
        text: bytes,
        signature: bytes,
        withKey: RSA.RsaKey,
        ignoreWarning: bool = False,
    ) -> bool:
        """
        Verifies a signature using the given Public Key.
        :param text: Bytes to be verified.
        :param signature: Signature to be verified.
        :param withKey: Public Key to be used to verify the signature.
        :param ignoreWarning: Inform or not the user if the text is not bytes.
        :return: Boolean value of the verification.
        """
        if type(text) not in [bytes, bytearray]:
            if not ignoreWarning:
                print("WARNING: RSAKeys.verify() was passed a non-bytes object.")
            text = text.encode()
        hashedText = SHA256.new(text)
        cipherVer = pkcs1_15.new(withKey)
        try:
            cipherVer.verify(hashedText, signature)
            return True
        except (ValueError, TypeError) as errorMessage:
            if not ignoreWarning:
                print(
                    "WARNING: Could not verify the message,",
                    str(errorMessage).lower() + ".",
                )
            return False

    def exportKeys(self, fileName: str) -> bool:
        """
        Exports the keys to two files.
        :param fileName: Name of the file to be exported to.
        """
        try:
            with open(fileName + "-Publ.pem", "wb") as file:
                file.write(self.publicKey.exportKey())
            with open(fileName + "-Priv.pem", "wb") as file:
                file.write(self.secretKey.exportKey())
            with open(fileName + "-Info.pem", "w") as file:
                file.write(f"{self.keySize}\n{self.creationTime}")
            return True
        except:
            return False

    def importKeys(self, fileName: str) -> bool:
        """
        Imports the keys from a file.
        :param fileName: Name of the file to be imported from.
        """
        try:
            with open(fileName + "-Publ.pem", "rb") as file:
                self.publicKey = RSA.importKey(file.read())
            with open(fileName + "-Priv.pem", "rb") as file:
                self.secretKey = RSA.importKey(file.read())
            with open(fileName + "-Info.pem", "r") as file:
                self.keySize = int(file.readline())
                self.creationTime = float(file.readline())
            self.cipherDec = PKCS1_OAEP.new(self.secretKey, hashAlgo=SHA256)
            self.cipherSig = pkcs1_15.new(self.secretKey)
            return True
        except:
            return False

    def checkKeys(self, testSize: int = 200) -> bool:
        m = urandom(testSize)  # Random bytes
        test1 = self.decrypt(self.encrypt(m, self.publicKey)) == m
        test2 = self.verify(m, self.sign(m), self.publicKey)
        return test1 and test2

    def __str__(self) -> str:
        return f"RSAKeys object with key size {self.keySize} and creation time {self.creationTime}."

    def __repr__(self) -> str:
        return f"RSAKeys({self.keySize})"

    def __eq__(self, other: "RSAKeys") -> bool:
        return self.publicKey == other.publicKey and self.secretKey == other.secretKey

    def __hash__(self) -> int:
        return hash(self.publicKey) + hash(self.secretKey)

    def __len__(self) -> int:
        return self.keySize
