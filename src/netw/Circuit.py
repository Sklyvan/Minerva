from src.netw.Imports import *


class Node:
    def __init__(self, nodeIP: str, key: DiffieHellmanKey):
        self.nodeIP = nodeIP
        self.key = key

    def isOnline(self) -> bool:
        """
        This method checks if the node is online or not.
        The system pings the nodeIP to check if it is online.
        :return: True/False
        """
        raise NotImplementedError("This method is not implemented yet.")

    def checkKey(self) -> bool:
        return self.key.derivedKey is not None

    def exportNode(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.asJSON()))

    def importNode(self, path: str):
        with open(path, "r") as f:
            node = json.loads(f.read())
        importedKey = DiffieHellmanKey()
        importedKey.derivedKey = base64.b64decode(node["DiffieHellmanKey"])
        self.nodeIP = node["IP"]
        self.key = importedKey

    def __str__(self) -> str:
        return f"Node {self.nodeIP}"

    def __eq__(self, other: "Node") -> bool:
        return self.nodeIP == other.nodeIP and self.key == other.key

    def asJSON(self) -> dict:
        asDict = {"IP": str(self.nodeIP), "DiffieHellmanKey": repr(self.key)}
        return asDict


class Circuit:
    def __init__(self, circuitID: str = "", nodes: [Node] = []):
        self.circuitID = circuitID
        self.nodes = nodes
        self.size = len(nodes)

    def addNode(self, node: Node):
        self.nodes.append(node)
        self.size += 1

    def removeNode(self, node: Node):
        self.nodes.remove(node)
        self.size -= 1

    def isOnline(self) -> bool:
        return all((node.isOnline() for node in self.nodes))

    def checkKeys(self) -> bool:
        return all((node.checkKey() for node in self.nodes))

    def exportCircuit(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.asJSON()))

    def importCircuit(self, path: str):
        with open(path, "r") as f:
            circuit = json.loads(f.read())
        self.circuitID = circuit["ID"]
        self.size = 0
        for node in circuit["Nodes"]:
            importedKey = DiffieHellmanKey()
            importedKey.derivedKey = base64.b64decode(node["DiffieHellmanKey"])
            self.nodes.append(Node(node["IP"], importedKey))
            self.size += 1

    def __len__(self) -> int:
        return self.size

    def __eq__(self, other: "Circuit") -> bool:
        for i in range(len(self)):
            if self.nodes[i] != other.nodes[i]:
                return False
        return True

    def __str__(self) -> str:
        return f"Circuit {self.circuitID} with {self.size} nodes."

    def __iter__(self) -> iter:
        return iter(self.nodes)

    def __getitem__(self, index: int) -> Node:
        return self.nodes[index]

    def __setitem__(self, index: int, value: Node):
        self.nodes[index] = value

    def __delitem__(self, index: int):
        del self.nodes[index]
        self.size -= 1

    def __contains__(self, item: Node) -> bool:
        return item in self.nodes

    def __reversed__(self) -> list:
        return reversed(self.nodes)

    def __eq__(self, other: "Circuit") -> bool:
        sameID = self.circuitID == other.circuitID
        sameSize = self.size == other.size
        sameNodes = all((self.nodes[i] == other.nodes[i] for i in range(self.size)))
        return sameID and sameSize and sameNodes

    def asJSON(self) -> dict:
        asDict = {
            "ID": str(self.circuitID),
            "Nodes": [node.asJSON() for node in self.nodes],
        }
        return asDict

    def readCircuit(self, data: dict):
        self.circuitID = data["ID"]
        self.size = 0
        for node in data["Nodes"]:
            importedKey = DiffieHellmanKey()
            importedKey.derivedKey = base64.b64decode(node["DiffieHellmanKey"])
            self.nodes.append(Node(node["IP"], importedKey))
            self.size += 1
