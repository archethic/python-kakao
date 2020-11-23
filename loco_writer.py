class LocoWriter:
    def __init__(self, s, crypto):
        self.s = s
        self.crypto = crypto

    def sendPacket(self, packet):
        self.s.sendall(packet.toEncryptedLocoPacket(self.crypto))
