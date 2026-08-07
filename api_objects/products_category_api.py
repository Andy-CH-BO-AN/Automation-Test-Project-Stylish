from utils.api_utils import ApiBase


class ProductsCategoryApi(ApiBase):
    def __init__(self, session, category, paging):
        super().__init__(session, f"/products/{category}")
        self.params = {"paging": paging}

    def send(self):
        return self.api_request("get", params=self.params)
