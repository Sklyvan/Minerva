import unittest
from src.data.MessagesDB import *
from src.data.MessagesQueue import *
from src.main.User import *
import glob, os

class MessageTest(unittest.TestCase):
    def testMessageSecurity(self):
        User1 = User(1, "User1", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.1", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User1Public = PublicUser(1, "User1", [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
                                      Circuit())
        User2 = User(2, "User2", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.2", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User2Public = PublicUser(2, "User2", [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
                                      Circuit())

        Message1U1 = Message(1, b"Hello World!", b"", Circuit(), User1, User2Public, int(time())) # Create a sample message
        # Initially, the message is not encrypted or signed. We encrypt for User 2 and sign as User 1.
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(1, Message1U1.content, Message1U1.signature, Circuit(), User1Public, User2,
                             Message1U1.timeCreated, int(time()), True, True) # Simulate the message being sent to User 2
        self.assertTrue(Message1U2.verify(), "Verification failed.") # Verify the signature
        Message1U2.decrypt() # Decrypt the message
        self.assertEqual(Message1U2.content, b"Hello World!", "Decryption failed.")
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.pem"): os.remove(file)

    def testMessageDBCounting(self):
        for file in glob.glob("*.db"): os.remove(file)

        User1 = User(1, "User1", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.1", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User1Public = PublicUser(1, "User1", [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
                                 Circuit())
        User2 = User(2, "User2", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.2", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User2Public = PublicUser(2, "User2", [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
                                 Circuit())

        Message1U1 = Message(1, b"Hello World!", b"", Circuit(), User1, User2Public, int(time()), int(time()))
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(2, Message1U1.content, Message1U1.signature, Circuit(), User1Public, User2,
                             Message1U1.timeCreated, int(time()), True, True)
        Message1U2.verify()
        Message1U2.decrypt()

        DB = MessagesDB("Messages.db")
        DB.addMessage(Message1U1)
        self.assertEqual(len(DB), 1, "Message 1 not being counted.")
        DB.addMessage(Message1U2)
        self.assertEqual(len(DB), 2, "Message 2 not being counted.")
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.pem"): os.remove(file)

    def testMessageDBInsert(self):
        for file in glob.glob("*.db"): os.remove(file)

        User1 = User(1, "User1", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.1", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User1Public = PublicUser(1, "User1", [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
                                 Circuit())
        User2 = User(2, "User2", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.2", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User2Public = PublicUser(2, "User2", [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
                                 Circuit())

        Message1U1 = Message(1, b"Hello World!", b"", Circuit(), User1, User2Public, int(time()))
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(2, Message1U1.content, Message1U1.signature, Circuit(), User1Public, User2,
                             Message1U1.timeCreated, int(time()) + 10, True, True)
        Message1U2.verify()
        Message1U2.decrypt()

        DB = MessagesDB("Messages.db")
        DB.addMessage(Message1U1)
        DB.addMessage(Message1U2)
        self.assertEqual(DB.getMessage(Message1U1.messageID, justContent=True), Message1U1.content.hex(), "Message 1 not being inserted.")
        self.assertEqual(DB.getMessage(Message1U2.messageID, justContent=True), Message1U2.content.decode('utf-8'), "Message 2 not being inserted.")
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.pem"): os.remove(file)

    def testMessageDBDelete(self):
        for file in glob.glob("*.db"): os.remove(file)

        User1 = User(1, "User1", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.1", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User1Public = PublicUser(1, "User1", [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
                                 Circuit())
        User2 = User(2, "User2", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.2", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User2Public = PublicUser(2, "User2", [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
                                 Circuit())

        Message1U1 = Message(1, b"Hello World!", b"", Circuit(), User1, User2Public, int(time()))
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(2, Message1U1.content, Message1U1.signature, Circuit(), User1Public, User2,
                             Message1U1.timeCreated, int(time()) + 10, True, True)
        Message1U2.verify()
        Message1U2.decrypt()

        DB = MessagesDB("Messages.db")
        DB.addMessage(Message1U1)
        DB.addMessage(Message1U2)

        self.assertEqual(len(DB), 2, "Messages not being counted.")
        DB.deleteMessage(Message1U1.messageID)
        self.assertEqual(len(DB), 1, "Message 1 not being deleted.")
        DB.deleteMessage(Message1U2.messageID)
        self.assertEqual(len(DB), 0, "Message 2 not being deleted.")
        DB.deleteMessage(-1)
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.pem"): os.remove(file)

    def testNetworkMessageConvertion(self):
        for file in glob.glob("*.db"): os.remove(file)

        User1 = User(1, "User1", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.1", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User1Public = PublicUser(1, "User1", [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
                                 Circuit())
        User2 = User(2, "User2", [RSAKeys(fileName='TestKey'), RSAKeys(fileName='TestKey')],
                     "127.0.0.2", ForwardingTable(), Queue(), Contacts(), MessagesDB())
        User2Public = PublicUser(2, "User2", [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
                                 Circuit())

        User1.contacts.addContact(User2Public)
        User2.contacts.addContact(User1Public)

        msgU1 = Message('tempID', b"Hello World!", b"", Circuit(), User1, User2Public, int(time())) # User 1 creates the message to be sent to User 2.
        msgU1.updateMessageID()
        ntwMsgU1 = msgU1.toNetworkMessage() # Transforms the message to NetworkMessage.
        asBytes = bytes(ntwMsgU1) # Transforms the NetworkMessage to bytes and sends this bytes to User 2.

        ntwMsgU2 = loadNetworkMessage(asBytes) # The User 2 receives the bytes and reads them.

        msgU2 = User2.createMessageToReceive(ntwMsgU2)

        self.assertEqual(b"Hello World!", msgU2.content, "Message content not being decrypted.")
        self.assertEqual(msgU1.timeCreated, msgU2.timeCreated, "Message time not being read.")
        self.assertEqual(msgU1.sender.userID, msgU2.sender.userID, "Message sender not being read.")
        self.assertEqual(msgU1.receiver.userID, msgU2.receiver.userID, "Message receiver not being read.")
        self.assertEqual(msgU1.messageID, msgU2.messageID, "Message ID not being computed right.")

        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.pem"): os.remove(file)


class TestQueue(unittest.TestCase):
    def testQueueAddRemove(self):
        myQueue = Queue()
        self.assertEqual(len(myQueue), 0, "Queue not empty.")

        myQueue.addMessage(1)
        self.assertEqual(len(myQueue), 1, "Queue not adding.")
        myQueue.addMessage(2)
        self.assertEqual(len(myQueue), 2, "Queue not adding.")
        myQueue.addMessage(3)
        self.assertEqual(len(myQueue), 3, "Queue not adding.")

        msg = myQueue.nextMessage()
        self.assertEqual(msg, 1, "Queue not returning correct message.")
        msg = myQueue.nextMessage()
        self.assertEqual(msg, 2, "Queue not returning correct message.")
        msg = myQueue.nextMessage()
        self.assertEqual(msg, 3, "Queue not returning correct message.")


    def testQueueExport(self):
        myQueue = Queue()
        self.assertEqual(len(myQueue), 0, "Queue not empty.")

        myQueue.addMessage(1)
        self.assertEqual(len(myQueue), 1, "Queue not adding.")
        myQueue.addMessage(2)
        self.assertEqual(len(myQueue), 2, "Queue not adding.")
        myQueue.addMessage(3)
        self.assertEqual(len(myQueue), 3, "Queue not adding.")

        myQueue.exportQueue("TestQueue.json")
        myQueue_ = Queue()
        myQueue_.importQueue("TestQueue.json")

        self.assertEqual(myQueue, myQueue_, "Queue not exporting correctly.")
        for file in glob.glob("*.json"): os.remove(file)


if __name__ == '__main__':
    unittest.main()
