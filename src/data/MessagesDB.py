from src.SystemExceptions import *
from src.main.Circuit import Circuit
from src.main.PublicUser import *

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
    None