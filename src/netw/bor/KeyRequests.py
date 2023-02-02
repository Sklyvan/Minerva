import json


def createDiffieHellmanRequest(
    toNodeID: str, fromNodeID: str, publicKey: "EllipticCurvePublicKey"
) -> str:
    """
    Creates the JSON string that represents a request to perform a Diffie-Hellman key exchange.
    This request is sent through the internet with WebRTC and received by another node, using P2P mechanisms.
    There is no need to protect the Network ID, because the receiver does not know our Social ID.
    :param toNodeID: WebRTC identifier of the node that will receive the request.
    :param fromNodeID: WebRTC identifier of the node that is sending the request.
    :param publicKey: The public part of the Diffie-Hellman key, encoded in hexadecimal.
    :return: The JSON string that represents the request.
    """
    keyRequest = {
        "toNode": toNodeID,
        "fromNode": fromNodeID,
        "keyRequest": "DiffieHellman",
        "publicPart": publicKey.public_numbers().encode_point().hex(),
    }
    return json.dumps(keyRequest)
