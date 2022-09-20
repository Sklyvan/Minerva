import base64
import os
import xml.etree.ElementTree as ET
from TransferJS import SocketConnection

class Packet:
    def __init__(self, withData: bytes, fromIP: str, toIP: str, xmlConfig="SocketsInformation.xml"):
        """
        This class does not contain any methods to send the packet, since it
        is only used to create the packet from Python, use the result of the
        toJSON() method to sent it to JavaScript. From JavaScript is sent
        using the WebRTC API.
        :param withData: Bytes to send, this can be anything.
        :param fromIP: IP of the sender.
        :param toIP: IP of the receiver.
        :param xmlConfig: XML file with the host and port of the socket.
        """
        self.data = withData
        self.fromIP = fromIP
        self.toIP = toIP
        self.host, self.port = self.readHostPort(xmlConfig)
        self.socketConnection = SocketConnection(self.host, self.port)

    def readHostPort(self, xmlConfig):
        tree = ET.parse(xmlConfig)
        root = tree.getroot()
        h = root.find("host").text
        p = int(root.find("port").text)
        return h, p

    def toJSON(self):
        return str({"Data": base64.b64encode(self.data), "fromIP": self.fromIP, "toIP": self.toIP})

    def toNetworkLayer(self):
        self.socketConnection.start()
        self.socketConnection.send(self.toJSON().encode())
        self.socketConnection.close()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return f"Packet with data {self.data} from {self.fromIP} to {self.toIP}."

    def __repr__(self):
        return f"Packet with data {self.data} from {self.fromIP} to {self.toIP}."

    def __iter__(self):
        return [("data", self.data), ("fromIP", self.fromIP), ("toIP", self.toIP)].__iter__()


myPacket = Packet(b"Hello World!", "127.0.0.1", "127.0.0.2")
myPacket.toNetworkLayer()
