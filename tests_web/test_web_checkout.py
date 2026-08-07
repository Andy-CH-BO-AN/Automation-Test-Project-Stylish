import logging
import os

import allure
import pytest

from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from page_objects.cart_page import CartPage
from page_objects.index_page import IndexPage
from test_data import test_data_from_excel


@allure.title("checkout with empty cart")
def test_checkout_with_empty_cart(setup_driver, login):
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)

    with allure.step("No product added to cart"):
        product_page.go_to_cart()
        cart_page.click_checkout_button()

    alert_text = cart_page.get_alert()
    assert alert_text == "尚未選購商品", logging.info(f"alert_text: {alert_text} is not 尚未選購商品")


@pytest.mark.parametrize('customer_info',
                         test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx',
                                                        'Checkout with Invalid Value'))
@allure.title("checkout fail")
def test_checkout_fail(setup_driver, login, setup_db, customer_info):
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)
    index_page = IndexPage(setup_driver)

    with allure.step("Add to cart"):
        index_page.search_product_name("")
        index_page.select_a_product()
        product_page.select_product_options("size")
        product_page.add_to_cart()
        product_page.get_alert()

    with allure.step("Checkout with invalid customer info"):
        product_page.go_to_cart()
        cart_page.input_check_out_detail(customer_info)
        cart_page.click_checkout_button()

    alert_text = cart_page.get_alert()
    logging.info(customer_info)
    assert alert_text == customer_info["Alert Msg"], \
        logging.info(f"alert_text: {alert_text} is not {customer_info['Alert Msg']}")


@pytest.mark.parametrize('customer_info',
                         test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx', 'Checkout with Valid Value'))
@allure.title("checkout success")
def test_checkout_success(setup_driver, login, setup_db, customer_info):
    product_page = ProductPage(setup_driver)
    cart_page = CartPage(setup_driver)
    index_page = IndexPage(setup_driver)
    with allure.step("Add to cart"):
        index_page.search_product_name("")
        index_page.select_a_product()
        product_page.select_product_options("size")
        product_page.add_to_cart()
        product_page.get_alert()

    with allure.step("Checkout with valid customer info"):
        product_page.go_to_cart()
        customer_detail = cart_page.input_check_out_detail(customer_info)
        cart_page.click_checkout_button()

    alert_text = cart_page.get_alert()
    assert alert_text == "付款成功", \
        logging.info(f"alert_text: {alert_text} is not 付款成功")

    with allure.step("Verify thank you page"):
        cart_page.verify_check_out_info(customer_detail)
