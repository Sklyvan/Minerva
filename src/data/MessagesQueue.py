from src.data.Imports import *

class Queue:
    def __init__(self):
        """
        This class represents a queue of messages to be sent. The queue stores
        the messages IDs, not the messages themselves. The messages are stored
        in the SQLite database. The reason for this is that when the queue is
        exported as JSON, we don't export the messages content.
        """
        self.queue, self.size = [], 0
        self.creationTime = int(time.time()) # UNIX Timestamp
        self.lastAccessTime = int(time.time()) # UNIX Timestamp

    def addMessage(self, messageID):
        self.queue.append(messageID)
        self.size += 1
        self.lastAccessTime = int(time.time())

    def nextMessage(self) -> str:
        if self.size > 0:
            self.size -= 1
            self.lastAccessTime = int(time.time())
            return self.queue.pop(0)
        else:
            return None

    def asJSON(self):
        asDict = {"CreationTime": self.creationTime,
                  "LastAccessTime": self.lastAccessTime,
                  "Size": self.size,
                  "Queue": [msgID for msgID in self.queue]}
        return asDict

    def exportQueue(self, path: str):
        with open(path, "w") as f:
            f.write(json.dumps(self.asJSON()))

    def importQueue(self, path: str):
        with open(path, "r") as f:
            queue = json.loads(f.read())
        self.creationTime = queue["CreationTime"]
        self.lastAccessTime = queue["LastAccessTime"]
        self.size = queue["Size"]
        self.queue = queue["Queue"]

    def readQueue(self, jsonContent: dict):
        self.creationTime = jsonContent["CreationTime"]
        self.lastAccessTime = jsonContent["LastAccessTime"]
        self.size = jsonContent["Size"]
        self.queue = jsonContent["Queue"]

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.queue)

    def __getitem__(self, index):
        # WARNING: This method does not remove the message from the queue
        return self.queue[index]

    def __eq__(self, other: "Queue"):
        return self.queue == other.queue

    def __str__(self):
        return str(self.queue)
