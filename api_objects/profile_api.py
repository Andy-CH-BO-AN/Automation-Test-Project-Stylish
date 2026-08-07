import os
from utils.api_utils import ApiBase


class ProfileApi(ApiBase):
    def __init__(self, session):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/user/profile"
        super().__init__(session, url)
        self.session = session

    def send(self):
        response = self.api_request("get")
        return response
