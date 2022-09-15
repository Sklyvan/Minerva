import Crypto.PublicKey.RSA

from src.cryp.Imports import RSA
from src.main.Circuit import Circuit

class PublicUser:
    def __init__(self, userID: int, userName: str,
                 rsaPublicKeys: [Crypto.PublicKey.RSA.RsaKey, Crypto.PublicKey.RSA.RsaKey], throughCircuit: Circuit):
        self.userID = userID
        self.userName = userName
        self.encryptionKey, self.verificationKey = rsaPublicKeys
        if type(throughCircuit) is Circuit: # Sometimes can be instantiated with a None, so we check for that.
            self.throughCircuitID = throughCircuit.circuitID
        else:
            self.throughCircuitID = None

    def asJSON(self):
        return {
            "UserID": self.userID,
            "UserName": self.userName,
            "EncryptionKey": self.encryptionKey.export_key().decode("utf-8"),
            "VerificationKey": self.verificationKey.export_key().decode("utf-8"),
            "ThroughCircuit": self.throughCircuitID
        }

    def readUser(self, data: str):
        self.userID = data["UserID"]
        self.userName = data["UserName"]
        self.encryptionKey = RSA.import_key(data["EncryptionKey"])
        self.verificationKey = RSA.import_key(data["VerificationKey"])
        self.throughCircuitID = data["ThroughCircuit"]

    def __str__(self):
        return f"User {self.userName} (ID: {self.userID})"

    def __repr__(self):
        return f"PublicUser object with user name {self.userName} and ID {self.userID}."

    def __eq__(self, other: "PublicUser"):
        idCheck = self.userID == other.userID
        nameCheck = self.userName == other.userName
        encryptionKeyCheck = self.encryptionKey == other.encryptionKey
        circuitCheck = self.throughCircuitID == other.throughCircuitID
        return idCheck and nameCheck and encryptionKeyCheck and circuitCheck

class Contacts:
    def __init__(self, contacts = {}):
        self.contacts = contacts # contacts[userName] = PublicUser

    def addContact(self, contact: PublicUser):
        self.contacts[contact.userName] = contact

    def removeContact(self, contact: PublicUser):
        del self.contacts[contact.userName]

    def asJSON(self):
        return [contact.asJSON() for contact in self.contacts.values()]

    def readContacts(self, json: list):
        for contact in json:
            user = PublicUser(None, None, [None, None], None)
            user.readUser(contact)
            self.addContact(user)

    def __str__(self):
        return f"Contacts: {self.contacts}"

    def __repr__(self):
        return f"Contacts object with {len(self.contacts)} contacts."

    def __eq__(self, other: "Contacts"):
        for contact in self.contacts.values():
            if contact not in other.contacts.values():
                return False
        return True

    def __len__(self):
        return len(self.contacts)