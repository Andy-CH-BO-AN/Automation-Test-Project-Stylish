import logging
import os

import allure
import pytest
from allure_commons.types import AttachmentType

from page_objects.login_page import LoginPage


@allure.title("Login and logout success")
def test_login_and_logout_success(setup_driver, login):
    login_page = LoginPage(setup_driver)

    with allure.step("check token is exist"):
        jwt_token = login_page.get_jwt_token()
        assert jwt_token is not None

    with allure.step("logout"):
        allure.attach(setup_driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
        login_page.logout()
        alert_text = login_page.get_alert()
        assert alert_text == "Logout Success", logging.info(f"alert_text: {alert_text} is not Logout Success")


user_info = [(os.getenv("USER_NAME_1"), os.getenv("PASSWORD") + "a"),
             (os.getenv("USER_NAME_1") + "a", os.getenv("PASSWORD")),
             (os.getenv("USER_NAME_1"), "a" + os.getenv("PASSWORD"))]


@pytest.mark.parametrize(argnames='email, password',
                         argvalues=user_info)
@allure.title("Login failed with incorrect email or password")
def test_can_not_login_with_invalid_email_or_password(setup_driver, email, password):
    login_page = LoginPage(setup_driver)
    login_page.go_to_profile()
    login_page.login(email=email, password=password)

    alert_text = login_page.get_alert()
    assert alert_text == "Login Failed", logging.info(f"alert_text: {alert_text} is not Login Failed")


@allure.title("Login fail without token")
def test_can_not_login_without_token(setup_driver, login):
    login_page = LoginPage(setup_driver)

    with allure.step("check token is exist"):
        jwt_token = login_page.get_jwt_token()
        assert jwt_token is not None, logging.info(f"{jwt_token} is not exist")

    with allure.step("logout"):
        login_page.logout()
        login_page.get_alert()

    with allure.step("set invalid token"):
        login_page.set_jwt_token(jwt_token)
        login_page.go_to_profile()
        alert_text = login_page.get_alert()
        assert alert_text == "Invalid Access Token", logging.info(
            f"alert_text: {alert_text} is not Invalid Access Token")
