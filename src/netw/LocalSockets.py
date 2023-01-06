from src.netw.Imports import *


import socket
import asyncio
import websockets


class WebSocketConnection:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.uri = f"ws://{self.host}:{self.port}"

    def startsend(self, data: str):
        # This method starts the connection and sends the data.
        async def send(self, data):
            async with websockets.connect(self.uri) as websocket:
                await websocket.send(data)
                await websocket.close()

        asyncio.run(send(self, data))

    def startreceive(self, toPipe: "multiprocessing.Pipe" = None):
        # This method starts the connections and listens for data in an infinite loop.

        async def receive(self, toPipe):
            async with websockets.connect(self.uri) as websocket:
                while True:
                    data = await websocket.recv()
                    if type(data) is not bytes:
                        data = data.encode()
                    toPipe.send(data)

        isConnected = False
        while not isConnected:
            try:
                asyncio.run(receive(self, toPipe))
            except ConnectionRefusedError:
                isConnected = False
            else:
                isConnected = True

    def close(self):
        # This method closes the connection.
        async def _close(self):
            async with websockets.connect(self.uri) as websocket:
                await websocket._close()

        asyncio.run(_close(self))

    def __str__(self) -> str:
        return f"WebSocket Connection to {self.uri}"

    def __repr__(self) -> str:
        return f"WebSocket Connection to {self.uri}"
