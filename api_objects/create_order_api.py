import os
from utils.api_utils import ApiBase


class CreateOrderApi(ApiBase):
    def __init__(self, session, payload):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/order"
        super().__init__(session, url)
        self.session = session
        self.payload = payload
        self.session.headers = {
            "Authorization": self.session.headers["Authorization"]
        }

    def send(self):
        response = self.api_request("post", self.payload)
        return response
