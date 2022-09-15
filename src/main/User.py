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
        self.encryptionKeys.updateKeys()
        self.signingKeys.updateKeys()

    def exportKeys(self, encryptionPath: str, signingPath: str):
        self.encryptionKeys.exportKeys(encryptionPath)
        self.signingKeys.exportKeys(signingPath)

    def importKeys(self, encryptionPath: str, signingPath: str):
        self.encryptionKeys.importKeys(encryptionPath)
        self.signingKeys.importKeys(signingPath)

    def checkKeys(self):
        return self.encryptionKeys.checkKeys() and self.signingKeys.checkKeys()

    def exportUser(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.asJSON()))

    def importUser(self, path: str):
        with open(path, "r") as f:
            data = json.loads(f.read())
            self.userID = data["UserID"]
            self.userName = data["UserName"]
            self.encryptionKeys = RSAKeys(toImport=True, fileName=data["EncryptionKeys"])
            self.signingKeys = RSAKeys(toImport=True, fileName=data["SigningKeys"])
            self.IP = data["IP"]
            self.forwardingTable = data["ForwardingTable"]
            self.messagesQueue = data["MessagesQueue"]
            self.userFriends = data["UserFriends"]
            self.messages = MessagesDB(dbPath=data["Messages"])

    def asJSON(self) -> dict:
        return {"UserID": self.userID,
                "UserName": self.userName,
                "EncryptionKeys": self.encryptionKeys.filename,
                "SigningKeys": self.signingKeys.filename,
                "IP": self.IP,
                "ForwardingTable": 'None', # TODO: Implement forwarding table.
                "MessagesQueue": 'None', # TODO: Implement messages queue.
                "UserFriends": 'None', # TODO: Implement user friends.
                "Messages": self.messages.dbPath}

    def __eq__(self, other):
        return self.userID == other.userID \
               and self.userName == other.userName \
               and self.encryptionKeys == other.encryptionKeys \
               and self.signingKeys == other.signingKeys \
               and self.IP == other.IP \
               and self.forwardingTable == other.forwardingTable \
               and self.messagesQueue == other.messagesQueue \
               and self.userFriends == other.userFriends \
               and self.messages == other.messages

    def __str__(self):
        return f"User {self.userName} (ID: {self.userID}) with IP {self.IP} and keys {self.encryptionKeys} and {self.signingKeys}."
