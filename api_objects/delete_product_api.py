import os
from utils.api_utils import ApiBase


class DeleteProductApi(ApiBase):
    def __init__(self, session, product_id):
        self.base_url = os.getenv("BASE_URL")
        self.product_id = product_id
        url = f"{self.base_url}/admin/{product_id}"
        super().__init__(session, url)

    def send(self):
        response = self.api_request("delete")
        return response
