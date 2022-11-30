import socket
import asyncio
import websockets

class WebSocketConnection:
    def __init__(self, host='127.0.0.1', port=6774):
        self.host = host
        self.port = port
        self.uri = f"ws://{self.host}:{self.port}"

    def startsend(self, data):
        # This method starts the connection and sends the data.
        async def send(self, data):
            async with websockets.connect(self.uri) as websocket:
                await websocket.send(data)
                await websocket.close()

        asyncio.run(send(self, data))

    def startreceive(self, storeTo):
        # This method starts the connections and listens for data in an infinite loop.
        async def receive(self, storeTo):
            async with websockets.connect(self.uri) as websocket:
                while True:
                    data = await websocket.recv()
                    storeTo.append(data)

        asyncio.run(receive(self, storeTo))

    def startreceive_(self, storeTo):
        # This method starts the connections and listens for data in an infinite loop.
        async def receive(self, storeTo):
            async with websockets.connect(self.uri) as websocket:
                data = await websocket.recv()
                storeTo.append(data)
                return data

        asyncio.run(receive(self, storeTo))

    def __str__(self):
        return f"WebSocket Connection to {self.uri}"

    def __repr__(self):
        return f"WebSocket Connection to {self.uri}"
