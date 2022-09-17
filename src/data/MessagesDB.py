from src.data.Imports import *

class Message:
    def __init__(self, messageID: str, content: bytes, signature: bytes, circuitUsed: Circuit,
                 sender: "User", receiver: "PublicUser", timeCreated: float, timeReceived: float=None, isEncrypted: bool=False, isSigned: bool=False):
        self.messageID = messageID
        self.content = content
        self.signature = signature
        self.circuitUsed = circuitUsed
        self.sender, self.receiver = sender, receiver
        self.timeCreated, self.timeReceived = timeCreated, timeReceived
        self.isEncrypted, self.isSigned = isEncrypted, isSigned

    def updateMessageID(self):
        senderName = self.sender.userName
        receiverName = self.receiver.userName
        self.messageID = SHA256.new(f"{senderName}{receiverName}{self.timeCreated}{self.content.decode()}".encode()).hexdigest()
        return self.messageID

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

    def verify(self) -> bool: # When the receiver is me, we verify the message with the sender's Public Key.
        # Sender: PublicUser, Receiver: User
        if type(self.sender) is PublicUser and type(self.receiver) is not PublicUser:
            senderPK = self.sender.verificationKey # RSA Public Key of the sender.
            if not self.isSigned or not self.isEncrypted:
                print("WARNING: The message is not signed or encrypted.")
            return self.receiver.signingKeys.verify(self.content, self.signature, senderPK)
        else:
            raise WrongUserError("The sender must be a PublicUser and the receiver a User.")

    def toNetworkMessage(self) -> NetworkMessage:
        if not self.isEncrypted: self.encrypt()
        if not self.isSigned: self.sign()

        encPK = self.sender.encryptionKeys.publicKey
        sigPK = self.sender.signingKeys.publicKey
        publicSender = PublicUser(self.sender.userID,
                                  self.sender.userName,
                                  [encPK, sigPK],
                                  self.circuitUsed)
        publicReceiver = self.receiver

        netMsg = NetworkMessage(self.content, publicSender, publicReceiver, self.timeCreated, self.signature)
        return netMsg

    def __str__(self):
        return f"Message {self.messageID} from {self.sender} to {self.receiver}."

    def __repr__(self):
        return f"Message object with ID {self.messageID} from {self.sender} to {self.receiver}."

    def __eq__(self, other: "Message"):
        return self.messageID == other.messageID

    def __len__(self):
        return len(self.content)

    def __getitem__(self, item:int):
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

    def countMessages(self) -> int:
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
                                           msg.timeCreated, content))
            else:
                self.cursor.execute(x[0], (msg.messageID,
                                           msg.sender.userID, msg.receiver.userID,
                                           msg.timeCreated, msg.timeReceived,
                                           content))
        self.dbConnection.commit()
        self.numberMessages = self.countMessages()

    def deleteMessage(self, messageID: int) -> bool:
        isDeleted = False
        with open('../data/sqls/DeleteMessage.sql', 'r') as f:
            x = f.read()
            self.cursor.execute(x, (messageID,))
        self.dbConnection.commit()
        oldCount = self.numberMessages
        self.numberMessages = self.countMessages()
        isDeleted = self.numberMessages < oldCount
        return isDeleted

    def getMessage(self, messageID: str, justContent: bool=False) -> Message:
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

    def encryptDatabase(self, key: str) -> (bytes, bytes):
        """
        This function opens the content on the dbPath file, reads it as bytes
        and encrypts it with the key provided and the random 16 bytes.
        It returns the encrypted content as bytes and the nonce.
        :param key: Any string used to encrypt the data.
        :return: Database content encrypted as bytes and the nonce used.
        """
        keyBytes, nonce = key.encode(), urandom(16)
        with open(self.dbPath, "rb") as f:
            dbContent = f.read()

        encryptor = AES.new(keyBytes, nonce)
        return encryptor.encrypt(dbContent), nonce

    def decryptDatabase(self, key: str, nonce: bytes) -> bytes:
        """
        This function decrypts the content of the dbPath file with the key and nonce provided.
        :param key: Any string used to decrypt the data.
        :param nonce: The nonce used to encrypt the data.
        :return: Database content decrypted as bytes.
        """
        keyBytes = key.encode()
        with open(self.dbPath, "rb") as f:
            dbContent = f.read()

        decryptor = AES.new(keyBytes, nonce)
        return decryptor.decrypt(dbContent)

    def __len__(self):
        return self.numberMessages

    def __getitem__(self, item: str):
        return self.getMessage(item)

    def __eq__(self, other: "MessagesDB"):
        return self.dbPath == other.dbPath

    def __str__(self):
        return f"Messages database with {self.numberMessages} messages."
