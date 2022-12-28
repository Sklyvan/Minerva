import subprocess
import sys
import threading

from src.main.InitializeUser import initializeUser
from src.netw.p2p.MessagesListener import messagesListener

emojiTick, emojiCross = "\u2705", "\u274C"
comPipe = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def readPipe():
    while True:
        inputPacket = comPipe.stdout.readline()
        print(inputPacket)


if __name__ == "__main__":
    try:
        myUser = initializeUser(sys.argv)
    except Exception as e:
        print(f"[{emojiCross}] {e}")
        sys.exit(1)
    else:
        print(f"[{emojiTick}] User Initialized")

    try:
        threading.Thread(target=messagesListener, args=(comPipe,)).start()
    except Exception as e:
        print(f"[{emojiCross}] {e}")
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Messages Listener Started")

    try:
        threading.Thread(target=readPipe).start()
    except Exception as e:
        print(f"[{emojiCross}] {e}")
        sys.exit(1)
    else:
        print(f"[{emojiTick}] Pipe Reader Started")
