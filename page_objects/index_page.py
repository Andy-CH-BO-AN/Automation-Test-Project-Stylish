import logging
import random

from selenium.webdriver import Keys

from utils.page_base import PageBase
from selenium.webdriver.common.by import By


class IndexPage(PageBase):
    search_input = (By.CLASS_NAME, "header__search-input")
    logo = (By.CLASS_NAME, "header__logo")
    product_title = (By.CLASS_NAME, "product__title")
    products = (By.CLASS_NAME, "products")

    def get_logo(self):
        logo_element = self.find_element(self.logo, clickable=False)
        return logo_element

    def go_to_category(self, category):
        logging.info(f"category: {category}")
        self.find_element((By.XPATH, f'//a[@href="./index.html?category={category}"]')).click()

    def check_products_name(self, products_list):
        self.scroll_down()
        products = self.find_element(self.products)
        if products.text == "":
            return products_list == []
        else:
            elements = self.find_elements(self.product_title)
            expected_products_list = sorted(products_list)
            found_product_list = sorted([element.text for element in elements])
            logging.info(f"expected product list: {expected_products_list}")
            logging.info(f"found product list: {found_product_list}")
            return expected_products_list == found_product_list

    def search_product_name(self, keyword):
        logging.info(f"keyword: {keyword}")
        self.find_element(self.search_input).send_keys(keyword)
        self.find_element(self.search_input).send_keys(Keys.ENTER)

    def select_a_product(self):
        elements = self.find_elements(self.product_title)
        element = random.choice(elements)
        logging.info(f"product: {element.text}")
        element.click()
