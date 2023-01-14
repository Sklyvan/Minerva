import os
from src.netw.Constants import *

emojiTick, emojiCross = "\u2705", "\u274C"

DEFAULT_PORT = 8000
ALTERNATIVE_PORTS_RANGE = range(DEFAULT_PORT, DEFAULT_PORT + 1000)

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

DB_PATH = os.path.join(os.path.dirname(FILE_DIR), "userdata")
KEYS_PATH = os.path.join(os.path.dirname(FILE_DIR), "userdata", "keys")
USER_PATH = os.path.join(os.path.dirname(FILE_DIR), "userdata")

DB_NAME, DB_EXTENSION = "Messages", "db"
ENC_KEYS_NAME, SIG_KEYS_NAME = "EncKeys", "SigKeys"
USERFILE_NAME, USERFILE_EXTENSION = "User", "json"
TEMPUSERFILE_NAME, TEMPUSERFILE_EXTENSION = "tempUserFile", "inst"

NODEJS_PATH = "/usr/bin/node"
NODEJS_SERVER_PATH = "netw/Communicator.js"
P2P_HTML_PATH = "/netw/p2p/p2pNode.html"
nodeWebSocket = os.path.join((os.path.dirname(FILE_DIR)), NODEJS_SERVER_PATH)
openWebSocket = f"{NODEJS_PATH} {nodeWebSocket}"

USE_WEB_BROWSER = "Firefox"


def startServer(atPort: int):
    return f"python3 -m http.server {atPort} | cat > /dev/null"


def openBrowser(atPort: int):
    return f"http://{HOSTNAME}:{atPort}{P2P_HTML_PATH}"
