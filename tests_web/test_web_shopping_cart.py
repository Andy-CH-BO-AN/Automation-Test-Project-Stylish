import logging
import os
import random

import allure

from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from page_objects.cart_page import CartPage


@allure.title("Verify shopping cart detail")
def test_shopping_cart_detail(setup_driver, setup_db):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)
    product_detail_list = []

    with allure.step("add product to cart"):
        index_page.select_a_product()
        product_page.select_product_options("size")
        product_detail = product_page.get_product_detail(setup_db)
        product_detail_list.append(product_detail)
        product_page.add_to_cart()
        product_page.get_alert()

    with allure.step("verify shopping cart detail"):
        product_page.go_to_cart()
        cart_detail_list = cart_page.get_cart_info()
        assert product_detail_list == cart_detail_list


@allure.title("remove shopping product from cart")
def test_remove_product_from_cart(setup_driver, setup_db):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)
    product_detail_list = []
    select_nums = 0
    with allure.step("add products to cart"):
        while True:
            if select_nums == 2:
                break
            index_page.select_a_product()
            product_page.select_product_options("size")
            product_detail = product_page.get_product_detail(setup_db)
            if len(product_detail_list) > 0 and product_detail["product_id"] == product_detail_list[0]["product_id"]:
                setup_driver.get(os.getenv('DOMAIN'))
            else:
                product_detail_list.append(product_detail)
                product_page.add_to_cart()
                product_page.get_alert()
                select_nums += 1
            logging.info(product_detail_list)

    with allure.step("delete random product"):
        random_product_detail = random.choice(product_detail_list)
        product_page.go_to_cart()
        cart_page.delete_cart_by_product_id(random_product_detail["product_id"])
        alert_text = product_page.get_alert()
        assert alert_text == "已刪除商品", logging.info(f"alert_text: {alert_text} is not 已刪除商品")

    product_detail_list.remove(random_product_detail)
    cart_detail_list = cart_page.get_cart_info()
    logging.info(f"product_detail_list: {product_detail_list}")
    logging.info(f"cart_detail_list: {cart_detail_list}")
    assert product_detail_list == cart_detail_list, \
        logging.info(f"product_detail_list: {product_detail_list} and "
                     f"cart_detail_list: {cart_detail_list} is not equal")


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
        alert_text = product_page.get_alert()
        assert alert_text == "已修改數量", logging.info(f"alert_text: {alert_text} is not 已修改數量")

    with allure.step("verify shopping cart subtotal"):
        cart_detail_list = cart_page.get_cart_info()
        cart_sub_total = cart_page.get_cart_subtotal()
        logging.info(f"{cart_sub_total}, {cart_detail_list[0]['product_price']}")
        assert int(cart_sub_total) == int(cart_detail_list[0]['product_price']) * int(cart_qty), \
            logging.info(f"cart_sub_total: {int(cart_sub_total)} and "
                         f"product_price: {int(cart_detail_list[0]['product_price']) * int(cart_qty)} is not equal")
