from src.main.Imports import *

class User:
    def __init__(self, userID: int, userName: str, rsaKeys: [RSAKeys, RSAKeys], IP: str,
                 forwardingTable: ForwardingTable = None, messagesQueue: Queue = None, contacts: Contacts = None, messages: MessagesDB = None):
        self.userID = userID
        self.userName = userName
        self.encryptionKeys, self.signingKeys = rsaKeys
        self.IP = IP
        self.forwardingTable = forwardingTable
        self.messagesQueue = messagesQueue
        self.contacts = contacts
        self.messages = messages

    def regenerateKeys(self):
        self.encryptionKeys.updateKeys()
        self.signingKeys.updateKeys()

    def createMessage(self, content: str, toUserName: str) -> Message:
        """
        This method receives the content of the message and the receiver's username,
        then it extracts the sender/receiver as PublicUser objects, stores the creation time.
        The message ID comes from a SHA-256 hash of the content, sender, receiver and creation time.
        Once the message objects is created, we store it into the database without the RSA encryption,
        then we encrypt it with the receiver Public Key and sign it with the sender Private Key.
        :param content: String containing the message content, it's transformed into bytes.
        :param toUserName: String containing the receiver's username.
        :return: Message object already encrypted and signed.
        """
        userReceiver, userSender = self.contacts[toUserName], self
        circuitUsed = userReceiver.throughCircuit
        timeCreated = int(time())
        messageID = SHA256.new(f"{userSender.userName}{userReceiver.userName}{timeSent}{content}".encode()).hexdigest()
        msg = Message(messageID, content.encode(), b'', circuitUsed, userSender, userReceiver, timeCreated)
        self.messages.addMessage(msg) # Store the message withouth encryption/signature

        msg.encrypt()
        msg.sign()
        return message

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

            self.forwardingTable = ForwardingTable()
            self.forwardingTable.readTable(data["ForwardingTable"])

            self.messagesQueue = Queue()
            self.messagesQueue.readQueue(data["MessagesQueue"])

            self.contacts = Contacts()
            self.contacts.readContacts(data["UserFriends"])

            self.messages = MessagesDB(dbPath=data["Messages"])

    def asJSON(self) -> dict:
        return {"UserID": self.userID,
                "UserName": self.userName,
                "EncryptionKeys": self.encryptionKeys.filename,
                "SigningKeys": self.signingKeys.filename,
                "IP": self.IP,
                "ForwardingTable": self.forwardingTable.asJSON(),
                "MessagesQueue": self.messagesQueue.asJSON(),
                "UserFriends": self.contacts.asJSON(),
                "Messages": self.messages.dbPath}

    def __eq__(self, other):
        return self.userID == other.userID \
               and self.userName == other.userName \
               and self.encryptionKeys == other.encryptionKeys \
               and self.signingKeys == other.signingKeys \
               and self.IP == other.IP \
               and self.forwardingTable == other.forwardingTable \
               and self.messagesQueue == other.messagesQueue \
               and self.contacts == other.contacts \
               and self.messages == other.messages

    def __str__(self):
        return f"User {self.userName} (ID: {self.userID}) with IP {self.IP} and keys {self.encryptionKeys} and {self.signingKeys}."
