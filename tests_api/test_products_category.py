import logging
import math

import allure
import pytest

from api_objects.products_category_api import ProductsCategoryApi
from table_object.product_table import search_products_detail_by_category
from utils.api_product_utils import get_all_pages_products, normalize_db_product_detail


@allure.feature("Product category")
class TestProductCategory:
    @pytest.mark.parametrize("category", ["men", "women", "accessories"])
    @allure.title("user can search all products with valid category and paging")
    def test_user_can_search_products_with_valid_keyword_and_paging(self, session, setup_db, category):
        max_displayed_products = 6
        db_rows = search_products_detail_by_category(category, setup_db)
        pages = math.ceil(len(db_rows) / max_displayed_products)

        product_details = get_all_pages_products(session, pages, category=category)
        db_product_details = [
            normalize_db_product_detail(row, setup_db)
            for row in db_rows
        ]

        assert len(db_product_details) == len(product_details)
        assert db_product_details == product_details, logging.info(
            "expected product_details: %s, expected db_product_details: %s",
            product_details,
            db_product_details,
        )

    @allure.title("user cannot search invalid category")
    def test_user_cannot_search_not_invalid_category(self, session):
        response = ProductsCategoryApi(session, "Hello", 0).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Category"

    @allure.title("user cannot search without category")
    def test_user_cannot_search_without_keyword(self, session):
        response = ProductsCategoryApi(session, None, 0).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid Category"

    @allure.title("user cannot search products if products too few")
    def test_user_cannot_search_if_products_too_few(self, session, setup_db):
        category = "men"
        max_displayed_products = 6
        db_product_details = search_products_detail_by_category(category, setup_db)
        paging = math.ceil(len(db_product_details) / max_displayed_products) + 1

        response = ProductsCategoryApi(session, category, paging=paging).send()
        assert response.status_code == 200
        assert response.json()["data"] == []

    @allure.title("user cannot search without paging")
    def test_user_cannot_search_without_paging(self, session):
        response = ProductsCategoryApi(session, "men", None).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Search paging is required."

    @allure.title("user cannot search invalid paging")
    def test_user_cannot_search_with_invalid_paging(self, session):
        response = ProductsCategoryApi(session, "men", "men").send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Invalid search paging"
