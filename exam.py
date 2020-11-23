import client

class MyClass(client.Client):
    def onPacket(self, packet):
        print(packet.PacketName)
        print(packet.toJsonBody())
        print("\n")
            
cl = MyClass("device_name", "device_uuid")
cl.run("email", "password")
