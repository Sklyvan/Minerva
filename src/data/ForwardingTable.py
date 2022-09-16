from src.netw.Circuit import *
import json

class ForwardingTable:
    def __init__(self):
        self.table = {}

    def addEntry(self, circuitID: str, node: Node):
        self.table[circuitID] = node

    def removeEntry(self, circuitID: str):
        self.table.pop(circuitID)

    def replaceEntry(self, circuitID: str, node: Node):
        self.addEntry(circuit, node)

    def asJSON(self):
        asDict = {}
        for circuitID, node in self.table.items():
            asDict[circuitID] = node.asJSON()
        return asDict

    def exportTable(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.asJSON()))

    def importTable(self, path: str):
        with open(path, "r") as f:
            table = json.loads(f.read())
        for circuitID, node in table.items():
            importedKey = DiffieHellmanKey()
            importedKey.derivedKey = base64.b64decode(node["DiffieHellmanKey"])
            self.addEntry(circuitID, Node(node["IP"], importedKey))

    def readTable(self, jsonContent: dict):
        for circuitID, node in jsonContent.items():
            importedKey = DiffieHellmanKey()
            importedKey.derivedKey = base64.b64decode(node["DiffieHellmanKey"])
            self.addEntry(circuitID, Node(node["IP"], importedKey))

    def __getitem__(self, circuitID: str) -> Node:
        return self.table[circuitID]

    def __contains__(self, circuitID: str) -> bool:
        return circuitID in self.table

    def __str__(self):
        return str(self.table)

    def __len__(self):
        return len(self.table)

    def __iter__(self):
        return iter(self.table)

    def __eq__(self, other: "ForwardingTable"):
        for circuitID, node in self.table.items():
            if self[circuitID] != other[circuitID]:
                return False
        return True
