import subprocess

from src.cryp.Imports import *

class RSAKeys:
    def __init__(self, keySize=2048, fileName='UserKeys', toImport=False):
        """
        Creates the class to store a PK and SK of RSA keys,
        the generation is done by a GoLang script.
        :param fileName: Name of the keys file.
        :param keySize: Bite size of the keys.
        :param toImport: If this is True, then we just import PEM files.
        """
        self.filename = fileName

        if not toImport:
            system(f'../cryp/RSA {keySize} {fileName}')
        self.importKeys(fileName)

    def updateKeys(self, keySize=2048):
        system(f'../cryp/RSA {keySize} {fileName}')
        self.importKeys(self.filename)

    def encrypt(self, text: bytes, withKey: RSA.RsaKey, ignoreWarning=False) -> bytes:
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
        cipherEnc = PKCS1_OAEP.new(withKey)
        return cipherEnc.encrypt(text)

    def encrypt_(self, text: bytes, withKey: RSA.RsaKey, ignoreWarning=False) -> str:
        out = subprocess.check_output(f'../cryp/RSA {self.filename} ENC {text}', shell=True)
        return out[:-1].decode()

    def decrypt_(self, cipher: str, ignoreWarning=False) -> bytes:
        out = subprocess.check_output(f'../cryp/RSA {self.filename} DEC {cipher}', shell=True)
        return out[1:-1].replace(b'\\\\', b'\\') # TODO: This solution works, but it is not the best.

    def decrypt(self, cipher: bytes, ignoreWarning=False) -> bytes:
        """
        Decrypts a cipher using the stored Private Key.
        :param cipher: Bytes to be decrypted.
        :param ignoreWarning: Inform or not the user if the cipher is not bytes.
        :return: Bytes object of the plain text.
        """
        if type(cipher) not in [bytes, bytearray]:
            if not ignoreWarning:
                print("WARNING: RSAKeys.decrypt() was passed a non-bytes object.")
            cipher = cipher.encode()
        try:
            return self.cipherDec.decrypt(cipher)
        except ValueError:
            raise WrongSecretKeyError("Wrong Secret Key. Please check if the Secret Key is correct.")
            return False

    def sign(self, text: bytes, ignoreWarning=False) -> bytes:
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
            raise WrongSecretKeyError("Wrong Secret Key. Please check if the Secret Key is correct.")
            return False

    def verify(self, text: bytes, signature: bytes, withKey: RSA.RsaKey, ignoreWarning=False) -> bool:
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
                print("WARNING: Could not verify the message,", str(errorMessage).lower()+'.')
            return False

    def exportKeys(self, fileName: str) -> bool:
        """
        Exports the keys to two files.
        :param fileName: Name of the file to be exported to.
        """
        try:
            with open(fileName+'-Publ.pem', 'wb') as file:
                file.write(self.publicKey.exportKey())
            with open(fileName+'-Priv.pem', 'wb') as file:
                file.write(self.secretKey.exportKey())
            with open(fileName+'-Info.pem', 'w') as file:
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
            with open(fileName+'-Publ.pem', 'rb') as file:
                self.publicKey = RSA.importKey(file.read())
            with open(fileName+'-Priv.pem', 'rb') as file:
                self.secretKey = RSA.importKey(file.read())
            with open(fileName+'-Info.pem', 'r') as file:
                self.keySize = int(file.readline())
                self.creationTime = float(file.readline())
            self.cipherDec = PKCS1_OAEP.new(self.secretKey)
            self.cipherSig = pkcs1_15.new(self.secretKey)
            return True
        except:
            return False

    def checkKeys(self, testSize=200) -> bool:
        m = urandom(testSize)
        test1 = (self.decrypt(self.encrypt(m, self.publicKey)) == m)
        test2 = (self.verify(m, self.sign(m), self.publicKey))
        return test1 and test2

    def __str__(self):
        return f"RSAKeys object with key size {self.keySize} and creation time {self.creationTime}."

    def __repr__(self):
        return f"RSAKeys({self.keySize})"

    def __eq__(self, other):
        return self.publicKey == other.publicKey and self.secretKey == other.secretKey

    def __hash__(self):
        return hash(self.publicKey) + hash(self.secretKey)

    def __len__(self):
        return self.keySize
