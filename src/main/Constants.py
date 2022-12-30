import os

emojiTick, emojiCross = "\u2705", "\u274C"

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

DB_PATH = os.path.join(os.path.dirname(FILE_DIR), "userdata")
KEYS_PATH = os.path.join(os.path.dirname(FILE_DIR), "userdata", "keys")
USER_PATH = os.path.join(os.path.dirname(FILE_DIR), "userdata")

DB_NAME = "Messages.db"
ENC_KEYS_NAME, SIG_KEYS_NAME = "EncKeys", "SigKeys"

openWebSocket = "node netw/openWebSocket.js"


def startServer(atPort: int):
    return f"python3 -m http.server {atPort}"


def openBrowser(atPort: int):
    return f"http://localhost:{atPort}/netw/p2p/p2pNode.html"
