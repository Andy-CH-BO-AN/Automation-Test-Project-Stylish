import logging
import os

import allure
from allure_commons.types import AttachmentType

from utils.page_base import PageBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class AdminPage(PageBase):
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
        self.driver.get(os.getenv("DOMAIN") + "/admin/products.html")

    def go_to_create_product_page(self):
        self.find_element(self.btn_go_to_create_product).click()
        create_product_page = self.driver.window_handles[1]
        self.driver.switch_to.window(create_product_page)

    def input_product_detail(self, product_detail):
        logging.info(product_detail)
        select_category_element = self.find_element(self.select_category)
        Select(select_category_element).select_by_visible_text(product_detail['Category'])
        self.find_element(self.input_title).send_keys(product_detail['Title'])
        self.find_element(self.textarea_description).send_keys(product_detail['Description'])
        self.find_element(self.input_price).send_keys(product_detail['Price'])
        self.find_element(self.input_texture).send_keys(product_detail['Texture'])
        self.find_element(self.input_wash).send_keys(product_detail['Wash'])
        self.find_element(self.input_place_of_production).send_keys(product_detail['Place of Product'])
        self.find_element(self.input_note).send_keys(product_detail['Note'])

        for color in product_detail['Colors'].split(", "):
            self.select_color(color)

        for size in product_detail['Sizes'].split(", "):
            self.select_size(size)

        self.find_element(self.input_story).send_keys(product_detail['Story'])

        test_data_path = os.path.abspath('test_data')
        logging.info(test_data_path)
        if product_detail['Main Image'] != '':
            self.find_element(self.input_main_image).send_keys(f"{test_data_path}/Stylish_product_image/mainImage.jpg")
        input_images = self.find_elements(self.input_other_images)
        if product_detail['Other Image 1'] != '':
            input_images[0].send_keys(f"{test_data_path}/Stylish_product_image/otherImage0.jpg")
        if product_detail['Other Image 2'] != '':
            input_images[1].send_keys(f"{test_data_path}/Stylish_product_image/otherImage1.jpg")
        allure.attach(self.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    def select_color(self, color):
        logging.info(f'color: "{color}"]')
        if color != '':
            if color == "全選":
                elements = self.find_elements(self.checkbox_colors)
                for element in elements:
                    element.click()
            else:
                checkbox_color = self.find_element((By.XPATH, f'//label[text()=" {color} "]/preceding-sibling::input'))
                checkbox_color.click()
        else:
            pass

    def select_size(self, size):
        logging.info(f'size: "{size}"]')
        if size != '':
            if size == "全選":
                elements = self.find_elements(self.checkbox_sizes)
                for element in elements:
                    element.click()
            else:
                checkbox_size = self.find_element((By.XPATH, f'//input[@value="{size}"]'))
                checkbox_size.click()
        else:
            pass

    def create_product(self):
        self.find_element(self.btn_create_product).click()

    def verify_product_info_in_admin(self, product_detail):
        self.driver.refresh()
        logging.info(f'//td[text()="{product_detail["Category"]}"]')
        product_title = self.find_element(
            (By.XPATH, f'//*[text()="{product_detail["Title"]}"]')
            , clickable=False)
        product_title.is_displayed()

        product_category = self.find_element(
            (By.XPATH, f'//*[text()="{product_detail["Category"].lower()}"]'
             ), clickable=False)
        product_category.is_displayed()

    def delete_product(self, product_detail):
        self.driver.refresh()
        allure.attach(self.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

        element = self.find_element(
            (By.XPATH, f'//td[text()="{product_detail["Title"]}"]/following-sibling::td/descendant::button')
        )
        if "m" in element.text:
            element.click()
            logging.info("delete product success")
        self.get_alert()

    def delete_all_products(self):
        self.driver.refresh()
        allure.attach(self.driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

        elements = self.find_elements(self.product_title)
        for element in elements:
            if "m" in element.text:
                logging.info("Need to delete product.")
                self.find_element(
                    (By.XPATH, f'//td[text()="{element.text}"]/following-sibling::td/descendant::button')
                ).click()
                self.get_alert()
