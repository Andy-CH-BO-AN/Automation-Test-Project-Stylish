import os
from utils.api_utils import ApiBase


class ProductsDetailApi(ApiBase):
    def __init__(self, session, product_id):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/products/details?id={product_id}"
        super().__init__(session, url)

    def send(self):
        response = self.api_request("get")
        return response
