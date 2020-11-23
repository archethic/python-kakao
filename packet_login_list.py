import kakaoTalk_api

class PacketLoginListReq:
    def __init__(self, appVer = kakaoTalk_api.KakaoTalk["Version"], prtVer = "1", os = "win32", lang = "ko", duuid = None, oauthToken = None, dtype = 1, ntype = 0, MCCMNC = "999", revision = 0, chatIds = [], maxIds = [], lastTokenId = 0, lbk = 0, bg = False):
        self.appVer = appVer
        self.prtVer = prtVer
        self.os = os
        self.lang = lang
        self.duuid = duuid
        self.oauthToken = oauthToken
        self.dtype = dtype
        self.ntype = ntype
        self.MCCMNC = MCCMNC
        self.revision = revision
        self.chatIds = chatIds
        self.maxIds = maxIds
        self.lastTokenId = lastTokenId
        self.lbk = lbk
        self.bg = bg

    def PacketName(self):
        return "LOGINLIST"

    def toBodyJson(self):
        return {
            "appVer": self.appVer,
            "prtVer": self.prtVer,
            "os": self.os,
            "lang": self.lang,
            "duuid": self.duuid,
            "oauthToken": self.oauthToken,
            "dtype": self.dtype,
            "ntype": self.ntype,
            "MCCMNC": self.MCCMNC,
            "revision": self.revision,
            "chatIds": self.chatIds,
            "maxIds": self.maxIds,
            "lastTokenId": self.lastTokenId,
            "lbk": self.lbk,
            "bg": self.bg
        }
