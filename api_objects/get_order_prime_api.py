import os
from utils.api_utils import ApiBase
import json
import urllib.parse


class GetOrderPrimeApi(ApiBase):
    def __init__(self, session, cardnumber, cardduedate, cardccv):
        url = f"https://js.tappaysdk.com/tpdirect/sandbox/getprime"
        super().__init__(session, url)
        self.session = session
        self.session.headers = {
            "Authorization": self.session.headers["Authorization"],
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
            "fraudid": ""
        }
        self.data = 'jsonString=' + urllib.parse.quote(json.dumps(payload))

    def send(self):
        response = self.api_request("post", data=self.data)
        return response
