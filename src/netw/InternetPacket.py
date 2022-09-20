import base64

class Packet:
    def __init__(self, withData: bytes, fromIP: str, toIP: str):
        self.data = withData
        self.fromIP = fromIP
        self.toIP = toIP

    def toJSON(self):
        return str({"Data": base64.encode(self.data), "fromIP": self.fromIP, "toIP": self.toIP})

    def __bytes__(self):
        return self.data

    def __str__(self):
        return f"Packet with data {self.data} from {self.fromIP} to {self.toIP}."

    def __repr__(self):
        return f"Packet with data {self.data} from {self.fromIP} to {self.toIP}."

    def __iter__(self):
        return [("data", self.data), ("fromIP", self.fromIP), ("toIP", self.toIP)].__iter__()
