from src.netw.LocalSockets import WebSocketConnection
from src.netw.InternetPacket import cleanData
import threading, base64, subprocess


def messagesListener(outputPipe: subprocess.Popen):
    inputPipe = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    receiver = WebSocketConnection()  # In this WebSocket, we will receive the data.

    threading.Thread(target=receiver.startreceive, args=(inputPipe,)).start()

    # Read the data from the inputPipe and send it to the outputPipe.
    while True:
        data = inputPipe.stdout.readline()
        data = cleanData(data)
        outputPipe.stdin.write(data)
