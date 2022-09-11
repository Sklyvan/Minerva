from src.cryp.Imports import RSA
from src.main.Circuit import Circuit

class PublicUser:
    def __init__(self, userID: int, userName: str, rsaPublicKeys: [RSA.RsaKey, RSA.RsaKey], throughCircuit: Circuit):
        self.userID = userID
        self.userName = userName
        self.encryptionKey, self.verificationKey = rsaPublicKeys
        self.throughCircuit = throughCircuit

    def __str__(self):
        return f"User {self.userName} (ID: {self.userID})"

    def __repr__(self):
        return f"PublicUser object with user name {self.userName} and ID {self.userID}."

    def __eq__(self, other: PublicUser):
        return self.userID == other.userID
