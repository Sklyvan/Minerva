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
            self.userID = data["userID"]
            self.userName = data["userName"]
            self.encryptionKeys = RSAKeys(toImport=True, fileName=data["encryptionKeys"])
            self.signingKeys = RSAKeys(toImport=True, fileName=data["signingKeys"])
            self.IP = data["IP"]
            self.forwardingTable = data["forwardingTable"]
            self.messagesQueue = data["messagesQueue"]
            self.userFriends = data["userFriends"]
            self.messages = MessagesDB(dbPath=data["messages"])

    def asJSON(self) -> dict:
        return {"userID": self.userID,
                "userName": self.userName,
                "encryptionKeys": self.encryptionKeys.filename,
                "signingKeys": self.signingKeys.filename,
                "IP": self.IP,
                "forwardingTable": 'None', # TODO: Implement forwarding table.
                "messagesQueue": 'None', # TODO: Implement messages queue.
                "userFriends": 'None', # TODO: Implement user friends.
                "messages": self.messages.dbPath}

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
