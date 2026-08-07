import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils.page_base import PageBase


class CartPage(PageBase):
    DELIVERY_TIMES = {
        "Anytime": "不指定",
        "Morning": "08:00-12:00",
        "Afternoon": "14:00-18:00",
    }

    cart_name = (By.CLASS_NAME, "cart__item-name")
    cart_id = (By.CLASS_NAME, "cart__item-id")
    cart_price = (By.CLASS_NAME, "cart__item-price-content")
    cart_color = (By.CLASS_NAME, "cart__item-color")
    cart_size = (By.CLASS_NAME, "cart__item-size")
    cart_qty = (By.CLASS_NAME, "cart__item-quantity-selector")
    cart_subtotal = (By.CLASS_NAME, "cart__item-subtotal-content")
    btn_checkout = (By.CLASS_NAME, "checkout-button")
    input_customer_name = (By.XPATH, '//div[text()="收件人姓名"]/following-sibling::input')
    input_customer_email = (By.XPATH, '//div[text()="Email"]/following-sibling::input')
    input_customer_phone = (By.XPATH, '//div[text()="手機"]/following-sibling::input')
    input_customer_address = (By.XPATH, '//div[text()="地址"]/following-sibling::input')
    input_customer_card_number = (By.ID, "cc-number")
    customer_card_number_iframe = (By.XPATH, '//div[@id="card-number"]/iframe')
    input_customer_card_exp_date = (By.ID, "cc-exp")
    customer_card_exp_date_iframe = (By.XPATH, '//div[@id="card-expiration-date"]/iframe')
    input_customer_card_ccv = (By.ID, "cc-ccv")
    customer_card_ccv_iframe = (By.XPATH, '//div[@id="card-ccv"]/iframe')

    @classmethod
    def normalize_delivery_time(cls, delivery_time):
        logging.info("delivery_time: %s", delivery_time)
        return cls.DELIVERY_TIMES.get(delivery_time)

    def get_cart_info(self):
        product_names = self.find_elements(self.cart_name)
        product_ids = self.find_elements(self.cart_id)
        product_prices = self.find_elements(self.cart_price)
        product_colors = self.find_elements(self.cart_color)
        product_sizes = self.find_elements(self.cart_size)
        product_quantities = self.find_elements(self.cart_qty)

        cart_details = []
        for index, product_name in enumerate(product_names):
            detail = {
                "product_name": product_name.text,
                "product_id": product_ids[index].text,
                "product_price": product_prices[index].text.split("\n")[-1].split(".")[-1],
                "product_color": product_colors[index].text.split("｜")[-1],
                "product_size": product_sizes[index].text.split("｜")[-1],
                "product_qty": product_quantities[index].text.split("\n")[0],
            }
            cart_details.append(detail)
            logging.info("cart_detail: %s", detail)
        return cart_details

    def delete_cart_by_product_id(self, product_id):
        logging.info("delete cart product: %s", product_id)
        locator = (
            By.XPATH,
            f"//*[text()='{product_id}']/ancestor::*[@class='cart__item']"
            "/descendant::*[@class='cart__delete-button']",
        )
        self.find_element(locator).click()

    def edit_cart_quantity(self, qty):
        Select(self.find_element(self.cart_qty)).select_by_visible_text(qty)

    def get_cart_subtotal(self):
        subtotal = self.find_element(self.cart_subtotal).text.split(".")[-1]
        logging.info("sub_total: %s", subtotal)
        return subtotal

    def click_checkout_button(self):
        self.find_element(self.btn_checkout).click()

    def fill_checkout_form(self, customer_detail):
        normalized = dict(customer_detail)
        delivery_time = self.normalize_delivery_time(normalized["Deliver Time"])
        normalized["Deliver Time"] = delivery_time

        self.find_element(self.input_customer_name).send_keys(normalized["Receiver"])
        self.find_element(self.input_customer_email).send_keys(normalized["Email"])
        self.find_element(self.input_customer_phone).send_keys(normalized["Mobile"])
        self.find_element(self.input_customer_address).send_keys(normalized["Address"])

        if delivery_time is not None:
            self.find_element((By.XPATH, f'//*[text()="{delivery_time}"]')).click()

        self._fill_iframe(self.customer_card_number_iframe, self.input_customer_card_number, normalized["Credit Card No"])
        self._fill_iframe(self.customer_card_exp_date_iframe, self.input_customer_card_exp_date, normalized["Expiry Date"])
        self._fill_iframe(self.customer_card_ccv_iframe, self.input_customer_card_ccv, normalized["Security Code"])
        return normalized

    def _fill_iframe(self, iframe_locator, input_locator, value):
        self.driver.switch_to.frame(self.find_element(iframe_locator))
        try:
            self.find_element(input_locator).send_keys(value)
        finally:
            self.driver.switch_to.default_content()

    def checkout_summary_contains(self, customer_info):
        delivery_time = customer_info["Deliver Time"].replace("-", " - ")
        expected_values = [
            customer_info["Receiver"],
            customer_info["Email"],
            customer_info["Mobile"],
            customer_info["Address"],
            delivery_time,
        ]
        for value in expected_values:
            if not self.find_element((By.XPATH, f'//*[text()="{value}"]')).is_displayed():
                return False
        return True
