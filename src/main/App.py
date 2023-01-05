import sys, os  # This libraries are required to be able to import the other modules

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from src.main.Imports import *
from src.netw.p2p import WebApp
from src.main.InitializeUser import initializeUser
from src.netw.p2p.MessagesListener import messagesListener

RECEIVED_MESSAGES = multiprocessing.Queue()
THREADS = []


def readPipe(readFrom: multiprocessing.Queue, writeTo=None):
    while True:
        if not readFrom.empty():
            data = readFrom.get()
            if data != b"":
                if writeTo:
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


def main():
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
        t = threading.Thread(target=messagesListener, args=(RECEIVED_MESSAGES,))
        t.start()
        THREADS.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Messages Listener Started")

    try:
        t = threading.Thread(target=readPipe, args=(RECEIVED_MESSAGES,))
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
        None
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
