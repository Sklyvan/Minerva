import unittest
import random, glob, os
from src.cryp.RSAKeys import *
from src.cryp.DiffieHellmanKey import *
from src.cryp.AES import *
from src.data.MessagesDB import *
from src.data.MessagesQueue import *
from src.main.User import *
from src.netw.bor.RoutingPackets import *
from src.main.MainSystem import *

from src.main.User import *
import glob, os


class UserTest(unittest.TestCase):
    def testImportExportData(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()
        K3 = DiffieHellmanKey()
        K4 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)
        K3.generateSharedKey(K4.publicKey)
        K4.generateSharedKey(K3.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)
        N3 = Node("127.0.0.3", K3)
        N4 = Node("127.0.0.4", K4)

        Circuit1 = Circuit("CIRCUIT1", [N1, N2])
        Circuit2 = Circuit("CIRCUIT1", [N3, N4])

        ExampleTable = ForwardingTable()
        ExampleTable.addEntry("CIRCUIT1", N1)
        ExampleTable.addEntry("CIRCUIT2", N2)
        ExampleTable.addEntry("CIRCUIT3", N3)
        ExampleTable.addEntry("CIRCUIT4", N4)

        User1 = PublicUser(
            1,
            "User1",
            [RSA.generate(2048).public_key(), RSA.generate(2048).public_key()],
            Circuit1,
        )
        User2 = PublicUser(
            2,
            "User2",
            [RSA.generate(2048).public_key(), RSA.generate(2048).public_key()],
            Circuit2,
        )

        Friends = Contacts()
        Friends.addContact(User1)
        Friends.addContact(User2)

        MessagesQueue = Queue()
        for i in range(10):
            MessagesQueue.addMessage(i)

        MyUser = User(
            1,
            "MyUser",
            [
                RSAKeys(fileName="TestEncKeys"),
                RSAKeys(fileName="TestSigKeys"),
            ],
            "127.0.0.1",
            forwardingTable=ExampleTable,
            messagesQueue=MessagesQueue,
            contacts=Friends,
            messages=MessagesDB(dbPath="TestMessages.db"),
        )
        MyUser.exportUser("TestMyUser.json")

        MyUserCheck = User(None, None, [None, None], None)
        MyUserCheck.importUser("TestMyUser.json")

        self.assertEqual(MyUser, MyUserCheck, "Users are not equal.")

        for file in glob.glob("Test*.pem"):
            os.remove(file)
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testEncryptedImportExport(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()
        K3 = DiffieHellmanKey()
        K4 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)
        K3.generateSharedKey(K4.publicKey)
        K4.generateSharedKey(K3.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)
        N3 = Node("127.0.0.3", K3)
        N4 = Node("127.0.0.4", K4)

        Circuit1 = Circuit("CIRCUIT1", [N1, N2])
        Circuit2 = Circuit("CIRCUIT1", [N3, N4])

        ExampleTable = ForwardingTable()
        ExampleTable.addEntry("CIRCUIT1", N1)
        ExampleTable.addEntry("CIRCUIT2", N2)
        ExampleTable.addEntry("CIRCUIT3", N3)
        ExampleTable.addEntry("CIRCUIT4", N4)

        User1 = PublicUser(
            1,
            "User1",
            [RSA.generate(2048).public_key(), RSA.generate(2048).public_key()],
            Circuit1,
        )
        User2 = PublicUser(
            2,
            "User2",
            [RSA.generate(2048).public_key(), RSA.generate(2048).public_key()],
            Circuit2,
        )

        Friends = Contacts()
        Friends.addContact(User1)
        Friends.addContact(User2)

        MessagesQueue = Queue()
        for i in range(10):
            MessagesQueue.addMessage(i)

        MyUser = User(
            1,
            "MyUser",
            [
                RSAKeys(fileName="TestEncKeys"),
                RSAKeys(fileName="TestSigKeys"),
            ],
            "127.0.0.1",
            forwardingTable=ExampleTable,
            messagesQueue=MessagesQueue,
            contacts=Friends,
            messages=MessagesDB(dbPath="TestMessages.db"),
        )
        exportKey = "".join([chr(random.randint(32, 126)) for _ in range(100)])
        MyUser.exportEncryptedUser("TestMyUser.json", exportKey)

        MyUserCheck = User(None, None, [None, None], None)
        MyUserCheck.importEncryptedUser("TestMyUser.json", exportKey)

        self.assertEqual(MyUser, MyUserCheck, "Users are not equal.")

        for file in glob.glob("Test*.pem"):
            os.remove(file)
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testImportExportKeys(self):
        MyUser1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestEncKeys"), RSAKeys(fileName="TestSigKeys")],
            "127.0.0.1",
        )
        MyUser1.exportKeys("TestEncKeys", "TestSigKeys")

        MyUser2 = User(
            2,
            "User2",
            [
                # This display a text error because we are creating imaginary keys that do not really exist.
                RSAKeys(fileName="TestTempE", toImport=True),
                RSAKeys(fileName="TestTempS", toImport=True),
            ],
            "127.0.0.2",
        )
        MyUser2.importKeys("TestEncKeys", "TestSigKeys")

        self.assertEqual(
            MyUser1.encryptionKeys,
            MyUser2.encryptionKeys,
            "Encryption keys are not equal.",
        )
        self.assertEqual(
            MyUser1.signingKeys, MyUser2.signingKeys, "Signing keys are not equal."
        )
        self.assertTrue(MyUser1.checkKeys(), "Keys 1 are not valid.")
        self.assertTrue(MyUser2.checkKeys(), "Keys 2 are not valid.")

        for file in glob.glob("Test*.pem"):
            os.remove(file)
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testImportExportEncryptedKeys(self):
        keysPassword = "".join([chr(random.randint(32, 126)) for _ in range(100)])

        MyUser1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestEncKeys"), RSAKeys(fileName="TestSigKeys")],
            "127.0.0.1",
        )
        MyUser1.exportKeys("TestEncKeys", "TestSigKeys", keysPassword)

        MyUser2 = User(
            2,
            "User2",
            [
                RSAKeys(fileName="TestTempE", toImport=True),
                RSAKeys(fileName="TestTempS", toImport=True),
            ],
            "127.0.0.2",
        )
        MyUser2.importKeys("TestEncKeys", "TestSigKeys", keysPassword)

        self.assertEqual(
            MyUser1.encryptionKeys,
            MyUser2.encryptionKeys,
            "Encryption keys are not equal.",
        )
        self.assertEqual(
            MyUser1.signingKeys, MyUser2.signingKeys, "Signing keys are not equal."
        )
        self.assertTrue(MyUser1.checkKeys(), "Keys 1 are not valid.")
        self.assertTrue(MyUser2.checkKeys(), "Keys 2 are not valid.")

        for file in glob.glob("Test*.pem"):
            os.remove(file)
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.json"):
            os.remove(file)


class NodeTest(unittest.TestCase):
    def testImportExportNode(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        N1.exportNode("TestNode.json")
        N2.importNode("TestNode.json")

        self.assertEqual(N1, N2)

        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testNodeAsJSON(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)

        self.assertEqual(N1.asJSON(), {"IP": "127.0.0.1", "DiffieHellmanKey": repr(K1)})


class CircuitTest(unittest.TestCase):
    def testCircuitImportExport(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        MyCircuit1 = Circuit("Circuit")
        MyCircuit2 = Circuit("Circuit")

        MyCircuit1.addNode(N1)
        MyCircuit1.addNode(N2)

        MyCircuit1.exportCircuit("TestCircuit.json")
        MyCircuit2.importCircuit("TestCircuit.json")

        self.assertEqual(MyCircuit1, MyCircuit2)

        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testCircuitAsJSON(self):
        self.maxDiff = None

        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        MyCircuit = Circuit("Circuit")
        MyCircuit.addNode(N1)
        MyCircuit.addNode(N2)

        self.assertEqual(
            MyCircuit.asJSON(), {"ID": "Circuit", "Nodes": [N1.asJSON(), N2.asJSON()]}
        )

        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testCircuitAddRemoveNode(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        MyCircuit = Circuit("Circuit")
        MyCircuit.addNode(N1)
        MyCircuit.addNode(N2)

        self.assertEqual(MyCircuit.nodes, [N1, N2])
        self.assertEqual(len(MyCircuit.nodes), 2)

        MyCircuit.removeNode(N1)
        MyCircuit.removeNode(N2)
        self.assertEqual(MyCircuit.nodes, [])


class ForwardingTableTest(unittest.TestCase):
    def testForwardingTableImportExport(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        ExampleTable = ForwardingTable()
        ExampleTable.addEntry("CIRCUIT1", N1)
        ExampleTable.addEntry("CIRCUIT2", N2)

        ExampleTable.exportTable("TestTable.json")

        ExampleTable2 = ForwardingTable()
        ExampleTable2.importTable("TestTable.json")

        self.assertEqual(ExampleTable, ExampleTable2)

        for file in glob.glob("Test*.json"):
            os.remove(file)

    def testForwardingTableAsJSON(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        ExampleTable = ForwardingTable()
        ExampleTable.addEntry("CIRCUIT1", N1)
        ExampleTable.addEntry("CIRCUIT2", N2)

        self.assertEqual(
            ExampleTable.asJSON(), {"CIRCUIT1": N1.asJSON(), "CIRCUIT2": N2.asJSON()}
        )

    def testForwardingTableAddRemoveEntry(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        ExampleTable = ForwardingTable()
        ExampleTable.addEntry("CIRCUIT1", N1)
        ExampleTable.addEntry("CIRCUIT2", N2)

        self.assertEqual(ExampleTable.table, {"CIRCUIT1": N1, "CIRCUIT2": N2})

        ExampleTable.removeEntry("CIRCUIT1")
        ExampleTable.removeEntry("CIRCUIT2")
        self.assertEqual(ExampleTable.table, {})

    def testForwardingTableGetEntry(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        ExampleTable = ForwardingTable()
        ExampleTable.addEntry("CIRCUIT1", N1)
        ExampleTable.addEntry("CIRCUIT2", N2)

        self.assertEqual(ExampleTable["CIRCUIT1"], N1)
        self.assertEqual(ExampleTable["CIRCUIT2"], N2)


class MessageTest(unittest.TestCase):
    def testMessageSecurity(self):
        User1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.1",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test1.db"),
        )
        User1Public = PublicUser(
            1,
            "User1",
            [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
            Circuit(),
        )
        User2 = User(
            2,
            "User2",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.2",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test2.db"),
        )
        User2Public = PublicUser(
            2,
            "User2",
            [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
            Circuit(),
        )

        Message1U1 = Message(
            1, b"Hello World!", b"", Circuit(), User1, User2Public, int(getTime())
        )  # Create a sample message
        # Initially, the message is not encrypted or signed. We encrypt for User 2 and sign as User 1.
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(
            1,
            Message1U1.content,
            Message1U1.signature,
            Circuit(),
            User1Public,
            User2,
            Message1U1.timeCreated,
            int(getTime()),
            True,
            True,
        )  # Simulate the message being sent to User 2
        self.assertTrue(
            Message1U2.verify(), "Verification failed."
        )  # Verify the signature
        Message1U2.decrypt()  # Decrypt the message
        self.assertEqual(Message1U2.content, b"Hello World!", "Decryption failed.")
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testMessageDBCounting(self):

        User1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.1",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test1.db"),
        )
        User1Public = PublicUser(
            1,
            "User1",
            [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
            Circuit(),
        )
        User2 = User(
            2,
            "User2",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.2",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test2.db"),
        )
        User2Public = PublicUser(
            2,
            "User2",
            [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
            Circuit(),
        )

        Message1U1 = Message(
            1,
            b"Hello World!",
            b"",
            Circuit(),
            User1,
            User2Public,
            int(getTime()),
            int(getTime()),
        )
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(
            2,
            Message1U1.content,
            Message1U1.signature,
            Circuit(),
            User1Public,
            User2,
            Message1U1.timeCreated,
            int(getTime()),
            True,
            True,
        )
        Message1U2.verify()
        Message1U2.decrypt()

        DB = MessagesDB("TestMessages.db")
        DB.addMessage(Message1U1)
        self.assertEqual(len(DB), 1, "Message 1 not being counted.")
        DB.addMessage(Message1U2)
        self.assertEqual(len(DB), 2, "Message 2 not being counted.")
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testMessageDBInsert(self):

        User1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.1",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test1.db"),
        )
        User1Public = PublicUser(
            1,
            "User1",
            [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
            Circuit(),
        )
        User2 = User(
            2,
            "User2",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.2",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test2.db"),
        )
        User2Public = PublicUser(
            2,
            "User2",
            [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
            Circuit(),
        )

        Message1U1 = Message(
            1, b"Hello World!", b"", Circuit(), User1, User2Public, int(getTime())
        )
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(
            2,
            Message1U1.content,
            Message1U1.signature,
            Circuit(),
            User1Public,
            User2,
            Message1U1.timeCreated,
            int(getTime()) + 10,
            True,
            True,
        )
        Message1U2.verify()
        Message1U2.decrypt()

        DB = MessagesDB("TestMessages.db")
        DB.addMessage(Message1U1)
        DB.addMessage(Message1U2)
        self.assertEqual(
            DB.getMessage(Message1U1.messageID, justContent=True),
            Message1U1.content.hex(),
            "Message 1 not being inserted.",
        )
        self.assertEqual(
            DB.getMessage(Message1U2.messageID, justContent=True),
            Message1U2.content.decode("utf-8"),
            "Message 2 not being inserted.",
        )
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testMessageDBDelete(self):

        User1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.1",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test1.db"),
        )
        User1Public = PublicUser(
            1,
            "User1",
            [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
            Circuit(),
        )
        User2 = User(
            2,
            "User2",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.2",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test2.db"),
        )
        User2Public = PublicUser(
            2,
            "User2",
            [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
            Circuit(),
        )

        Message1U1 = Message(
            1, b"Hello World!", b"", Circuit(), User1, User2Public, int(getTime())
        )
        Message1U1.encrypt()
        Message1U1.sign()

        Message1U2 = Message(
            2,
            Message1U1.content,
            Message1U1.signature,
            Circuit(),
            User1Public,
            User2,
            Message1U1.timeCreated,
            int(getTime()) + 10,
            True,
            True,
        )
        Message1U2.verify()
        Message1U2.decrypt()

        DB = MessagesDB("TestMessages.db")
        DB.addMessage(Message1U1)
        DB.addMessage(Message1U2)

        self.assertEqual(len(DB), 2, "Messages not being counted.")
        DB.deleteMessage(Message1U1.messageID)
        self.assertEqual(len(DB), 1, "Message 1 not being deleted.")
        DB.deleteMessage(Message1U2.messageID)
        self.assertEqual(len(DB), 0, "Message 2 not being deleted.")
        DB.deleteMessage(-1)
        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testNetworkMessageConvertion(self):

        User1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.1",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test1.db"),
        )
        User1Public = PublicUser(
            1,
            "User1",
            [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
            Circuit(),
        )
        User2 = User(
            2,
            "User2",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.2",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test2.db"),
        )
        User2Public = PublicUser(
            2,
            "User2",
            [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
            Circuit(),
        )

        User1.contacts.addContact(User2Public)
        User2.contacts.addContact(User1Public)

        msgU1 = User1.createMessageToSend("Hello World!", User2.userName)
        ntwMsgU1 = msgU1.toNetworkMessage()  # Transforms the message to NetworkMessage.
        asBytes = bytes(
            ntwMsgU1
        )  # Transforms the NetworkMessage to bytes and sends this bytes to User 2.

        ntwMsgU2 = loadNetworkMessage(
            asBytes
        )  # The User 2 receives the bytes and reads them.

        msgU2 = User2.createMessageToReceive(ntwMsgU2)

        self.assertEqual(
            b"Hello World!", msgU2.content, "Message content not being decrypted."
        )
        self.assertEqual(
            msgU1.timeCreated, msgU2.timeCreated, "Message time not being read."
        )
        self.assertEqual(
            msgU1.sender.userID, msgU2.sender.userID, "Message sender not being read."
        )
        self.assertEqual(
            msgU1.receiver.userID,
            msgU2.receiver.userID,
            "Message receiver not being read.",
        )
        self.assertEqual(
            msgU1.messageID, msgU2.messageID, "Message ID not being computed right."
        )

        for file in glob.glob("Test*.db"):
            os.remove(file)
        for file in glob.glob("Test*.pem"):
            os.remove(file)


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
        for file in glob.glob("Test*.json"):
            os.remove(file)


class RSATesting(unittest.TestCase):
    def testEncryptionDecryption1024(self):
        keys = RSAKeys(1024, fileName="TestKey")
        # Generate a random text
        text = ("".join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(
            keys.decrypt(cipher), text, "1024 Encryption/Decryption failed."
        )
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testSigningVerification1024(self):
        keys = RSAKeys(1024, fileName="TestKey")
        # Generate a random text
        text = ("".join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        signature = keys.sign(text)
        self.assertTrue(
            keys.verify(text, signature, keys.publicKey),
            "1024 Signing/Verification failed.",
        )
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testEncryptionDecryption2048(self):
        keys = RSAKeys(2048, fileName="TestKey")
        # Generate a random text
        text = ("".join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        cipher = keys.encrypt(text, keys.publicKey)
        self.assertEqual(
            keys.decrypt(cipher), text, "2048 Encryption/Decryption failed."
        )
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testSigningVerification2048(self):
        keys = RSAKeys(2048, fileName="TestKey")
        # Generate a random text
        text = ("".join([chr(random.randint(32, 126)) for _ in range(1000)])).encode()
        signature = keys.sign(text)
        self.assertTrue(
            keys.verify(text, signature, keys.publicKey),
            "2048 Signing/Verification failed.",
        )
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testImportExport(self):
        Keys1 = RSAKeys(fileName="TestKey")
        Keys2 = RSAKeys(fileName="TestKey", toImport=True)

        Keys1.exportKeys("TestKey")
        Keys2.importKeys("TestKey")

        self.assertTrue(Keys1 == Keys2, "Import/Export failed.")
        for file in glob.glob("Test*.pem"):
            os.remove(file)

    def testEncryptedImportExport(self):
        Keys1 = RSAKeys(fileName="TestKey")
        Keys2 = RSAKeys(fileName="TestKey", toImport=True)

        testPassword = "".join([chr(random.randint(32, 126)) for _ in range(15)])

        Keys1.exportKeys("TestKey", withPassword=testPassword)
        Keys2.importKeys("TestKey", withPassword=testPassword)

        self.assertTrue(Keys1 == Keys2, "Encrypted Import/Export failed.")
        for file in glob.glob("Test*.pem"):
            os.remove(file)


class DiffieHellmanTesting(unittest.TestCase):
    def testEncryptionDecryption(self):
        Alice = DiffieHellmanKey()
        Bob = DiffieHellmanKey()
        Alice.generateSharedKey(Bob.publicKey)
        Bob.generateSharedKey(Alice.publicKey)
        self.assertEqual(Alice.sharedKey, Bob.sharedKey, "Diffie-Hellman failed.")

    def testImportExport(self):
        key = DiffieHellmanKey()
        key.generateSharedKey(ec.generate_private_key(ec.SECP384R1()).public_key())
        key.exportDerivedKey("TestKey.dh")
        importedKey = importDerivedKey("TestKey.dh")
        self.assertEqual(key.derivedKey, importedKey, "Import/Export failed.")

        for file in glob.glob("Test*.dh"):
            os.remove(file)


class AESTesting(unittest.TestCase):
    def testEncryptionDecryption(self):
        key = os.urandom(32)
        nonce = os.urandom(8)
        message = urandom(1000)

        c1 = KeyAES(key, nonce)
        encMessage = c1.encrypt(message)

        c2 = KeyAES(key, nonce)
        decMessage = c2.decrypt(encMessage)

        self.assertEqual(message, decMessage, "AES Encryption/Decryption failed.")

    def testEncryptionDecryptionFunctions(self):
        key, nonce = os.urandom(32), os.urandom(8)
        message = "".join([chr(random.randint(32, 126)) for _ in range(100)])

        encMessage = encryptAES(message, key, nonce)
        decMessage = decryptAES(encMessage, key, nonce)

        self.assertEqual(message, decMessage, "AES Encryption/Decryption failed.")


class PacketsRoutingTesting(unittest.TestCase):
    def testPacking(self):
        User1 = User(
            1,
            "User1",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.1",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test1.db"),
        )
        User1Public = PublicUser(
            1,
            "User1",
            [User1.encryptionKeys.publicKey, User1.signingKeys.publicKey],
            Circuit(),
        )
        User2 = User(
            2,
            "User2",
            [RSAKeys(fileName="TestKey"), RSAKeys(fileName="TestKey")],
            "127.0.0.2",
            ForwardingTable(),
            Queue(),
            Contacts(),
            MessagesDB("Test2.db"),
        )
        User2Public = PublicUser(
            2,
            "User2",
            [User2.encryptionKeys.publicKey, User2.signingKeys.publicKey],
            Circuit(),
        )

        User1.contacts.addContact(User2Public)
        User2.contacts.addContact(User1Public)

        CIRCUIT = ["NodeA", "Node1", "Node2", "Node3"]

        msg1 = User1.createMessageToSend("Hello World!", User2.userName)
        networkMessage = createNetworkMessage(msg1)
        base64NetworkMessage = base64.b64encode(networkMessage).decode()
        routingPacket = createBlindOnionPackets(
            base64NetworkMessage, CIRCUIT, "CIRCUIT_ID"
        )
        routingPacket = createOnionPacketsJson(routingPacket)
        frontEndPacket = buildFrontEndPacket(routingPacket, msg1.messageID)

        receivedPacket = json.loads(frontEndPacket)["data"]
        receivedPacket = json.loads(receivedPacket)
        finalPacket = None
        for i in range(len(CIRCUIT)):
            if type(finalPacket) is str:
                break
            if (
                receivedPacket["fromNode"] == CIRCUIT[i]
                and receivedPacket["toNode"] == CIRCUIT[i + 1]
            ):
                finalPacket = receivedPacket["Data"]
                receivedPacket = receivedPacket["Data"]

        stringMessage = loadStringNetworkMessage(finalPacket)
        msg2 = User2.createMessageToReceive(stringMessage)

        self.assertEqual(msg1, msg2, "Packing/Unpacking failed.")


if __name__ == "__main__":
    unittest.main()
