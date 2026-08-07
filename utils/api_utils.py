import logging


class ApiBase:
    def __init__(self, session, url):
        self.url = url
        self.session = session
        self.response = None

    def api_request(self, method, payload=None, data=None, files=None):
        logging.info(f"Request method: {method}")
        logging.info(f"Request url: {self.url}")
        logging.info(f"payload: {payload}")
        logging.info(f"data: {data}")
        logging.info(f"Request Cookies: {self.session.cookies}")
        logging.info(f"Request headers: {self.session.headers}")
        self.response = self.session.request(method, self.url, json=payload, data=data, files=files)
        logging.info(f"response.json(): {self.response.json()}")
        return self.response
