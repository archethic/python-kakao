import crypto_Manager
import packet_check_in
import loco_packet
from socket import socket
import io
from bson import BSON as bson
import struct

def getCheckinData(host: str, port: int):
    reqData = packet_check_in.PacketCheckInReq()
    crypto = crypto_Manager.CryptoManager()

    sock = socket()
    sock.connect((host, port))

    handshakePacket = crypto.getHandshakePacket()
    sock.send(handshakePacket)

    p = loco_packet.Packet(1, 0, reqData.PacketName(), 0, bson.encode(reqData.toBodyJson()))

    sock.send(p.toEncryptedLocoPacket(crypto))

    data = sock.recv(2048)

    recvPacket = loco_packet.Packet()
    recvPacket.readEncryptedLocoPacket(data, crypto)

    return recvPacket


