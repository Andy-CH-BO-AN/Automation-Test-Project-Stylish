import logging
import os
import random

import allure

from page_objects.cart_page import CartPage
from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from tests_web.product_test_helpers import resolve_product_color


def add_selected_product(product_page, setup_db):
    product_page.select_product_options("size")
    detail = resolve_product_color(product_page.get_product_detail(), setup_db)
    product_page.add_to_cart()
    product_page.get_alert()
    return detail


@allure.title("Verify shopping cart detail")
def test_shopping_cart_detail(setup_driver, setup_db):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)

    with allure.step("add product to cart"):
        index_page.select_a_product()
        product_detail = add_selected_product(product_page, setup_db)

    with allure.step("verify shopping cart detail"):
        product_page.go_to_cart()
        assert [product_detail] == cart_page.get_cart_info()


@allure.title("remove shopping product from cart")
def test_remove_product_from_cart(setup_driver, setup_db):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)
    product_details = []

    with allure.step("add two different products to cart"):
        for _ in range(10):
            if len(product_details) == 2:
                break

            index_page.select_a_product()
            product_page.select_product_options("size")
            detail = resolve_product_color(product_page.get_product_detail(), setup_db)

            if product_details and detail["product_id"] == product_details[0]["product_id"]:
                setup_driver.get(os.getenv("DOMAIN"))
                continue

            product_page.add_to_cart()
            product_page.get_alert()
            product_details.append(detail)
            logging.info("selected products: %s", product_details)

        assert len(product_details) == 2, "Unable to select two different products"

    with allure.step("delete random product"):
        removed_product = random.choice(product_details)
        product_page.go_to_cart()
        cart_page.delete_cart_by_product_id(removed_product["product_id"])
        assert product_page.get_alert() == "已刪除商品"

    product_details.remove(removed_product)
    assert product_details == cart_page.get_cart_info()


@allure.title("edit quantity in cart")
def test_edit_quantity_in_cart(setup_driver, setup_db):
    cart_qty = "2"
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)

    with allure.step("add product to cart"):
        index_page.select_a_product()
        product_page.select_product_options("size")
        product_page.add_to_cart()
        product_page.get_alert()

    with allure.step("edit quantity in cart"):
        product_page.go_to_cart()
        cart_page.edit_cart_quantity(cart_qty)
        assert product_page.get_alert() == "已修改數量"

    with allure.step("verify shopping cart subtotal"):
        cart_detail = cart_page.get_cart_info()[0]
        cart_sub_total = cart_page.get_cart_subtotal()
        assert int(cart_sub_total) == int(cart_detail["product_price"]) * int(cart_qty)
