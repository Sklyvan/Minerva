import sys, os  # This libraries are required to be able to import the other modules

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from src.main.Imports import *
from src.netw.p2p import WebApp
from src.netw.LocalSockets import WebSocketConnection
from src.main.InitializeUser import *
from src.netw.p2p.MessagesListener import messagesListener
from src.netw.BrowserEmulator import *

RECEIVED_MESSAGES = multiprocessing.Queue()
SOCKET = WebSocketConnection(RECEIVED_MESSAGES)
PROCESSES = []


def createNetworkMessage(fromMsg: Message) -> NetworkMessage:
    # networkMessage = {encyptedContent:..., signature:..., ...}
    networkMessage = fromMsg.toNetworkMessage()

    networkMessage = networkMessage.asJSON()  # Convert to a JSON string.
    networkMessage = networkMessage.encode()  # Encode to send the JSON string as bytes.

    return networkMessage


def buildInternetPacket(networkMessage: str, fromNode: str, toNode: str) -> str:
    # This packet is the one that is going to be sent through internet.
    internetPacket = {
        "Data": base64.b64encode(networkMessage).decode(),
        "fromNode": fromNode,
        "toNode": toNode,
    }
    return json.dumps(internetPacket)


def buildFrontEndPacket(internetPacket: str, packetID: int) -> str:
    # This packet is sent to the Front-End.
    frontPacket = {
        "ID": packetID,
        "toSend": True,
        "toReceive": False,
        "data": internetPacket,
    }
    return json.dumps(frontPacket)


def sendMessage(
    messageContent: str,
    messageSender: User,
    messageReceiver: PublicUser,
    receiverIP: str,  # TODO: This should be not used because Blind Onion Routing avoids knowing the other's IP.
):
    msg = messageSender.createMessageToSend(messageContent, messageReceiver.userName)
    networkMessage = createNetworkMessage(msg)
    internetPacket = buildInternetPacket(networkMessage, messageSender.IP, receiverIP)
    frontEndPacket = buildFrontEndPacket(internetPacket, msg.messageID)

    SOCKET.send(frontEndPacket)

    return None


def receiveMessages(forUser: User):
    threading.Thread(target=SOCKET.receive).start()
    while True:
        if not RECEIVED_MESSAGES.empty():
            message = RECEIVED_MESSAGES.get()
            parsedMessage = json.loads(message)
            if parsedMessage["toReceive"]:
                parsedData = json.loads(parsedMessage["data"])
                if parsedData["toNode"] == forUser.IP:
                    msg = forUser.createMessageToReceive(
                        loadStringNetworkMessage(parsedData["Data"])
                    )
                    yield msg


def isUsed(checkPort):
    if not checkPort:
        return True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOSTNAME, checkPort)) == 0


def obtainPort():
    atPort = DEFAULT_PORT
    while isUsed(atPort):
        atPort = random.randint(
            ALTERNATIVE_PORTS_RANGE.start, ALTERNATIVE_PORTS_RANGE.stop
        )
    return atPort


def main(
    userName: str, userKey: str = None, loadUser: bool = False, createUser: bool = False
):
    print(f"ROOT = {ROOT}")
    atPort = obtainPort()

    try:
        toRun = lambda: subprocess.call(openWebSocket, shell=True)
        PROCESSES.append(multiprocessing.Process(target=toRun))
        PROCESSES[-1].start()
        while not isUsed(PORT):
            None
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] WebSocket Server Started")

    try:
        myUser, filePath = initializeUser(
            userName, userKey, loadUser=loadUser, newUser=createUser
        )

        # Make a copy of the file at filePath but change the name from UserName.json to tempUserFile.inst
        tempFilePath = filePath.replace(
            USERFILE_NAME + myUser.userName + "." + USERFILE_EXTENSION,
            TEMPUSERFILE_NAME + "." + TEMPUSERFILE_EXTENSION,
        )
        with open(tempFilePath, "w") as f:
            json.dump({"IP": myUser.IP}, f)

    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] User Initialized: {myUser.userName} | {myUser.IP}")

    try:
        toRun = lambda: subprocess.call(startServer(atPort), shell=True)
        PROCESSES.append(multiprocessing.Process(target=toRun))
        PROCESSES[-1].start()
        while not isUsed(atPort):
            None
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Web Server Started")

    try:
        browserEmulator = BrowserEmulator(USE_WEB_BROWSER, openBrowser(atPort))
        browserEmulator.startDriver()
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Browser Opened")

    return myUser, browserEmulator
