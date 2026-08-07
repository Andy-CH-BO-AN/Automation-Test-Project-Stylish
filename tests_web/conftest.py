import logging
import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import allure
from allure_commons.types import AttachmentType

from page_objects.admin_page import AdminPage
from page_objects.login_page import LoginPage


@pytest.fixture(scope="function")
def setup_driver():
    # set log
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # set driver
    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get(os.getenv('DOMAIN'))
    yield driver
    allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
    driver.quit()


@pytest.fixture(scope="function")
def login(setup_driver, request):
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
    login_page = LoginPage(setup_driver)
    login_page.go_to_profile()
    login_page.login(email, password)
    alert_text = login_page.get_alert()
    assert alert_text == "Login Success", logging.info(f"alert_text: {alert_text} is not Login Success")
