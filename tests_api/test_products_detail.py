import logging

import allure

from api_objects.products_detail_api import ProductsDetailApi
from table_object.product_table import search_products_detail_by_id, search_random_product_id
from utils.api_product_utils import normalize_db_product_detail


@allure.feature("Product detail")
class TestProductDetail:
    @allure.title("user can get product detail with valid product id")
    def test_user_can_get_product_detail(self, session, setup_db):
        product_id = search_random_product_id(setup_db)
        db_row = search_products_detail_by_id(product_id, setup_db)[0]
        db_product_detail = normalize_db_product_detail(db_row, setup_db)

        response = ProductsDetailApi(session, product_id).send()
        assert response.status_code == 200
        assert response.json()["data"] == db_product_detail, logging.info(
            "expected product_detail: %s expected db_product_detail: %s",
            response.json()["data"],
            db_product_detail,
        )

    @allure.title("user can't get product detail if the product not exist")
    def test_product_detail_not_exist(self, session, setup_db):
        product_id = 123456789098
        assert search_products_detail_by_id(product_id, setup_db) == ()

        response = ProductsDetailApi(session, product_id).send()
        assert response.status_code == 404
        assert response.json()["errorMsg"] == "404 Not Found"

    @allure.title("user can't get product detail if product id is invalid")
    def test_product_detail_with_invalid_product_id(self, session, setup_db):
        product_id = f"{search_random_product_id(setup_db)}a"
        assert search_products_detail_by_id(product_id, setup_db) == ()

        response = ProductsDetailApi(session, product_id).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Product ID"

    @allure.title("user can't get product detail if product id is None")
    def test_product_detail_without_product_id(self, session, setup_db):
        product_id = ""
        assert search_products_detail_by_id(product_id, setup_db) == ()

        response = ProductsDetailApi(session, product_id).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Product ID"
