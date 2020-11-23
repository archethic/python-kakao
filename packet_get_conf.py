class PacketGetConfReq:
    def __init__(self, os = "win32", model = "", MCCMNC = "999"):
        self.os = os
        self.model = model
        self.MCCMNC = MCCMNC

    def PacketName(self):
        return "GETCONF"

    def toBodyJson(self):
        return {
            "MCCMNC": self.MCCMNC,
            "os": self.os,
            "model": self.model
        }

