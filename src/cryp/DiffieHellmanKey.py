from src.cryp.Imports import *


class DiffieHellmanKey:
    def __init__(
        self,
        curve: "EllipticCurve" = DFH_CURVE,
        hashAlgorithm: "HashAlgorithm" = DFH_HASH,
        salting: bool = False,
        info: str = "Handshake",
    ):
        """
        This class is used to do all the key agreement and key derivation stuff. It's important to use the exact same
        parameters for both parties, otherwise the derived key will be different and the communication will fail.
        :param curve: The curve to use for the Diffie-Hellman key exchange.
        :param curve: By default, we just support NIST curves. In a future version I will move to newer ones.
        The default curve is SECP384R1 (NIST P-384). https://neuromancer.sk/std/secg/secp384r1
        :param hashAlgorithm: SHA256 is the default hash algorithm.
        :param salting: If this is True, we generate 32 random bytes.
        :param info: A string to be used as info in the HKDF. It is transformed to bytes.
        """
        self.curve = curve
        self.hashAlgorithm = hashAlgorithm
        self.salt = None if not salting else urandom(DFH_SALT_SIZE)
        self.info = info.encode()
        self.privateKey = ec.generate_private_key(self.curve)
        self.publicKey = self.privateKey.public_key()
        self.sharedKey = None
        self.derivedKey = None

    def generateSharedKey(self, otherPublicKey: ec.EllipticCurvePublicKey) -> bytes:
        self.sharedKey = self.privateKey.exchange(ec.ECDH(), otherPublicKey)
        self.computeDerivedKey()
        return self.sharedKey

    def computeDerivedKey(self, length: int = None) -> bytes:
        if self.sharedKey is None:
            raise Exception("Shared key not generated yet.")
        else:
            if length is None:
                length = 255 * (self.hashAlgorithm.digest_size // 8)
            self.derivedKey = HKDF(
                algorithm=self.hashAlgorithm,
                length=length,
                salt=self.salt,
                info=self.info,
            ).derive(self.sharedKey)
            return self.derivedKey

    def exportDerivedKey(self, path: str):
        with open(path, "wb") as f:
            f.write(self.derivedKey)

    def __eq__(self, other: "DiffieHellmanKey") -> bool:
        return self.derivedKey == other.derivedKey

    def __str__(self) -> str:
        return f"DiffieHellmanKey object with derived key {self.derivedKey}"

    def __repr__(
        self,
    ) -> bytes:  # This function is used to store the object in a JSON file.
        return b64encode(self.derivedKey).decode()

    def __hash__(self) -> int:
        return hash(self.derivedKey)


def importDerivedKey(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
