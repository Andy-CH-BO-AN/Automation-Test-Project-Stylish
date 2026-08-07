import allure
import pytest
from api_objects.logout_api import LogoutApi


@pytest.fixture()
def logout_api(session):
    return LogoutApi(session)


@allure.feature("Logout")
class TestLogout:
    @allure.title("logout success")
    def test_logout_success(self, login, logout_api, setup_db):
        response = logout_api.send()
        assert response.status_code == 200
        assert response.json()["message"] == "Logout Success"

    @allure.title("logout without login")
    def test_logout_without_login(self, logout_api):
        response = logout_api.send()
        assert response.status_code == 401
        assert response.json()["errorMsg"] == "Unauthorized"

    @allure.title("logout with invalid token")
    def test_logout_with_invalid_token(self, session, logout_api):
        session.headers["Authorization"] = f"Bearer a"
        response = logout_api.send()
        assert response.status_code == 403
        assert response.json()["errorMsg"] == "Forbidden"
