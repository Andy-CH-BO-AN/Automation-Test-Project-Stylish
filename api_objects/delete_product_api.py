from utils.api_utils import ApiBase


class DeleteProductApi(ApiBase):
    def __init__(self, session, product_id):
        super().__init__(session, f"/admin/{product_id}")

    def send(self):
        return self.api_request("delete")
