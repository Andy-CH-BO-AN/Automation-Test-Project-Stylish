import json
import os
import urllib.parse

from utils.api_utils import ApiBase


class GetOrderPrimeApi(ApiBase):
    URL = "https://js.tappaysdk.com/tpdirect/sandbox/getprime"

    def __init__(self, session, cardnumber, cardduedate, cardccv):
        super().__init__(session, url=self.URL)
        self.headers = {
            "Authorization": None,
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Api-Key": os.getenv("X_API_KEY"),
        }
        payload = {
            "cardnumber": cardnumber,
            "cardduedate": cardduedate,
            "cardccv": cardccv,
            "appid": 12348,
            "appkey": os.getenv("X_API_KEY"),
            "appname": os.getenv("DB_HOST"),
            "url": os.getenv("DOMAIN"),
            "port": "",
            "protocol": "http:",
            "fraudid": "",
        }
        self.data = "jsonString=" + urllib.parse.quote(json.dumps(payload))

    def send(self):
        return self.api_request("post", data=self.data, headers=self.headers)
