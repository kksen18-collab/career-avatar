import requests

class PushoverClient:
    def __init__(self, token:str, user_key:str,url:str):
        self.token = token
        self.user_key = user_key
        self.url = url
        
    def push(self, message: str):
        print(f"Push: {message}")
        payload = {"user": self.user_key, "token": self.token, "message": message}
        requests.post(self.url, data=payload)