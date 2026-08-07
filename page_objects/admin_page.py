import logging
import os
from pathlib import Path

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from utils.page_base import PageBase


class AdminPage(PageBase):
    IMAGE_DIR = Path("test_data/Stylish_product_image").resolve()

    btn_go_to_create_product = (By.XPATH, "//button[text()='Create New Product']")
    select_category = (By.XPATH, "//select[@name='category']")
    input_title = (By.XPATH, "//input[@name='title']")
    textarea_description = (By.XPATH, "//textarea[@name='description']")
    input_price = (By.XPATH, "//input[@name='price']")
    input_texture = (By.XPATH, "//input[@name='texture']")
    input_wash = (By.XPATH, "//input[@name='wash']")
    input_place_of_production = (By.XPATH, "//input[@name='place']")
    input_note = (By.XPATH, "//input[@name='note']")
    input_story = (By.XPATH, "//input[@name='story']")
    input_main_image = (By.XPATH, "//input[@name='main_image']")
    input_other_images = (By.XPATH, "//input[@name='other_images']")
    btn_create_product = (By.XPATH, "//input[@value='Create']")
    product_title = (By.ID, "product_title")
    checkbox_colors = (By.ID, "color_ids")
    checkbox_sizes = (By.NAME, "sizes")

    def go_to_admin_page(self):
        self.driver.get(f"{os.getenv('DOMAIN')}/admin/products.html")

    def go_to_create_product_page(self):
        current_window = self.driver.current_window_handle
        self.find_element(self.btn_go_to_create_product).click()
        self.wait.until(EC.number_of_windows_to_be(2))
        new_window = next(
            handle for handle in self.driver.window_handles if handle != current_window
        )
        self.driver.switch_to.window(new_window)

    def input_product_detail(self, product_detail):
        logging.info("product detail: %s", product_detail)
        Select(self.find_element(self.select_category)).select_by_visible_text(
            product_detail["Category"]
        )
        self.find_element(self.input_title).send_keys(product_detail["Title"])
        self.find_element(self.textarea_description).send_keys(product_detail["Description"])
        self.find_element(self.input_price).send_keys(product_detail["Price"])
        self.find_element(self.input_texture).send_keys(product_detail["Texture"])
        self.find_element(self.input_wash).send_keys(product_detail["Wash"])
        self.find_element(self.input_place_of_production).send_keys(product_detail["Place of Product"])
        self.find_element(self.input_note).send_keys(product_detail["Note"])

        for color in product_detail["Colors"].split(", "):
            self.select_color(color)
        for size in product_detail["Sizes"].split(", "):
            self.select_size(size)

        self.find_element(self.input_story).send_keys(product_detail["Story"])
        self._upload_images(product_detail)
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Screenshot",
            attachment_type=AttachmentType.PNG,
        )

    def _upload_images(self, product_detail):
        if product_detail["Main Image"]:
            self.find_element(self.input_main_image).send_keys(
                str(self.IMAGE_DIR / product_detail["Main Image"])
            )

        other_image_inputs = self.find_elements(self.input_other_images)
        for index, key in enumerate(("Other Image 1", "Other Image 2")):
            if product_detail[key]:
                other_image_inputs[index].send_keys(
                    str(self.IMAGE_DIR / product_detail[key])
                )

    def select_color(self, color):
        logging.info("color: %s", color)
        if not color:
            return
        if color == "全選":
            for element in self.find_elements(self.checkbox_colors):
                element.click()
            return
        self.find_element(
            (By.XPATH, f'//label[text()=" {color} "]/preceding-sibling::input')
        ).click()

    def select_size(self, size):
        logging.info("size: %s", size)
        if not size:
            return
        if size == "全選":
            for element in self.find_elements(self.checkbox_sizes):
                element.click()
            return
        self.find_element((By.XPATH, f'//input[@value="{size}"]')).click()

    def create_product(self):
        self.find_element(self.btn_create_product).click()

    def has_product(self, product_detail):
        self.driver.refresh()
        title = self.find_element(
            (By.XPATH, f'//*[text()="{product_detail["Title"]}"]'),
            clickable=False,
        )
        category = self.find_element(
            (By.XPATH, f'//*[text()="{product_detail["Category"].lower()}"]'),
            clickable=False,
        )
        return title.is_displayed() and category.is_displayed()

    def delete_product(self, product_detail):
        self.driver.refresh()
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Screenshot",
            attachment_type=AttachmentType.PNG,
        )
        self.find_element(
            (
                By.XPATH,
                f'//td[text()="{product_detail["Title"]}"]'
                "/following-sibling::td/descendant::button",
            )
        ).click()
        self.get_alert()
        logging.info("delete product success: %s", product_detail["Title"])

    def delete_all_products(self):
        self.driver.refresh()
        elements = self.find_elements(self.product_title)
        for element in elements:
            if "m" not in element.text:
                continue
            logging.info("delete generated product: %s", element.text)
            self.find_element(
                (
                    By.XPATH,
                    f'//td[text()="{element.text}"]'
                    "/following-sibling::td/descendant::button",
                )
            ).click()
            self.get_alert()
