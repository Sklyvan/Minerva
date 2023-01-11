import asyncio
import websockets
import multiprocessing

from src.netw.Imports import *


class WebSocketConnection:
    def __init__(
        self, dataQueue: "multiprocessing.Queue", host: str = HOST, port: int = PORT
    ):
        self.dataQueue = dataQueue
        self.host, self.port = host, port
        self.uri = f"ws://{self.host}:{self.port}"
        self.readData = True

    def start(self):
        self.readData = True
        multiprocessing.Process(target=self.receive).start()

    def stop(self):
        self.readData = False

    def receive(self):
        async def receive():
            async with websockets.connect(self.uri) as websocket:
                while self.readData:
                    data = await websocket.recv()
                    self.dataQueue.put(data)

        asyncio.run(receive())

    def send(self, data):
        async def send():
            async with websockets.connect(self.uri) as websocket:
                await websocket.send(data)

        asyncio.run(send())

    def __str__(self) -> str:
        return f"WebSocket Connection to {self.uri}"

    def __repr__(self) -> str:
        return f"WebSocket Connection to {self.uri}"
