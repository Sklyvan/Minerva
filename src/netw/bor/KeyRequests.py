from src.netw.bor.Imports import *


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
        "publicPart": publicKey.public_bytes(
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
        ).decode(),
    }
    return json.dumps(keyRequest)


def createDiffieHellmanKey(publicPart: str) -> "EllipticCurvePublicKey":
    """
    Creates a Diffie-Hellman key from the public part of the key.
    :param publicPart: The public part of the Diffie-Hellman key, encoded in PEM.
    :return: The Diffie-Hellman key.
    """
    return serialization.load_pem_public_key(publicPart.encode())
