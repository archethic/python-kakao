import kakaoTalk_api

class PacketCheckInReq:
    def __init__(self, userId = 0, os = "win32", ntype = 0, appVer = kakaoTalk_api.KakaoTalk["Version"], MCCMNC = "999", lang = kakaoTalk_api.KakaoTalk["Lang"]):
        self.userId = userId
        self.os = os
        self.ntype = ntype
        self.appVer = appVer
        self.MCCMNC = MCCMNC
        self.lang = lang

    def PacketName(self):
        return "CHECKIN"

    def toBodyJson(self):
        return {
            "userId": self.userId,
            "os": self.os,
            "ntype": self.ntype,
            "appVer": self.appVer,
            "MCCMNC": self.MCCMNC,
            "lang": self.lang
        }

