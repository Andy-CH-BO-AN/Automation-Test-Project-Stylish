import logging
import os

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page_objects.login_page import LoginPage
from utils.test_credentials import get_worker_credentials


@pytest.fixture(scope="function")
def setup_driver():
    logging.getLogger().setLevel(logging.INFO)

    domain = os.getenv("DOMAIN")
    if not domain:
        pytest.fail("DOMAIN environment variable is required for web tests")

    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(domain)

    try:
        yield driver
    finally:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Screenshot",
                attachment_type=AttachmentType.PNG,
            )
        except Exception:
            logging.exception("Unable to capture final browser screenshot")
        driver.quit()


@pytest.fixture(scope="function")
def login(setup_driver, request):
    email, password = get_worker_credentials(request)

    login_page = LoginPage(setup_driver)
    login_page.go_to_profile()
    login_page.login(email, password)
    alert_text = login_page.get_alert()
    assert alert_text == "Login Success", f"Unexpected login alert: {alert_text}"
