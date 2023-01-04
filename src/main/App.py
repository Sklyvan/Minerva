import sys, os  # This libraries are required to be able to import the other modules

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from src.main.Imports import *
from src.netw.p2p import WebApp
from src.main.InitializeUser import initializeUser
from src.netw.p2p.MessagesListener import messagesListener

COMMUNICATION_PIPE = subprocess.Popen(
    ["/bin/cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
)
THREADS = []


def readPipe(readFrom, writeTo=None):
    while True:
        inputPacket = readFrom.stdout.readline()
        if inputPacket != b"":
            if writeTo:
                writeTo.append(inputPacket)
            else:
                print(inputPacket)


def readPipeIterable(readFrom, writeTo=None):
    while True:
        inputPacket = readFrom.stdout.readline()
        if inputPacket != b"":
            if writeTo:
                writeTo.append(inputPacket)
                yield inputPacket
            else:
                yield inputPacket


def isUsed(checkPort):
    if not checkPort:
        return True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", checkPort)) == 0


if __name__ == "__main__":
    print(f"ROOT = {ROOT}")
    try:
        t = threading.Thread(
            target=subprocess.call, args=(openWebSocket,), kwargs={"shell": True}
        )
        t.start()
        THREADS.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] WebSocket Server Started")

    try:
        myUser = initializeUser(sys.argv)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] User Initialized: {myUser.userName} | {myUser.IP}")

    try:
        t = threading.Thread(target=messagesListener, args=(COMMUNICATION_PIPE,))
        t.start()
        THREADS.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Messages Listener Started")

    try:
        t = threading.Thread(target=readPipe, args=(COMMUNICATION_PIPE,))
        t.start()
        THREADS.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Pipe Reader Started")

    try:
        atPort = DEFAULT_PORT
        while isUsed(atPort):
            atPort = random.randint(8000, 9000)
        t = threading.Thread(
            target=subprocess.call, args=(startServer(atPort),), kwargs={"shell": True}
        )
        t.start()
        THREADS.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Web Server Started")
        webbrowser.open(openBrowser(atPort), new=2)

    # Wait for all the threads, if KeyboardInterrupt is pressed, then exit.
    try:
        for t in THREADS:
            t.join()
    except KeyboardInterrupt:
        for t in THREADS[::-1]:
            t.exit()
        sys.exit(0)
