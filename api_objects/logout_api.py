from utils.api_utils import ApiBase


class LogoutApi(ApiBase):
    def __init__(self, session):
        super().__init__(session, "/user/logout")

    def send(self):
        return self.api_request("post")
