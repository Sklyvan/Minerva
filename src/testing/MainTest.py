import unittest
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


if __name__ == "__main__":
    unittest.main()
