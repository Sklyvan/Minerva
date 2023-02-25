import os

from src.netw.bor.Imports import *


def createBlindOnionPacket(
    fromNode: str, toNode: str, data: str, circuitID: str = None
) -> dict:
    """
    Creates an onion packet with the given data, from_node, and to_node.
    :param fromNode: The ID of the node that is sending the packet.
    :param toNode: The ID of the node that the packet is being sent to.
    :param data: The message data to be included in the packet.
    :param circuitID: The circuit ID to be included in the final packet. This is only used in the final packet.
    :return: A dictionary representing the onion packet.
    """
    if not circuitID:  # Compute a random SHA-256 output.
        circuitID = hashlib.sha256(os.urandom(32)).hexdigest().upper()

    return {
        "fromNode": fromNode,
        "toNode": toNode,
        "Data": data,
        "circuitID": circuitID,
    }


def createBlindOnionPackets(message: str, circuitNodes: list, circuitID: str) -> dict:
    """
    Creates a list of onion packets for the given message, network identifiers, and circuit ID.
    The packets are encapsulated in the reverse order of the circuitNodes list.
    :param message: The message data to be included in the packets.
    :param circuitNodes: A list of network identifiers representing the nodes in the circuit.
    :param circuitID: The circuit ID to be included in the final packet.
    :return: A dictionary representing the onion packet.
    """
    sendData = message
    for i in reversed(range(1, len(circuitNodes))):
        if i == len(circuitNodes) - 1:
            sendData = createBlindOnionPacket(
                circuitNodes[i - 1], circuitNodes[i], sendData, circuitID
            )
        else:
            sendData = createBlindOnionPacket(
                circuitNodes[i - 1], circuitNodes[i], sendData
            )
    return sendData


def createOnionPacketsJson(packets: list) -> str:
    """
    Creates a JSON string from the given list of onion packet dictionaries.
    :param packets: A list of dictionaries representing onion packets.
    :return: A JSON string representing the onion packets.
    """
    return json.dumps(packets)
