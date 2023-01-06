from src.netw.LocalSockets import WebSocketConnection
from src.netw.InternetPacket import cleanData
import threading, multiprocessing


def messagesListener(receivedMessages: multiprocessing.Queue):
    receiverPipe, senderPipe = multiprocessing.Pipe()
    receiver = WebSocketConnection()  # In this WebSocket, we will receive the data.

    threading.Thread(target=receiver.startreceive, args=(senderPipe,)).start()

    # Read the data from the WebSocket Thread and put it in the queue.
    while True:
        data = receiverPipe.recv().decode()
        data = cleanData(data)
        receivedMessages.put(data)
