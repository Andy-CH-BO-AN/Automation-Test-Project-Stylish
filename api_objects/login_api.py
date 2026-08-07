import os
from utils.api_utils import ApiBase


class LoginApi(ApiBase):
    def __init__(self, session, email, password):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/user/login"
        super().__init__(session, url)
        self.payload = {
            "provider": "native",
            "email": email,
            "password": password
        }

    def send(self):
        response = self.api_request("post", self.payload)
        if response.status_code == 200:
            token = response.json()['data']['access_token']
            self.session.headers["Authorization"] = f"Bearer {token}"
        return response
