import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT)

from src.main.Imports import *
from src.netw.p2p import WebApp
from src.main.InitializeUser import initializeUser
from src.netw.p2p.MessagesListener import messagesListener

comPipe = subprocess.Popen(["/bin/cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
threads = []


def readPipe():
    while True:
        inputPacket = comPipe.stdout.readline()
        if inputPacket != b"":
            print(inputPacket)


def isUsed(port):
    if not port:
        return True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


if __name__ == "__main__":
    print(f"ROOT = {ROOT}")
    try:
        t = threading.Thread(
            target=subprocess.call, args=(openWebSocket,), kwargs={"shell": True}
        )
        t.start()
        threads.append(t)
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
        t = threading.Thread(target=messagesListener, args=(comPipe,))
        t.start()
        threads.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Messages Listener Started")

    try:
        t = threading.Thread(target=readPipe)
        t.start()
        threads.append(t)
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
        threads.append(t)
    except Exception as e:
        raise e
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Web Server Started")
        webbrowser.open(openBrowser(atPort), new=2)

    # Wait for all the threads, if KeyboardInterrupt is pressed, then exit.
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        for t in threads[::-1]:
            t.exit()
        sys.exit(0)
