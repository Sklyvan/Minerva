import unittest
from src.main.User import *
import glob, os

class UserTest(unittest.TestCase):
    def testImportExportData(self):
        MyUser1 = User(1, "MyUser", [RSAKeys(fileName='EncKeys'), RSAKeys(fileName='SigKeys')],
                       "127.0.0.1", 'None', 'None', 'None', MessagesDB('Messages.db'))

        MyUser1.exportUser('User.json')

        MyUser2 = User(None, None, [None, None], None)
        MyUser2.importUser('User.json')

        self.assertEqual(MyUser1, MyUser2)

        for file in glob.glob("*.pem"): os.remove(file)
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.json"): os.remove(file)

    def testImportExportKeys(self):
        MyUser1 = User(1, 'User1', [RSAKeys(fileName='EncKeys'), RSAKeys(fileName='SigKeys')], "127.0.0.1")
        MyUser1.exportKeys('EncKeys.pem', 'SigKeys.pem')

        MyUser2 = User(2, 'User2', [RSAKeys(fileName='TempE', toImport=True), RSAKeys(fileName='TempS', toImport=True)], "127.0.0.2")
        MyUser2.importKeys('EncKeys.pem', 'SigKeys.pem')

        self.assertEqual(MyUser1.encryptionKeys, MyUser2.encryptionKeys, "Encryption keys are not equal.")
        self.assertEqual(MyUser1.signingKeys, MyUser2.signingKeys, "Signing keys are not equal.")
        self.assertTrue(MyUser1.checkKeys(), "Keys 1 are not valid.")
        self.assertTrue(MyUser2.checkKeys(), "Keys 2 are not valid.")

        for file in glob.glob("*.pem"): os.remove(file)
        for file in glob.glob("*.db"): os.remove(file)
        for file in glob.glob("*.json"): os.remove(file)


class NodeTest(unittest.TestCase):
    def testImportExportNode(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)
        N2 = Node("127.0.0.2", K2)

        N1.exportNode('Node.json')
        N2.importNode('Node.json')

        self.assertEqual(N1, N2)

        for file in glob.glob("*.json"): os.remove(file)

    def testNodeAsJSON(self):
        K1 = DiffieHellmanKey()
        K2 = DiffieHellmanKey()

        K1.generateSharedKey(K2.publicKey)
        K2.generateSharedKey(K1.publicKey)

        N1 = Node("127.0.0.1", K1)

        self.assertEqual(N1.asJSON(), {'IP': '127.0.0.1', 'DiffieHellmanKey': repr(K1)})

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

        MyCircuit1.exportCircuit("Circuit.json")
        MyCircuit2.importCircuit("Circuit.json")

        self.assertEqual(MyCircuit1, MyCircuit2)

        for file in glob.glob("*.json"): os.remove(file)

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

        self.assertEqual(MyCircuit.asJSON(), {
            "ID": "Circuit",
            "Nodes": [N1.asJSON(), N2.asJSON()]
        })

        for file in glob.glob("*.json"): os.remove(file)

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

        ExampleTable.exportTable("Test.json")

        ExampleTable2 = ForwardingTable()
        ExampleTable2.importTable("Test.json")

        self.assertEqual(ExampleTable, ExampleTable2)

        for file in glob.glob("*.json"): os.remove(file)

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

        self.assertEqual(ExampleTable.asJSON(), {
            "CIRCUIT1": N1.asJSON(),
            "CIRCUIT2": N2.asJSON()
        })


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

        self.assertEqual(ExampleTable.table, {
            "CIRCUIT1": N1,
            "CIRCUIT2": N2
        })

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


if __name__ == '__main__':
    unittest.main()
