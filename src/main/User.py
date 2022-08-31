from src.main.Imports import *

class User:
    def __init__(self, userID: int, userName: str, rsaKeys: [RSAKeys, RSAKeys], IP: str,
                 forwardingTable: ForwardingTable = None, messagesQueue: Queue = None, userFriends: dict = None, messages: MessagesDB = None):
        self.userID = userID
        self.userName = userName
        self.encryptionKeys, self.signingKeys = rsaKeys
        self.IP = IP
        self.forwardingTable = forwardingTable
        self.messagesQueue = messagesQueue
        self.userFriends = userFriends
        self.messages = messages

    def regenerateKeys(self):
        self.encryptionKeys.regenerateKeys()
        self.signingKeys.regenerateKeys()

    def exportKeys(self, encryptionPath: str, signingPath: str):
        self.encryptionKeys.exportKeys(encryptionPath)
        self.signingKeys.exportKeys(signingPath)

    def importKeys(self, encryptionPath: str, signingPath: str):
        self.encryptionKeys.importKeys(encryptionPath)
        self.signingKeys.importKeys(signingPath)

    def checkKeys(self):
        return self.encryptionKeys.checkKeys() and self.signingKeys.checkKeys()

    def __str__(self):
        return f"User {self.userName} (ID: {self.userID})"
