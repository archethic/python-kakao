import get_booking
import get_checkin
import kakaoTalk_api
import socket
import loco_packet
import packet_login_list
import crypto_Manager
import time
import threading
import loco_writer
from bson import BSON as bson
import struct
import json

class Client:
    def __init__(self, device_name, device_uuid):
        self.device_name = device_name
        self.device_uuid = device_uuid

        self.__processingBuffer = b""
        self.__processingHeader = b""
        self.__processingSize = 0

    def connect(self):
        bookingData = get_booking.getBookingData().toJsonBody()
        checkInData = get_checkin.getCheckinData(bookingData["ticket"]["lsl"][0], bookingData["wifi"]["ports"][0]).toJsonBody()
        reqData = packet_login_list.PacketLoginListReq(kakaoTalk_api.KakaoTalk["Version"], "1", "win32", "ko", self.device_uuid, self.__accessKey)
        self.__crypto = crypto_Manager.CryptoManager()
        LoginListPacket = loco_packet.Packet(0, 0, reqData.PacketName(), 0, bson.encode(reqData.toBodyJson()))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((checkInData["host"], int(checkInData["port"])))
        self.writer = loco_writer.LocoWriter(self.s, self.__crypto)
        self.s.sendall(self.__crypto.getHandshakePacket())
        self.writer.sendPacket(LoginListPacket)
        self.pingThread = threading.Thread(target=self.ping)
        self.pingThread.start()
        self.__recvPacket()
        
    def ping(self):
        while True:
            time.sleep(180)
            PingPacket = loco_packet.Packet(0, 0, "PING", 0, bson.encode({}))
            self.s.sendall(PingPacket.toEncryptedLocoPacket(self.__crypto))

    def __recvPacket(self):
        encryptedBuffer = b""
        currentPacketSize = 0

        while True:
            if not self.s:
                exit()
                
            recv = self.s.recv(256)
                
            if not recv:
                print(recv)
                self.s.close()
                exit()

            encryptedBuffer += recv

            if not currentPacketSize and len(encryptedBuffer) >= 4:
                currentPacketSize = struct.unpack("<I", encryptedBuffer[0:4])[0]

            if currentPacketSize:
                encryptedPacketSize = currentPacketSize+4

                if len(encryptedBuffer) >= encryptedPacketSize:
                    self.__processingPacket(encryptedBuffer[0:encryptedPacketSize])
                    encryptedBuffer = encryptedBuffer[encryptedPacketSize:]
                    currentPacketSize = 0

    def __processingPacket(self, encryptedPacket):
        encLen = encryptedPacket[0:4]
        IV = encryptedPacket[4:20]
        BODY = encryptedPacket[20:]

        self.__processingBuffer += self.__crypto.aesDecrypt(BODY, IV)

        if not self.__processingHeader and len(self.__processingBuffer) >= 22:
            self.__processingHeader = self.__processingBuffer[0:22]
            self.__processingSize = struct.unpack("<i", self.__processingHeader[18:22])[0] + 22

        if self.__processingHeader:
            if len(self.__processingBuffer) >= self.__processingSize:
                p = loco_packet.Packet()
                p.readLocoPacket(self.__processingBuffer[:self.__processingSize])
                
                self.onPacket(p)

                self.__processingBuffer = self.__processingBuffer[self.__processingSize:]
                self.__processingHeader = b""

    def onPacket(self, packet):
        pass

    def run(self, email, password):
        r = json.loads(kakaoTalk_api.login(email, password, self.device_name, self.device_uuid))
        if r["status"] != kakaoTalk_api.Status["Success"]:
            print(r)
            exit()

        self.__accessKey = r["access_token"]
        self.connect()
        
