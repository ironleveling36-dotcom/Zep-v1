import requests
from fake_useragent import UserAgent

class ZeptoHacker:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Content-Type': 'application/json',
            'x-client-type': 'ANDROID',
            'x-client-version': '3.0.0',
            'x-device-os': 'Android',
        })
        self.base_url = "https://api.zepto.in"

    def request_otp(self, phone: str):
        url = f"{self.base_url}/v2/user/otp/send"
        payload = {
            "mobile": phone,
            "country_code": "+91",
            "flow": "login"
        }
        try:
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code in [200, 201]:
                return r.json().get("request_id")
            print(f"[!] Send OTP Failed: {r.text}")
            return None
        except Exception as e:
            print(f"[!] Exception in send_otp: {e}")
            return None

    def verify_otp(self, request_id: str, otp: str):
        url = f"{self.base_url}/v2/user/otp/verify"
        payload = {
            "request_id": request_id,
            "otp": otp,
            "country_code": "+91"
        }
        headers = {
            'Content-Type': 'application/json',
            'x-client-type': 'ANDROID',
            'x-client-version': '3.0.0'
        }
        try:
            r = self.session.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()["data"]
                tokens = data["auth_tokens"]
                return {
                    "token": tokens["access_token"],
                    "refreshToken": tokens["refresh_token"],
                    "customerId": data["id"],
                    "name": data.get("name", "Unknown"),
                    "email": data.get("email", ""),
                    "sid": tokens.get("session_id", ""),
                    "deviceId": tokens.get("device_id", ""),
                    "mobile": data["mobile"]
                }
            print(f"[!] Verify failed: {r.text}")
            return None
        except Exception as e:
            print(f"[!] Exception in verify_otp: {e}")
            return None
