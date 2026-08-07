import allure
import pytest
from api_objects.profile_api import ProfileApi
from table_object.user_table import search_user_info


@pytest.fixture()
def profile_api(session):
    return ProfileApi(session)


@allure.feature("Profile")
class TestProfile:
    @allure.title("get user profile success")
    def test_get_user_profile_success(self, login, profile_api, setup_db):
        response, session = login
        email = response.json()["data"]["user"]["email"]
        db_result = search_user_info(email, setup_db)
        response = profile_api.send()
        assert response.status_code == 200
        assert response.json()["data"]["provider"] == db_result["provider"]
        assert response.json()["data"]["name"] == db_result["name"]
        assert response.json()["data"]["email"] == db_result["email"]

    @allure.title("get user profile without login")
    def test_get_user_profile_without_login(self, profile_api):
        response = profile_api.send()
        assert response.status_code == 401
        assert response.json()["errorMsg"] == "Unauthorized"

    @allure.title("get user profile with invalid token")
    def test_get_user_profile_with_invalid_token(self, profile_api, session):
        session.headers["Authorization"] = f"Bearer a"
        response = profile_api.send()
        assert response.status_code == 403
        assert response.json()["errorMsg"] == "Forbidden"
