import logging
import random

from selenium.webdriver.common.by import By

from table_object import color_table
from utils.page_base import PageBase


class ProductPage(PageBase):
    qty_value = (By.CLASS_NAME, "product__quantity-value")
    btn_add_to_cart = (By.CLASS_NAME, "product__add-to-cart-button")
    cart_number = (By.CLASS_NAME, "header__link-icon-cart-number")
    btn_cart = (By.CLASS_NAME, "header__link-icon-cart")
    product_name = (By.CLASS_NAME, "product__title")
    product_id = (By.CLASS_NAME, "product__id")
    product_price = (By.CLASS_NAME, "product__price")

    def product_options(self, option):
        return By.CLASS_NAME, f"product__{option}"

    def product_option_selected(self, option):
        return By.XPATH, f"//div[contains(@class, 'product__{option}--selected')]"

    def select_product_options(self, option):
        elements = self.find_elements(self.product_options(option))
        element = random.choice(elements)
        element.click()
        selected_element = self.find_element(self.product_option_selected(option))

        if option == "size":
            logging.info("size: %s\nselected size: %s", element.text, selected_element.text)
            return element.text == selected_element.text

        logging.info(
            "data_id: %s\nselected data_id: %s",
            element.get_attribute("data_id"),
            selected_element.get_attribute("data_id"),
        )
        logging.info(
            "style: %s\nselected style: %s",
            element.get_attribute("style"),
            selected_element.get_attribute("style"),
        )
        return (
            element.get_attribute("data_id") == selected_element.get_attribute("data_id")
            and element.get_attribute("style") == selected_element.get_attribute("style")
        )

    def get_quantity(self):
        qty = self.find_element(self.qty_value).text
        logging.info("qty: %s", qty)
        return qty

    def edit_quantity(self, operation):
        self.find_element((By.CLASS_NAME, f"product__quantity-{operation}")).click()

    def add_to_cart(self):
        self.find_element(self.btn_add_to_cart).click()

    def get_cart_nums(self):
        cart_nums = self.find_element(self.cart_number).text
        logging.info("cart_nums: %s", cart_nums)
        return cart_nums

    def get_product_detail(self, conn):
        product_name = self.find_element(self.product_name, clickable=False).text
        product_id = self.find_element(self.product_id, clickable=False).text
        product_price = (
            self.find_element(self.product_price, clickable=False)
            .text.split("\n")[-1]
            .split(".")[-1]
        )
        color_id = (
            self.find_element(self.product_option_selected("color"))
            .get_attribute("data_id")
            .replace("color_code_", "")
        )
        product_color = color_table.search_color(color_id, conn)
        product_size = self.find_element(self.product_option_selected("size")).text
        product_qty = self.get_quantity()

        product_detail = {
            "product_name": product_name,
            "product_id": product_id,
            "product_price": product_price,
            "product_color": product_color,
            "product_size": product_size,
            "product_qty": product_qty,
        }
        logging.info(product_detail)
        return product_detail

    def go_to_cart(self):
        self.find_element(self.btn_cart).click()
