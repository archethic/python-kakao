import packet_get_conf
import loco_packet
import ssl
import socket
from bson import BSON as bson

def getBookingData():
    reqData = packet_get_conf.PacketGetConfReq()
    context = ssl.create_default_context()
    
    with socket.create_connection(("booking-loco.kakao.com", 443)) as sock:
        with context.wrap_socket(sock, server_hostname = "booking-loco.kakao.com") as ssock:
            b = loco_packet.Packet(1000, 0, reqData.PacketName(), 0, bson.encode(reqData.toBodyJson()))
            ssock.write(b.toLocoPacket())
            data = ssock.recv(4096)
            recvPacket = loco_packet.Packet()
            recvPacket.readLocoPacket(data)
            return recvPacket
