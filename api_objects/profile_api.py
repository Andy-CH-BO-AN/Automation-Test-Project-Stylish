from utils.api_utils import ApiBase


class ProfileApi(ApiBase):
    def __init__(self, session):
        super().__init__(session, "/user/profile")

    def send(self):
        return self.api_request("get")
