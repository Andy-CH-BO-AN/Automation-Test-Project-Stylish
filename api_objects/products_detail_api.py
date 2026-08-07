from utils.api_utils import ApiBase


class ProductsDetailApi(ApiBase):
    def __init__(self, session, product_id):
        super().__init__(session, "/products/details")
        self.params = {"id": product_id}

    def send(self):
        return self.api_request("get", params=self.params)
