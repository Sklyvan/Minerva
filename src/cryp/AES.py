from src.cryp.Imports import *


class KeyAES:
    def __init__(self, key: bytes, nonce: bytes):
        """
        This class is used to encrypt/decrypt data using AES. The key usually
        comes from a DiffieHellmanKey object. Since the original key is so long
        we just use the first 32 bytes of it.
        The nonce should be in the range of [0, 15], it is recommended to use
        8 bytes. This value can be shared publicly since it is not a secret.
        :param key: Bytes object that are going to be used as key.
        :param nonce: Random bytes that are going to be used as nonce.
        """
        self.key, self.nonce = key[:AES_KEY_SIZE], nonce[:AES_NONCE_SIZE]
        self.cipher = AES.new(self.key, AES.MODE_CTR, nonce=self.nonce)

    def encrypt(self, data: bytes) -> bytes:
        return self.cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.cipher.decrypt(data)

    def __eq__(self, other: "KeyAES") -> bool:
        return self.key == other.key and self.nonce == other.nonce

    def __len__(self):
        return len(self.key) + len(self.nonce)


def encryptAES(data: str, key: bytes, nonce: bytes) -> bytes:
    """
    Encrypts a string using AES.
    :param data: String to be encrypted.
    :param key: Bytes object that are going to be used as key.
    :param nonce: Random bytes that are going to be used as nonce.
    :return: Encrypted string.
    """
    objectAES = KeyAES(key, nonce)
    encryptedData = objectAES.encrypt(data.encode())
    return encryptedData


def decryptAES(data: bytes, key: bytes, nonce: bytes) -> str:
    """
    Decrypts a string using AES.
    :param data: String to be decrypted.
    :param key: Bytes object that are going to be used as key.
    :param nonce: Random bytes that are going to be used as nonce.
    :return: Decrypted string.
    """
    objectAES = KeyAES(key, nonce)
    decryptedData = objectAES.decrypt(data)
    return decryptedData.decode()
