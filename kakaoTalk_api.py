import requests
import hashlib

Status = {
    "Success": 0
}
KakaoTalk = {
    "Version": "3.1.7",
    "Lang": "ko",
    "osVer": "10.0"
}

AuthHeader = "win32/{version}/{lang}".format(version=KakaoTalk["Version"], lang=KakaoTalk["Lang"])
AuthUserAgent = "KT/{version} Wd/{osVer} {lang}".format(
    version=KakaoTalk["Version"], osVer=KakaoTalk["osVer"], lang=KakaoTalk["Lang"])

def login(email, password, device_name, device_uuid):
    r = requests.post("https://ac-sb-talk.kakao.com/win32/account/login.json", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AuthHeader,
        "X-VC": getXVC(email, device_uuid),
        "User-Agent": AuthUserAgent,
        "Accept": "*/*",
        "Accept-Language": KakaoTalk["Lang"],
    }, data={
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": KakaoTalk["osVer"],
        "permanent": True,
        "forced": True
    })

    return r.content.decode()

def getXVC(email, device_uuid, isFull=False):
    hash = hashlib.sha512("HEATH|{}|DEMIAN|{}|{}".format(
        AuthUserAgent, email, device_uuid).encode("utf-8")).hexdigest()
    if(isFull):
        return hash
    return hash[0:16]
