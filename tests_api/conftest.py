import logging

import pytest
import requests

from api_objects.login_api import LoginApi
from utils.test_credentials import get_worker_credentials


@pytest.fixture()
def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture()
def login(request, session):
    logging.getLogger().setLevel(logging.INFO)
    email, password = get_worker_credentials(request)

    login_api = LoginApi(session=session, email=email, password=password)
    response = login_api.send()
    yield response, session
