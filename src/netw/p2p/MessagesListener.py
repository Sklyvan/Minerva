from src.netw.LocalSockets import WebSocketConnection
from src.netw.InternetPacket import cleanData
import threading, base64

def start(pipe):
    readingQueue = []
    receiver = WebSocketConnection() # In this WebSocket, we will receive the data.
    threading.Thread(target=receiver.startreceive, args=(readingQueue,)).start()

    while True:
        if len(readingQueue) > 0:
            # Base64 decode the data.
            data = base64.b64decode(readingQueue.pop(0)).decode()
            cleanData = cleanData(data) # This data can be used by the User.createMessageToReceive() method.

            # Send the data to the pipe.
            pipe.stdin.write(cleanData)