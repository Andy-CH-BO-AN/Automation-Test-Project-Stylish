import logging
import allure
import math
import pytest
from api_objects.products_category_api import ProductsCategoryApi
from table_object.product_table import search_products_detail_by_category
from utils.api_product_utils import get_all_pages_products, processing_data_to_compare_product_detail


@allure.feature("Product category")
class TestProductCategory:

    @pytest.mark.parametrize("category", ["men", "women", "accessories"])
    @allure.title("user can search all products with valid category and paging")
    def test_user_can_search_products_with_valid_keyword_and_paging(self, session, setup_db, category):
        product_details = []
        max_displayed_products = 6
        db_product_details = search_products_detail_by_category(category, setup_db)
        pages = math.ceil(len(db_product_details) / max_displayed_products)
        product_details = get_all_pages_products(product_details, pages, session, keyword=None, category=category)

        for db_product_detail in db_product_details:
            processing_data_to_compare_product_detail(db_product_detail, setup_db)

        assert len(db_product_details) == len(product_details)
        assert db_product_details == product_details, \
            logging.info(f"expected product_details: {product_details}, "
                         f"expected db_product_details: {db_product_details}")

    @allure.title("user cannot search invalid category")
    def test_user_cannot_search_not_invalid_category(self, session):
        category = "Hello"
        paging = 0
        product_search_api = ProductsCategoryApi(session, category, paging)
        response = product_search_api.send()

        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Category"

    @allure.title("user cannot search without category")
    def test_user_cannot_search_without_keyword(self, session):
        category = None
        paging = 0
        product_search_api = ProductsCategoryApi(session, category, paging)
        response = product_search_api.send()

        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Category"

    @allure.title("user cannot search products if products too few")
    def test_user_cannot_search_if_products_too_few(self, session, setup_db):
        category = "men"
        max_displayed_products = 6
        db_product_details = search_products_detail_by_category(category, setup_db)
        paging = math.ceil(len(db_product_details) / max_displayed_products) + 1

        product_search_api = ProductsCategoryApi(session, category, paging=paging)
        response = product_search_api.send()
        product_detail_data = response.json()["data"]

        assert response.status_code == 200
        assert product_detail_data == []

    @allure.title("user cannot search without paging")
    def test_user_cannot_search_without_paging(self, session):
        category = "men"
        paging = None
        product_search_api = ProductsCategoryApi(session, category, paging)
        response = product_search_api.send()

        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Search paging is required."

    @allure.title("user cannot search invalid paging")
    def test_user_cannot_search_with_invalid_paging(self, session):
        category = "men"
        paging = "men"
        product_search_api = ProductsCategoryApi(session, category, paging)
        response = product_search_api.send()

        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid search paging"
