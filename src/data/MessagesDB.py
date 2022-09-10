from src.SystemExceptions import *
from src.main.Circuit import Circuit
from src.main.PublicUser import *
import sqlite3, os

class Message:
    def __init__(self, messageID: int, content: bytes, signature: bytes, circuitUsed: Circuit,
                 sender, receiver, timeSent: float, timeReceived: float=None, isEncrypted: bool=False, isSigned: bool=False):
        self.messageID = messageID
        self.content = content
        self.signature = signature
        self.circuitUsed = circuitUsed
        self.sender, self.receiver = sender, receiver
        self.timeSent, self.timeReceived = timeSent, timeReceived
        self.isEncrypted, self.isSigned = isEncrypted, isSigned

    def encrypt(self): # When the sender is me, we encrypt the message with the receiver's Public Key.
        # Sender: User, Receiver: PublicUser
        if type(self.sender) is not PublicUser and type(self.receiver) is PublicUser:
            receiverPK = self.receiver.encryptionKey # RSA Public Key of the receiver.
            self.content = self.sender.encryptionKeys.encrypt(self.content, receiverPK)
            self.isEncrypted = True
        else:
            raise WrongUserError("The sender must be a User and the receiver a PublicUser.")

    def decrypt(self): # When the receiver is me, we decrypt the message with our Private Key.
        # Sender: PublicUser, Receiver: User
        if type(self.sender) is PublicUser and type(self.receiver) is not PublicUser:
            self.content = self.receiver.encryptionKeys.decrypt(self.content)
            self.isEncrypted = False
        else:
            raise WrongUserError("The sender must be a PublicUser and the receiver a User.")

    def sign(self): # When the sender is me, we sign the message with our Private Key.
        # Sender: User, Receiver: PublicUser
        if type(self.sender) is not PublicUser and type(self.receiver) is PublicUser:
            self.signature = self.sender.signingKeys.sign(self.content)
            self.isSigned = True
        else:
            raise WrongUserError("The sender must be a User and the receiver a PublicUser.")

    def verify(self): # When the receiver is me, we verify the message with the sender's Public Key.
        # Sender: PublicUser, Receiver: User
        if type(self.sender) is PublicUser and type(self.receiver) is not PublicUser:
            senderPK = self.sender.verificationKey # RSA Public Key of the sender.
            if not self.isSigned or not self.isEncrypted:
                print("WARNING: The message is not signed or encrypted.")
            return self.receiver.signingKeys.verify(self.content, self.signature, senderPK)
        else:
            raise WrongUserError("The sender must be a PublicUser and the receiver a User.")

    def __str__(self):
        return f"Message {self.messageID} from {self.sender} to {self.receiver}."

    def __repr__(self):
        return f"Message object with ID {self.messageID} from {self.sender} to {self.receiver}."

    def __eq__(self, other):
        return self.messageID == other.messageID

    def __len__(self):
        return len(self.content)

    def __getitem__(self, item):
        return self.content[item]

class MessagesDB:
    def __init__(self, dbPath: str="Messages.db"):
        firstTime = not(os.path.isfile(dbPath))
        self.dbPath = dbPath
        self.dbConnection = sqlite3.connect(self.dbPath)
        self.cursor = self.dbConnection.cursor()

        with open("../data/sqls/TablesCreation.sql", "r") as f:
            x = f.read() # Creation of the tables if they don't exist.
            self.cursor.executescript(x)
        self.dbConnection.commit()

        if firstTime:
            with open('../data/sqls/InitializeMetadata.sql', 'r') as f:
                x = f.read()
                self.cursor.executescript(x)
            self.dbConnection.commit()
            self.numberMessages = 0
        else:
            dbStored = self.cursor.execute("SELECT 'NumberMessages' "
                                       "FROM Metadata").fetchone()
            self.numberMessages = dbStored[0]

    def countMessages(self):
        dbStored = self.cursor.execute("SELECT NumberMessages "
                                       "FROM Metadata").fetchone()
        return dbStored[0]

    def addMessage(self, msg: Message):
        if msg.isEncrypted:
            # Transform the bytes into a string of hexadecimal numbers.
            content = msg.content.hex()
        else:
            content = msg.content.decode("utf-8")

        with open('../data/sqls/InsertMessage.sql', 'r') as f:
            x = f.read().replace('\n', '').split(";")
            if not msg.timeReceived: # Insert time received as NULL.
                self.cursor.execute(x[1], (msg.messageID,
                                        msg.sender.userID, msg.receiver.userID,
                                        msg.timeSent, content))
            else:
                self.cursor.execute(x[0], (msg.messageID,
                                        msg.sender.userID, msg.receiver.userID,
                                        msg.timeSent, msg.timeReceived,
                                        content))
        self.dbConnection.commit()
        self.numberMessages = self.countMessages()

    def deleteMessage(self, messageID: int):
        isDeleted = False
        with open('../data/sqls/DeleteMessage.sql', 'r') as f:
            x = f.read()
            self.cursor.execute(x, (messageID,))
        self.dbConnection.commit()
        oldCount = self.numberMessages
        self.numberMessages = self.countMessages()
        isDeleted = self.numberMessages < oldCount
        return isDeleted

    def getMessage(self, messageID: int, justContent: bool=False):
        """
        This function uses the queries from GetMessage.sql
        If justContent is False, we read and execute the first line of the file.
        If justContent is True, we read and execute the second line of the file.
        """
        with open('../data/sqls/GetMessage.sql', 'r') as f:
            x = f.read().replace('\n', '').split(";")
            if justContent:
                msg = self.cursor.execute(x[1], (str(messageID),)).fetchone()

            else:
                msg = self.cursor.execute(x[0], (str(messageID),)).fetchone()
        self.dbConnection.commit()

        if msg:
            return msg[0]
        else:
            raise MessageNotFoundError(f"Message {messageID} not found at {self.dbPath} database.")

    def __len__(self):
        return self.numberMessages

    def __getitem__(self, item):
        return self.getMessage(item)

    def __str__(self):
        return f"Messages database with {self.numberMessages} messages."
