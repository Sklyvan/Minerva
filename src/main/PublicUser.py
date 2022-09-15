from src.cryp.Imports import RSA
from src.main.Circuit import Circuit

class PublicUser:
    def __init__(self, userID: int, userName: str, rsaPublicKeys: [RSA.RsaKey, RSA.RsaKey], throughCircuit: Circuit):
        self.userID = userID
        self.userName = userName
        self.encryptionKey, self.verificationKey = rsaPublicKeys
        self.throughCircuit = throughCircuit

    def asJSON(self):
        return {
            "UserID": self.userID,
            "UserName": self.userName,
            "EncryptionKey": self.encryptionKey.export_key().decode("utf-8"),
            "VerificationKey": self.verificationKey.export_key().decode("utf-8"),
            "ThroughCircuit": self.throughCircuit.asJSON()
        }

    def __str__(self):
        return f"User {self.userName} (ID: {self.userID})"

    def __repr__(self):
        return f"PublicUser object with user name {self.userName} and ID {self.userID}."

    def __eq__(self, other: "PublicUser"):
        idCheck = self.userID == other.userID
        nameCheck = self.userName == other.userName
        encryptionKeyCheck = self.encryptionKey == other.encryptionKey
        circuitCheck = self.throughCircuit == other.throughCircuit
        return idCheck and nameCheck and encryptionKeyCheck and circuitCheck
