from utils.api_utils import ApiBase


class GetOrderApi(ApiBase):
    def __init__(self, session, order_number):
        super().__init__(session, f"/order/{order_number}")

    def send(self):
        return self.api_request("get")
