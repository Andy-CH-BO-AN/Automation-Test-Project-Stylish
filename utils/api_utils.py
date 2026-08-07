import logging
import os


class ApiBase:
    def __init__(self, session, path=None, *, url=None):
        if (path is None) == (url is None):
            raise ValueError("Provide exactly one of path or url")

        self.session = session
        self.url = url or self._build_url(path)
        self.response = None

    @staticmethod
    def _build_url(path):
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise RuntimeError("BASE_URL is required")
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    def api_request(
        self,
        method,
        payload=None,
        data=None,
        files=None,
        params=None,
        headers=None,
    ):
        logging.info("Request %s %s", method.upper(), self.url)
        self.response = self.session.request(
            method,
            self.url,
            json=payload,
            data=data,
            files=files,
            params=params,
            headers=headers,
        )
        logging.info("Response status: %s", self.response.status_code)
        return self.response
