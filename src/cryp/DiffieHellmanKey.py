from src.cryp.Imports import *

class DiffieHellmanKey:
    def __init__(self, curve=ec.SECP384R1, hashAlgorithm=hashes.SHA256(), salting=False, info='Handshake'):
        """
        This class is used to do all the key agreement and key derivation stuff. It's important to use the exact same
        parameters for both parties, otherwise the derived key will be different and the communication will fail.
        :param curve: The curve to use for the Diffie-Hellman key exchange.
        :param curve: By default, we just support NIST curves. In a future version I will move to newer ones.
        :param hashAlgorithm: SHA256 is the default hash algorithm.
        :param salting: If this is True, we generate 32 random bytes.
        :param info: A string to be used as info in the HKDF. Transformed to bytes.
        """
        self.curve = curve
        self.hashAlgorithm = hashAlgorithm
        self.salt = None if not salting else urandom(32)
        self.info = info.encode()
        self.privateKey = ec.generate_private_key(self.curve)
        self.publicKey = self.privateKey.public_key()
        self.sharedKey = None
        self.derivedKey = None

    def generateSharedKey(self, otherPublicKey: ec.EllipticCurvePublicKey):
        self.sharedKey = self.privateKey.exchange(ec.ECDH(), otherPublicKey)
        self.computeDerivedKey()
        return self.sharedKey

    def computeDerivedKey(self, length: int=None):
        if self.sharedKey is None:
            raise Exception("Shared key not generated yet.")
        else:
            if length is None:
                length = 255 * (self.hashAlgorithm.digest_size // 8)
            self.derivedKey = HKDF(
                algorithm=self.hashAlgorithm,
                length=length,
                salt=self.salt,
                info=self.info).derive(self.sharedKey)
            return self.derivedKey

    def exportDerivedKey(self, path: str):
        with open(path, 'wb') as f:
            f.write(self.derivedKey)

    def __eq__(self, other: "DiffieHellmanKey"):
        return self.derivedKey == other.derivedKey

    def __str__(self):
        return f"DiffieHellmanKey object with derived key {self.derivedKey}"

    def __repr__(self):
        return f"DiffieHellmanKey object with derived key {self.derivedKey}"

    def __hash__(self):
        return hash(self.derivedKey)

def importDerivedKey(path: str):
    with open(path, 'rb') as f:
        return f.read()
