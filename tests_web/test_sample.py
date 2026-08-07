from page_objects.index_page import IndexPage
import allure
import logging


@allure.title("display logo")
def test_stylish_logo_displayed(setup_driver):
    index_page = IndexPage(setup_driver)
    logo_element = index_page.get_logo()
    if logo_element.is_displayed():
        logging.info("Stylish logo is displayed.")
        assert True
    else:
        logging.info("Stylish logo isn't displayed.")
        assert False
