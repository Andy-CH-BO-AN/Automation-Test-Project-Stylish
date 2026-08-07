from contextlib import ExitStack
from pathlib import Path

from utils.api_utils import ApiBase


class CreateProductApi(ApiBase):
    def __init__(self, session, data, test_data_dir="test_data"):
        super().__init__(session, "/admin/product")
        self.data = data
        self.test_data_dir = Path(test_data_dir)

    def _open_upload(self, stack, relative_path):
        return stack.enter_context(open(self.test_data_dir / relative_path, "rb"))

    def send(self):
        with ExitStack() as stack:
            files = []

            main_image = self.data.get("main_image")
            if main_image:
                files.append(("main_image", self._open_upload(stack, main_image)))

            for image in self.data.get("other_images", []):
                if image:
                    files.append(("other_images", self._open_upload(stack, image)))

            return self.api_request("post", data=self.data, files=files)
