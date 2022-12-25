import socket
import asyncio
import websockets

class WebSocketConnection:
    def __init__(self, host:str = '127.0.0.1', port:int = 6774):
        self.host = host
        self.port = port
        self.uri = f"ws://{self.host}:{self.port}"

    def startsend(self, data:str):
        # This method starts the connection and sends the data.
        async def send(self, data):
            async with websockets.connect(self.uri) as websocket:
                await websocket.send(data)
                await websocket.close()

        asyncio.run(send(self, data))

    def startreceive(self, toPipe:'subprocess.Popen' = None):
        # This method starts the connections and listens for data in an infinite loop.
        async def receive(self, toPipe):
            async with websockets.connect(self.uri) as websocket:
                while True:
                    data = await websocket.recv()
                    toPipe.stdin.write(data)

        asyncio.run(receive(self, toPipe))

    def __str__(self) -> str:
        return f"WebSocket Connection to {self.uri}"

    def __repr__(self) -> str:
        return f"WebSocket Connection to {self.uri}"
