import requests
import allure
import pytest

from api_objects.create_product_api import CreateProductApi
from api_objects.delete_product_api import DeleteProductApi
from api_objects.products_detail_api import ProductsDetailApi
from test_data import test_data_from_excel
from tests_api.product_test_helpers import (
    delete_product_if_exists,
    find_product_by_title,
    product_id,
    product_payload_from_row,
)


def sample_product_payload():
    return {
        "category": "men",
        "title": "m",
        "description": "m",
        "price": 69,
        "texture": "m",
        "wash": "m",
        "place": "m",
        "note": "m",
        "color_ids": ["1", "2"],
        "sizes": ["M", "XL"],
        "story": "m",
        "main_image": "mainImage.jpg",
        "other_images": ["otherImage0.jpg", "otherImage1.jpg"],
    }


@allure.feature("Create and delete product")
class TestCreateProduct:
    @pytest.mark.parametrize(
        "product_row",
        test_data_from_excel.read_data(
            "test_data/Stylish_TestCase.xlsx",
            "API Create Product Success",
        ),
    )
    @allure.title("admin can create and delete product success")
    def test_admin_can_create_and_delete_product(self, login, session, product_row):
        payload = product_payload_from_row(product_row)

        try:
            response = CreateProductApi(session, payload).send()
            assert response.status_code == 200

            product = find_product_by_title(session, payload["title"])
            assert product is not None

            created_product_id = product_id(product)
            response = DeleteProductApi(session, created_product_id).send()
            assert response.status_code == 200

            response = ProductsDetailApi(session, created_product_id).send()
            assert response.status_code == 404
        finally:
            delete_product_if_exists(session, payload["title"])

    @pytest.mark.parametrize(
        "product_row",
        test_data_from_excel.read_data(
            "test_data/Stylish_TestCase.xlsx",
            "API Create Product Failed",
        ),
    )
    @allure.title("admin cannot create product with invalid value")
    def test_admin_cannot_create_product_with_invalid_value(self, login, session, product_row):
        payload = product_payload_from_row(product_row)
        try:
            response = CreateProductApi(session, payload).send()
            assert response.status_code == 400
            assert response.json()["errorMsg"] == product_row["Error Msg"]
        finally:
            delete_product_if_exists(session, payload["title"])

    @allure.title("admin cannot create product without login")
    def test_admin_cannot_create_product_without_login(self, session):
        response = CreateProductApi(session, sample_product_payload()).send()
        assert response.status_code == 401
        assert response.json()["errorMsg"] == "Unauthorized"

    @allure.title("admin cannot delete product without login")
    def test_admin_cannot_delete_product_without_login(self, login, session):
        payload = sample_product_payload()
        try:
            response = CreateProductApi(session, payload).send()
            assert response.status_code == 200

            product = find_product_by_title(session, payload["title"])
            assert product is not None

            with requests.Session() as anonymous_session:
                response = DeleteProductApi(anonymous_session, product_id(product)).send()
            assert response.status_code == 401
            assert response.json()["errorMsg"] == "Unauthorized"
        finally:
            delete_product_if_exists(session, payload["title"])

    def test_admin_cannot_delete_product_without_product_id(self, login, session):
        response = DeleteProductApi(session, "").send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Product ID not found."

    def test_admin_cannot_delete_product_with_product_id_not_exist(self, login, session):
        response = DeleteProductApi(session, 123412341234).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Product ID not found."

    def test_admin_cannot_delete_product_with_invalid_product_id(self, login, session):
        response = DeleteProductApi(session, "a").send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Product ID"
