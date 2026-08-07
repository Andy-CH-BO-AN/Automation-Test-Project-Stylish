from utils.api_utils import ApiBase


class CreateOrderApi(ApiBase):
    def __init__(self, session, payload):
        super().__init__(session, "/order")
        self.payload = payload

    def send(self):
        return self.api_request("post", payload=self.payload)
