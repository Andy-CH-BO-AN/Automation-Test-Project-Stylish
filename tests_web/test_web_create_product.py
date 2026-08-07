import logging
import os

import allure
import pytest
from page_objects.admin_page import AdminPage
from page_objects.index_page import IndexPage
from test_data import test_data_from_excel


@pytest.mark.usefixtures("login")
@pytest.mark.usefixtures("delete_products_method")
@pytest.mark.parametrize('product_info',
                         test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx', 'Create Product Success'))
@allure.title("create product success")
def test_create_product_success(setup_driver, product_info, request):
    admin_page = AdminPage(setup_driver)
    admin_page.go_to_admin_page()
    admin_page.go_to_create_product_page()
    admin_page.input_product_detail(product_info)
    admin_page.create_product()
    admin_page.get_alert()
    setup_driver.switch_to.window(setup_driver.window_handles[0])
    admin_page.verify_product_info_in_admin(product_info)

    def teardown_method():
        admin_page.delete_product(product_info)

    request.addfinalizer(teardown_method)


@pytest.mark.usefixtures("login")
@pytest.mark.usefixtures("delete_products_method")
@pytest.mark.parametrize('product_info',
                         test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx', 'Create Product Failed'))
@allure.title("create product fail")
def test_create_product_fail(setup_driver, product_info, request):
    admin_page = AdminPage(setup_driver)
    admin_page.go_to_admin_page()
    admin_page.go_to_create_product_page()
    admin_page.input_product_detail(product_info)
    admin_page.create_product()
    alert_text = admin_page.get_alert()
    assert alert_text == product_info["Alert Msg"], logging.info(
        f"alert_text: {alert_text} is not {product_info['Alert Msg']}")

    def teardown_method():
        admin_page.delete_product(product_info)

    request.addfinalizer(teardown_method)


@pytest.mark.parametrize('product_info',
                         test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx', 'Create Product Success'))
@allure.title("create product fail without login")
def test_create_product_fail_without_login(setup_driver, product_info):
    index_page = IndexPage(setup_driver)
    admin_page = AdminPage(setup_driver)
    setup_driver.get(os.getenv("DOMAIN") + "/admin/product_create.html")
    admin_page.input_product_detail(product_info)
    admin_page.create_product()
    alert_text = admin_page.get_alert()
    assert alert_text == "Please Login First", logging.info(f"alert_text: {alert_text} is not Please Login First")

    index_page.get_logo()
    assert setup_driver.current_url == os.getenv("DOMAIN") + "/login.html" \
        , logging.info(f"setup_driver.current_url: {setup_driver.current_url} is not "
                       f"{os.getenv('DOMAIN') + '/login.html'}")
