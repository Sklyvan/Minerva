import subprocess
import sys, os
import threading

from src.main.InitializeUser import initializeUser
from src.netw.p2p.MessagesListener import messagesListener

emojiTick, emojiCross = "\u2705", "\u274C"
comPipe = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
threads = []


def readPipe():
    while True:
        inputPacket = comPipe.stdout.readline()
        if inputPacket != b"":
            print(inputPacket)


if __name__ == "__main__":
    # Run the $ node src/netw/openWebSocket.js command as a thread.
    t = threading.Thread(target=os.system, args=("node ../netw/openWebSocket.js",))
    t.start()
    threads.append(t)

    try:
        myUser = initializeUser(sys.argv)
    except Exception as e:
        print(f"[{emojiCross}] {e}")
        sys.exit(1)
    else:
        print(f"[{emojiTick}] User Initialized: {myUser.userName} | {myUser.IP}")

    try:
        t = threading.Thread(target=messagesListener, args=(comPipe,))
        t.start()
        threads.append(t)
    except Exception as e:
        print(f"[{emojiCross}] {e}")
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Messages Listener Started")

    try:
        t = threading.Thread(target=readPipe)
        t.start()
        threads.append(t)
    except Exception as e:
        print(f"[{emojiCross}] {e}")
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Pipe Reader Started")

    # Wait for all the threads, if KeyboardInterrupt is pressed, then exit.
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        for t in threads[::-1]:
            t.exit()
        sys.exit(0)
