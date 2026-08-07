import logging

import pytest
import allure

from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from utils.page_base import PageBase


@pytest.mark.parametrize("option", ["color", "size"])
@allure.title("select a product and options")
def test_select_a_product_and_options(setup_driver, option):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    index_page.select_a_product()
    assert product_page.select_product_options(option), logging.info(f"select {option} failed")


@allure.title("quantity editor fail without select size")
def test_quantity_editor_fail_without_select_size(setup_driver):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    index_page.select_a_product()
    qty = product_page.get_quantity()
    product_page.edit_quantity("add")
    expect_qty = product_page.get_quantity()
    assert qty == expect_qty, logging.info(f"qty: {qty} and expect_qty: {expect_qty} is not equal")


@allure.title("quantity editor can increase quantity")
def test_quantity_editor_increase_quantity(setup_driver):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    index_page.select_a_product()
    product_page.select_product_options("size")

    for i in range(8):
        product_page.edit_quantity("add")
    expect_qty = int(product_page.get_quantity())
    assert expect_qty == 9, logging.info(f"expect_qty: {expect_qty} is not 9")

    for i in range(2):
        product_page.edit_quantity("add")
    expect_qty = int(product_page.get_quantity())
    assert expect_qty == 9, logging.info(f"expect_qty: {expect_qty} is not 9")


@allure.title("quantity editor can decrease quantity")
def test_quantity_editor_decrease_quantity(setup_driver):
    index_page = IndexPage(setup_driver)
    product_page = ProductPage(setup_driver)
    index_page.select_a_product()
    product_page.select_product_options("size")

    for i in range(8):
        product_page.edit_quantity("add")
    expect_qty = int(product_page.get_quantity())
    assert expect_qty == 9, logging.info(f"expect_qty: {expect_qty} is not 9")

    for i in range(8):
        product_page.edit_quantity("minus")
    expect_qty = int(product_page.get_quantity())
    assert expect_qty == 1, logging.info(f"expect_qty: {expect_qty} is not 1")


@allure.title("product can add to cart")
def test_add_to_cart(setup_driver):
    index_page = IndexPage(setup_driver)
    page_base = PageBase(setup_driver)
    product_page = ProductPage(setup_driver)

    index_page.select_a_product()
    product_page.select_product_options("size")
    product_page.edit_quantity("add")
    product_page.add_to_cart()

    alert_text = product_page.get_alert()
    assert alert_text == "已加入購物車", logging.info(f"alert_text: {alert_text} is not 已加入購物車")
    setup_driver.switch_to.default_content()
    cart_nums = int(product_page.get_cart_nums())
    assert cart_nums == 1, logging.info(f"cart_nums: {cart_nums} is not 1")


@allure.title("product cannot add to cart with out select size")
def test_add_to_cart_fail_without_select_size(setup_driver):
    index_page = IndexPage(setup_driver)
    page_base = PageBase(setup_driver)
    product_page = ProductPage(setup_driver)

    index_page.select_a_product()
    product_page.add_to_cart()

    alert_text = page_base.get_alert()
    assert alert_text == "請選擇尺寸", logging.info(f"alert_text: {alert_text} is not 請選擇尺寸")
