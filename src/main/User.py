from src.main.Imports import *


class User:
    def __init__(
        self,
        userID: int,
        userName: str,
        rsaKeys: [RSAKeys, RSAKeys],
        IP: str,
        forwardingTable: ForwardingTable = None,
        messagesQueue: Queue = None,
        contacts: Contacts = None,
        messages: MessagesDB = None,
    ):
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

    def createMessageToSend(self, content: str, toUserName: str) -> Message:
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
        timeCreated = int(getTime())
        messageID = SHA256.new(
            f"{userSender.userName}{userReceiver.userName}{timeCreated}{content}".encode()
        ).hexdigest()
        msg = Message(
            messageID,
            content.encode(),
            b"",
            circuitUsed,
            userSender,
            userReceiver,
            timeCreated,
        )
        self.messages.addMessage(msg)  # Store the message withouth encryption/signature

        msg.encrypt()
        msg.sign()
        return msg

    def createMessageToReceive(
        self, msgData: dict, ignoreVerification=False
    ) -> Message:
        """
        This method receives a dictionary generated after reading a NetworkMessage as bytes,
        from this data we extract all the information to create a message.
        :param msgData: Dictionary with the message content and sender/receiver encrypted.
        :param ignoreVerification: Boolean to ignore the verification of the message.
        :return: Message object with the content decrypted.
        """
        signature = msgData["signature"]
        encryptedContent = msgData["encryptedContent"]
        encryptedSenderName = msgData["fromUser"]
        encryptedReceiverName = msgData["toUser"]
        timeCreated = msgData["timeCreated"]
        timeReceived = int(getTime())

        senderName = self.encryptionKeys.decrypt(encryptedSenderName).decode()
        receiverName = self.encryptionKeys.decrypt(encryptedReceiverName).decode()

        try:
            sender = self.contacts[senderName]
        except KeyError:
            raise Exception(f"Sender {senderName} not found in contacts.")

        receiver = self if receiverName == self.userName else None
        circuitUsed = sender.throughCircuit

        if not receiver:
            raise ValueError("The message is not for you.")
        else:
            msg = Message(
                "tempID",
                encryptedContent,
                signature,
                circuitUsed,
                sender,
                receiver,
                timeCreated,
                timeReceived,
                isEncrypted=True,
                isSigned=True,
            )
            isVerified = msg.verify()
            if not ignoreVerification and not isVerified:
                raise Exception("Message signature verification failed.")
            else:
                msg.decrypt()
                msg.updateMessageID()
                if self.messages.isMessage(msg.messageID):
                    # If we already have the message its the updated message with the received date.
                    messageID = self.messages.getMessage(msg.messageID)[0]
                    self.messages.updateTimeReceived(
                        messageID, timeReceived
                    )  # Update the time received.

                return msg

    def toPublicUser(self) -> PublicUser:
        """
        This method is used to create your own public information so other users can add it.
        The Circuit is created empty because this depends on both users.
        :return: The user as a Public User with the public information.
        """
        rsaPublicKeys = [self.encryptionKeys.publicKey, self.signingKeys.publicKey]
        return PublicUser(self.userID, self.userName, rsaPublicKeys, Circuit())

    def computeMessageID(
        self, senderName: str, receiverName: str, timeCreated: int, content: str
    ) -> str:
        """
        This method is used to compute the message ID from the message content.
        The message ID is a unique identifier of a message sent between two users in a certain moment.
        This ID is created by the sender of the message.
        :param senderName: String username of the sender.
        :param receiverName: String username of the receiver.
        :param timeCreated: UNIX Timestamp of the creation time.
        :param content: The content as a string.
        :return: The message ID as a string.
        """
        return SHA256.new(  # The input is converted to bytes because the SHA256 requires bytes.
            f"{senderName}{receiverName}{timeCreated}{content}".encode()
        ).hexdigest()

    def deleteMessage(self, messageID: str):
        self.messages.deleteMessage(messageID)

    def getMessage(self, messageID: str) -> Message:
        return self.messages[messageID]

    def numberOfMessages(self) -> int:
        return len(self.messages)

    def numberOfContacts(self) -> int:
        return len(self.contacts)

    def addToTable(self, circuitID: str, node: Node):
        self.forwardingTable.addEntry(circuitID, node)

    def forwardTo(self, circuitID: str) -> Node:
        return self.forwardingTable[circuitID]

    def addtoQueue(self, message: Message):
        self.messagesQueue.addMessage(message.messageID)

    def nextOnQueue(self) -> Message:
        nextMessageID = self.messagesQueue.nextMessage()
        return self.messages[nextMessageID]

    def addContact(self, contact: PublicUser):
        self.contacts.addContact(contact)

    def removeContact(self, userName: str):
        toRemove = self.contacts[userName]
        self.contacts.removeContact(toRemove)

    def updateTable(self, circuitID: str, node: Node):
        self.forwardingTable.replaceEntry(circuitID, node)

    def exportKeys(self, encryptionPath: str, signingPath: str):
        self.encryptionKeys.exportKeys(encryptionPath)
        self.signingKeys.exportKeys(signingPath)

    def importKeys(self, encryptionPath: str, signingPath: str):
        self.encryptionKeys.importKeys(encryptionPath)
        self.signingKeys.importKeys(signingPath)

    def checkKeys(self) -> bool:
        return self.encryptionKeys.checkKeys() and self.signingKeys.checkKeys()

    def exportUser(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.asJSON()))

    def importUser(self, path: str):
        with open(path, "r") as f:
            data = json.loads(f.read())
            self.userID = data["UserID"]
            self.userName = data["UserName"]
            self.encryptionKeys = RSAKeys(
                toImport=True, fileName=data["EncryptionKeys"]
            )
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
        return {
            "UserID": self.userID,
            "UserName": self.userName,
            "EncryptionKeys": self.encryptionKeys.filename,
            "SigningKeys": self.signingKeys.filename,
            "IP": self.IP,
            "ForwardingTable": self.forwardingTable.asJSON(),
            "MessagesQueue": self.messagesQueue.asJSON(),
            "UserFriends": self.contacts.asJSON(),
            "Messages": self.messages.dbPath,
        }

    def __eq__(self, other) -> bool:
        return (
            self.userID == other.userID
            and self.userName == other.userName
            and self.encryptionKeys == other.encryptionKeys
            and self.signingKeys == other.signingKeys
            and self.IP == other.IP
            and self.forwardingTable == other.forwardingTable
            and self.messagesQueue == other.messagesQueue
            and self.contacts == other.contacts
            and self.messages == other.messages
        )

    def __str__(self) -> str:
        return (
            f"User {self.userName} (ID: {self.userID}) "
            f"with IP {self.IP} and keys {self.encryptionKeys} and {self.signingKeys}."
        )


def createUser(userName, IP, ID) -> User:
    myUser = User(
        ID,
        userName,
        [
            RSAKeys(fileName=os.path.join(KEYS_PATH, ENC_KEYS_NAME + userName)),
            RSAKeys(fileName=os.path.join(KEYS_PATH, SIG_KEYS_NAME + userName)),
        ],
        IP,
        forwardingTable=ForwardingTable(),
        messagesQueue=Queue(),
        contacts=Contacts(),
        messages=MessagesDB(
            dbPath=os.path.join(DB_PATH, (DB_NAME + userName + "." + DB_EXTENSION))
        ),
    )
    return myUser
