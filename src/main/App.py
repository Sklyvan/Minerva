import sys, os  # This libraries are required to be able to import the other modules

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from src.main.Imports import *
from src.netw.p2p import WebApp
from src.main.InitializeUser import *
from src.netw.p2p.MessagesListener import messagesListener

RECEIVED_MESSAGES = multiprocessing.Queue()


def readPipe(readFrom: multiprocessing.Queue, writeTo=None):
    while True:
        if not readFrom.empty():
            data = readFrom.get()
            if data != b"":
                if writeTo is not None:
                    writeTo.append(data)
                else:
                    print(data)


def readPipeIterable(readFrom: multiprocessing.Queue, writeTo=None):
    while True:
        if not readFrom.empty():
            data = readFrom.get()
            if data != b"":
                if writeTo:
                    writeTo.append(data)
                else:
                    print(data)
                yield data


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
        myUser, filePath = initializeUser(sys.argv)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] User Initialized: {myUser.userName} | {myUser.IP}")

    try:
        toRun = lambda: subprocess.call(startServer(atPort), shell=True)
        threading.Thread(target=toRun).start()
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Web Server Started")

    try:
        webbrowser.open(openBrowser(atPort), new=2)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Browser Opened")

    try:
        toRun = lambda: subprocess.call(openWebSocket, shell=True)
        threading.Thread(target=toRun).start()
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] WebSocket Server Started")

    try:
        toRun = lambda: messagesListener(RECEIVED_MESSAGES)
        threading.Thread(target=toRun).start()
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Messages Listener Started")

    try:
        toRun = lambda: readPipe(RECEIVED_MESSAGES)
        threading.Thread(target=toRun).start()
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Pipe Reader Started")


if __name__ == "__main__":
    main()
