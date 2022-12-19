from src.cryp.Imports import RSA, PKCS1_OAEP, pkcs1_15, SHA256
from src.netw.Circuit import Circuit

class PublicUser:
    def __init__(self, userID: int, userName: str,
                 rsaPublicKeys: [RSA.RsaKey, RSA.RsaKey], throughCircuit: Circuit):
        self.userID = userID
        self.userName = userName
        self.encryptionKey, self.verificationKey = rsaPublicKeys
        self.cipherEnc = PKCS1_OAEP.new(self.encryptionKey, hashAlgo=SHA256)
        self.cipherVer = pkcs1_15.new(self.verificationKey)
        self.throughCircuit = throughCircuit

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

    def splitMessage(self, message: bytes, keySize: int) -> [bytes]:
        """
        Splits a message into chunks that can be encrypted with the given key.
        :param message: Bytes to be split.
        :param keySize: Size of the key in bits.
        :return: List of bytes objects of the chunks.
        """
        keyBytes = int(keySize / 8)
        chunkSize = keyBytes - 2 - 2 * SHA256.digest_size
        return [message[i:i+chunkSize] for i in range(0, len(message), chunkSize)]

    def encrypt(self, content: bytes) -> bytes:
        if not self.canEncrypt(len(content), self.encryptionKey.size_in_bits()):
            messageParts = self.splitMessage(content, self.encryptionKey.size_in_bits())
            cipher = b""
            for part in messageParts:
                cipher += self.encrypt(part)
            return cipher
        return self.cipherEnc.encrypt(content)

    def verify(self, content: bytes, signature: bytes) -> bool:
        return self.cipherVer.verify(content, signature)

    def asJSON(self) -> dict:
        return {
            "UserID": self.userID,
            "UserName": self.userName,
            "EncryptionKey": self.encryptionKey.export_key().decode("utf-8"),
            "VerificationKey": self.verificationKey.export_key().decode("utf-8"),
            "ThroughCircuit": self.throughCircuit.asJSON()
        }

    def readUser(self, data: dict):
        self.userID = data["UserID"]
        self.userName = data["UserName"]
        self.encryptionKey = RSA.import_key(data["EncryptionKey"])
        self.verificationKey = RSA.import_key(data["VerificationKey"])

        self.throughCircuit = Circuit('')
        self.throughCircuit.readCircuit(data["ThroughCircuit"])

    def __str__(self) -> str:
        return f"User {self.userName} (ID: {self.userID})"

    def __repr__(self) -> str:
        return f"PublicUser object with user name {self.userName} and ID {self.userID}."

    def __eq__(self, other: "PublicUser") -> bool:
        idCheck = self.userID == other.userID
        nameCheck = self.userName == other.userName
        encryptionKeyCheck = self.encryptionKey == other.encryptionKey
        circuitCheck = self.throughCircuit == other.throughCircuit
        return idCheck and nameCheck and encryptionKeyCheck and circuitCheck

class Contacts:
    def __init__(self, contacts = {}):
        self.contacts = contacts # contacts[userName] = PublicUser

    def addContact(self, contact: PublicUser):
        self.contacts[contact.userName] = contact

    def removeContact(self, contact: PublicUser):
        del self.contacts[contact.userName]

    def asJSON(self) -> list:
        return [contact.asJSON() for contact in self.contacts.values()]

    def readContacts(self, json: list):
        for contact in json:
            user = PublicUser(None, None, [None, None], None)
            user.readUser(contact)
            self.addContact(user)

    def __getitem__(self, userName: str) -> PublicUser:
        return self.contacts[userName]

    def __str__(self) -> str:
        return f"Contacts: {self.contacts}"

    def __repr__(self) -> str:
        return f"Contacts object with {len(self.contacts)} contacts."

    def __eq__(self, other: "Contacts") -> bool:
        for contact in self.contacts.values():
            if contact not in other.contacts.values():
                return False
        return True

    def __len__(self) -> int:
        return len(self.contacts)