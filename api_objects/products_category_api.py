import os
from utils.api_utils import ApiBase


class ProductsCategoryApi(ApiBase):
    def __init__(self, session, category, paging):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/products/{category}?paging={paging}"
        super().__init__(session, url)

    def send(self):
        response = self.api_request("get")
        return response
