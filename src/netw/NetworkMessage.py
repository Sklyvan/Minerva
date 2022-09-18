import pickle, base64

class NetworkMessage:
    def __init__(self, encryptedContent: bytes = None,
                 fromUser: "PublicUser" = None, toUser: "PublicUser" = None,
                 timeCreated: int = None, signature: bytes = None):
        """
        This class is used to define how the messages are sent over the network.
        The messages are stored as Message objects, then, are transformed to this
        class with Message.toNetworkMessage(), from this class are transformed to
        bytes with bytes(NetworkMessage) and then, are sent over the network.
        :param encryptedContent: This is the content of the message encrypted with the toUser's RSA Public Key.
        :param fromUser: Sender of the message as a Public User.
        :param toUser: Receiver of the message as a Public User.
        :param timeCreated: Time when the message was created in UNIX time.
        :param signature: Signature of the message created with the fromUser's RSA Private Key.
        """
        self.encryptedContent = encryptedContent
        self.fromUser, self.toUser = fromUser, toUser
        self.timeCreated = timeCreated
        self.signature = signature
        self.fromEncrypted, self.toEncrypted = self.encryptUsers() # Usernames encrypted.

    def encryptUsers(self):
        # Encrypt the usernames with the Public Key of the receiver.
        fromUserName, toUserName = self.fromUser.userName.encode(), self.toUser.userName.encode()
        return self.toUser.encrypt(fromUserName), self.toUser.encrypt(toUserName)

    def toJavaScript(self):
        asDict = {"encryptedContent": base64.b64encode(self.encryptedContent),
                  "fromUser": base64.b64encode(self.fromEncrypted),
                  "toUser": base64.b64encode(self.toEncrypted),
                  "timeCreated": self.timeCreated,
                  "signature": base64.b64encode(self.signature)}
        return str(asDict)

    def __iter__(self):
        asDict = {"encryptedContent": self.encryptedContent,
                  "fromUser": self.fromEncrypted,
                  "toUser": self.toEncrypted,
                  "timeCreated": self.timeCreated,
                  "signature": self.signature}
        return [(k, v) for k, v in asDict.items()].__iter__()

    def __bytes__(self):
        return pickle.dumps(dict(self))

    def __str__(self):
        return f"Message with content {self.encryptedContent} from {self.fromUser} to {self.toUser}."

def loadNetworkMessage(data: bytes):
    asDict = pickle.loads(data)
    return asDict
