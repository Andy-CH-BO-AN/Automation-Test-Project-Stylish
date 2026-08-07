import os
from utils.api_utils import ApiBase


class GetOrderApi(ApiBase):
    def __init__(self, session, order_number):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/order/{order_number}"
        super().__init__(session, url)
        self.session = session

    def send(self):
        response = self.api_request("get")
        return response
