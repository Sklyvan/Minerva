from src.netw.Imports import *
import defusedxml.ElementTree as elementTree
from src.netw.LocalSockets import WebSocketConnection


class Packet:
    def __init__(
        self,
        withData: bytes,
        fromIP: str,
        toIP: str,
        xmlConfig: str = XML_FILE_PATH,
    ):
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
        self.webSocketConnection = WebSocketConnection(self.host, self.port)

    def readHostPort(self, xmlConfig: str) -> (str, int):
        tree = elementTree.parse(xmlConfig)
        root = tree.getroot()
        h = root.find("host").text
        p = int(root.find("port").text)
        return h, p

    def toJSON(self) -> str:
        return str(
            {
                "Data": base64.b64encode(self.data),
                "fromIP": self.fromIP,
                "toIP": self.toIP,
            }
        )

    def toNetworkLayer(self):
        self.webSocketConnection.startsend(self.toJSON())

    def __bytes__(self) -> bytes:
        return self.data

    def __str__(self) -> str:
        return f"Packet with data {self.data} from {self.fromIP} to {self.toIP}."

    def __repr__(self) -> str:
        return f"Packet with data {self.data} from {self.fromIP} to {self.toIP}."

    def __iter__(self) -> iter:
        return [
            ("data", self.data),
            ("fromIP", self.fromIP),
            ("toIP", self.toIP),
        ].__iter__()


def cleanData(
    data: str,
) -> dict:  # This function is used to clean the data received from the network layer (JS).
    data = data.replace("{", "")
    data = data.replace("}", "")
    data = data.replace('"', "")
    data = data.replace("b'", "")
    data = data.replace("'", "")
    data = data.replace(" ", "")
    asArray = data.split(",")
    dictData = {}
    for i in range(len(asArray)):
        splitArray = asArray[i].split(":")
        # If splitArray[1] is a number, convert it to int
        if splitArray[1].isnumeric():
            splitArray[1] = int(splitArray[1])
        else:
            # The splitArray[1] is a Base64 string, transform it to decoded bytes.
            splitArray[1] = base64.b64decode(splitArray[1])

        dictData[splitArray[0]] = splitArray[1]

    return dictData
