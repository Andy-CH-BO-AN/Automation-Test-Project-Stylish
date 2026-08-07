import logging
import os

import pytest
import requests

from api_objects.login_api import LoginApi
from api_objects.logout_api import LogoutApi

@pytest.fixture()
def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture()
def login(request, session):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    worker_id = request.config.workerinput['workerid']
    if worker_id == 'gw0':
        email = os.getenv('USER_NAME_1')
        password = os.getenv('PASSWORD')
    elif worker_id == 'gw1':
        email = os.getenv('USER_NAME_2')
        password = os.getenv('PASSWORD')
    else:
        email = os.getenv('USER_NAME_1')
        password = os.getenv('PASSWORD')
    login_api = LoginApi(session=session, email=email, password=password)
    response = login_api.send()
    yield response, session
