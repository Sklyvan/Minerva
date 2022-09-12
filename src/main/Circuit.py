from src.SystemExceptions import *
from src.cryp.DiffieHellmanKey import *

class Node:
    def __init__(self, nodeIP: str, key: DiffieHellmanKey):
        self.nodeIP = nodeIP
        self.key = key

    def isOnline(self) -> bool:
        raise NotImplementedError("This method is not implemented yet.")

    def checkKey(self) -> bool:
        raise NotImplementedError("This method is not implemented yet.")

    def exportNode(self, path: str):
        raise NotImplementedError("This method is not implemented yet.")

    def importNode(self, path: str):
        raise NotImplementedError("This method is not implemented yet.")

    def __str__(self):
        return f"Node {self.nodeIP}"

    def __eq__(self, other: "Node"):
        return self.nodeIP == other.nodeIP


class Circuit:
    def __init__(self, circuitID: str, nodes: [Node] = []):
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
        raise NotImplementedError("This method is not implemented yet.")

    def exportCircuit(self, path: str):
        raise NotImplementedError("This method is not implemented yet.")

    def importCircuit(self, path: str):
        raise NotImplementedError("This method is not implemented yet.")

    def __len__(self):
        return self.size

    def __eq__(self, other: "Circuit"):
        for i in range(len(self)):
            if self.nodes[i] != other.nodes[i]:
                return False
        return True

    def __str__(self):
        return f"Circuit {self.circuitID} with {self.size} nodes."

    def __iter__(self):
        return iter(self.nodes)

    def __getitem__(self, index: int):
        return self.nodes[index]

    def __setitem__(self, index: int, value: Node):
        self.nodes[index] = value

    def __delitem__(self, index: int):
        del self.nodes[index]
        self.size -= 1

    def __contains__(self, item: Node):
        return item in self.nodes

    def __reversed__(self):
        return reversed(self.nodes)
