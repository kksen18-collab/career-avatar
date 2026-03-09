import requests

import logging

logger = logging.getLogger(__name__)


class PushoverClient:
    def __init__(self, token: str, user_key: str, url: str):
        self.token = token
        self.user_key = user_key
        self.url = url

    def push(self, message: str):
        logger.info("Sending pushover notification %s", message)
        payload = {"user": self.user_key, "token": self.token, "message": message}
        logger.debug("Pushover payload:%s",payload)
        response = requests.post(self.url, data=payload)
        logger.debug(f"Pushover response: {response}")
