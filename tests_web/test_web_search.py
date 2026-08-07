import pytest
import allure

from page_objects.index_page import IndexPage
import table_object.product_table


@pytest.mark.parametrize("keyword", ["洋裝", "", "Hello"])
@allure.title("search")
def test_search(setup_driver, setup_db, keyword):
    index_page = IndexPage(setup_driver)
    index_page.search_product_name(keyword)
    products_list = table_object.product_table.search_products_name(keyword, setup_db)
    assert index_page.check_products_name(products_list)
