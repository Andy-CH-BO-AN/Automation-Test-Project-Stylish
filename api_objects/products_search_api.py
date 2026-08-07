from utils.api_utils import ApiBase


class ProductsSearchApi(ApiBase):
    def __init__(self, session, keyword, paging):
        super().__init__(session, "/products/search")
        self.params = {"keyword": keyword, "paging": paging}

    def send(self):
        return self.api_request("get", params=self.params)
