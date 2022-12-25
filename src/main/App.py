import subprocess
import threading
import sys

from src.main.InitializeUser import initializeUser
from src.netw.p2p.MessagesListener import start

if __name__ == "__main__":
    myUser = initializeUser(sys.argv)
    myPipe = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    threading.Thread(target=start, args=(myPipe,)).start()
