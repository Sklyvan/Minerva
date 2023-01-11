import sys, os  # This libraries are required to be able to import the other modules

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from src.main.Imports import *
from src.netw.p2p import WebApp
from src.netw.LocalSockets import WebSocketConnection
from src.main.InitializeUser import *
from src.netw.p2p.MessagesListener import messagesListener

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
        "Data": base64.b64encode(networkMessage),
        "fromNode": fromNode,
        "toNode": toNode,
    }
    return str(internetPacket)


def buildFrontEndPacket(internetPacket: str, packetID: int) -> str:
    # This packet is sent to the Front-End.
    frontPacket = {
        "ID": str(packetID),
        "toSend": "true",
        "toReceive": "false",
        "data": internetPacket,
    }
    return str(frontPacket)


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
    # TODO: Here, we should wait for a confirmation of the P2P Node, then return True or False.

    return None


def receiveMessages():
    while True:
        if not RECEIVED_MESSAGES.empty():
            message = RECEIVED_MESSAGES.get()
            print(message)


def isUsed(checkPort):
    if not checkPort:
        return True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", checkPort)) == 0


def obtainPort():
    atPort = DEFAULT_PORT
    while isUsed(atPort):
        atPort = random.randint(8000, 9000)
    return atPort


def main():
    print(f"ROOT = {ROOT}")
    atPort = obtainPort()

    try:
        toRun = lambda: subprocess.call(openWebSocket, shell=True)
        PROCESSES.append(multiprocessing.Process(target=toRun))
        PROCESSES[-1].start()
        while not isUsed(6774):  # TODO: Do not use hardcoded port
            None
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] WebSocket Server Started")

    try:
        myUser, filePath = initializeUser(sys.argv)
        myPublicUser = PublicUser(
            myUser.userID,
            myUser.userName,
            [myUser.encryptionKeys.publicKey, myUser.signingKeys.publicKey],
            Circuit(),
        )
        myUser.contacts.addContact(myPublicUser)
        # myUser.exportUser(filePath)

        # Make a copy of the file at filePath but change the .json to .inst
        shutil.copyfile(filePath, filePath.replace(".json", ".inst"))
        # This file extension indicates the HTML that is going to be used to render the user's profile.

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
        webbrowser.open(openBrowser(atPort), new=2)
        None
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Browser Opened")

    time.sleep(3)
    sendMessage("Hello World!", myUser, myPublicUser, myUser.IP)
    receiveMessages()


if __name__ == "__main__":
    main()
