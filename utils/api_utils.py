import logging


class ApiBase:
    def __init__(self, session, url):
        self.url = url
        self.session = session
        self.response = None

    def api_request(self, method, payload=None, data=None, files=None):
        logging.info("Request %s %s", method.upper(), self.url)
        self.response = self.session.request(
            method,
            self.url,
            json=payload,
            data=data,
            files=files,
        )
        logging.info("Response status: %s", self.response.status_code)
        return self.response
