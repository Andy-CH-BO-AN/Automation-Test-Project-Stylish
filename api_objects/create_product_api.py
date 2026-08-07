import os
from utils.api_utils import ApiBase


class CreateProductApi(ApiBase):
    def __init__(self, session, data):
        self.base_url = os.getenv("BASE_URL")
        url = f"{self.base_url}/admin/product"
        super().__init__(session, url)
        self.data = data
        self.files = []

        if data['main_image'] != "":
            main_image = f"./test_data/{data['main_image']}"
            self.files.append(('main_image', open(main_image, 'rb')))

        for image in data['other_images']:
            image_path = f"./test_data/{image}"
            self.files.append(('other_images', open(image_path, 'rb')))

    def send(self):
        response = self.api_request("post", data=self.data, files=self.files)
        return response
