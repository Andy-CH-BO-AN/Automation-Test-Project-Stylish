import os

import allure
import pytest
from api_objects.login_api import LoginApi
from table_object.user_table import search_user_info


@allure.feature("Login")
class TestLogin:
    user_info = [(os.getenv("USER_NAME_1"), os.getenv("PASSWORD") + "a"),
                 (os.getenv("USER_NAME_1") + "a", os.getenv("PASSWORD")),
                 (os.getenv("USER_NAME_1"), ""),
                 ("", os.getenv("PASSWORD"))]

    @allure.title("login success")
    def test_login_success(self, login, setup_db):
        response, session = login
        email = response.json()["data"]["user"]["email"]
        db_result = search_user_info(email, setup_db)
        assert response.status_code == 200
        assert response.json()["data"]["user"]["id"] == db_result["id"]
        assert response.json()["data"]["user"]["provider"] == db_result["provider"]
        assert response.json()["data"]["user"]["name"] == db_result["name"]
        assert response.json()["data"]["user"]["email"] == db_result["email"]
        assert response.json()["data"]["user"]["picture"] == db_result["picture"]
        assert response.json()["data"]["access_token"] == db_result["access_token"]

    @pytest.mark.parametrize(argnames='email, password',
                             argvalues=user_info)
    @allure.title("login fail")
    def test_login_fail(self, session, email, password):
        login_api = LoginApi(session, email=email, password=password)
        response = login_api.send()
        assert response.status_code == 400
        if len(email) == 0 or len(password) == 0:
            assert response.json()["errorMsg"] == "Email and password are required."
        else:
            assert response.json()["errorMsg"] == "Login Failed"
