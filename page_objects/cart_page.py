import logging

from utils.page_base import PageBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class CartPage(PageBase):
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
    input_customer_card_number = (By.ID, 'cc-number')
    customer_card_number_iframe = (By.XPATH, '//div[@id="card-number"]/iframe')
    input_customer_card_exp_date = (By.ID, 'cc-exp')
    customer_card_exp_date_iframe = (By.XPATH, '//div[@id="card-expiration-date"]/iframe')
    input_customer_card_ccv = (By.ID, 'cc-ccv')
    customer_card_ccv_iframe = (By.XPATH, '//div[@id="card-ccv"]/iframe')

    def customer_delivery_time(self, delivery_time):
        logging.info(f"delivery_time: {delivery_time}")
        if delivery_time == "Anytime":
            return "不指定"
        elif delivery_time == "Morning":
            return "08:00-12:00"
        elif delivery_time == "Afternoon":
            return "14:00-18:00"

    def get_cart_info(self):
        cart_detail_list = []
        product_name = self.find_elements(self.cart_name)
        product_id = self.find_elements(self.cart_id)
        product_price = self.find_elements(self.cart_price)
        product_color = self.find_elements(self.cart_color)
        product_size = self.find_elements(self.cart_size)
        product_qty = self.find_elements(self.cart_qty)
        for i in range(len(product_name)):
            cart_detail = {
                "product_name": product_name[i].text,
                "product_id": product_id[i].text,
                "product_price": product_price[i].text.split("/n")[-1].split(".")[-1],
                "product_color": product_color[i].text.split("｜")[-1],
                "product_size": product_size[i].text.split("｜")[-1],
                "product_qty": product_qty[i].text.split("\n")[0]
            }
            cart_detail_list.append(cart_detail)
            logging.info(f"cart_detail: {cart_detail}")
        return cart_detail_list

    def delete_cart_by_product_id(self, product_id):
        logging.info(product_id)
        self.find_element((By.XPATH, f"//*[text()='{product_id}']/ancestor::*[@class='cart__item']/descendant::*["
                                     f"@class='cart__delete-button']")).click()

    def edit_cart_quantity(self, qty):
        cart_qty = self.find_element(self.cart_qty)
        Select(cart_qty).select_by_visible_text(qty)

    def get_cart_subtotal(self):
        sub_total = self.find_element(self.cart_subtotal).text.split(".")[-1]
        logging.info(f"sub_total: {sub_total}")
        return sub_total

    def click_checkout_button(self):
        self.find_element(self.btn_checkout).click()

    def input_check_out_detail(self, customer_detail):
        delivery_time = self.customer_delivery_time(customer_detail["Deliver Time"])
        customer_detail["Deliver Time"] = delivery_time
        logging.info(customer_detail)

        self.find_element(self.input_customer_name).send_keys(customer_detail["Receiver"])
        self.find_element(self.input_customer_email).send_keys(customer_detail["Email"])
        self.find_element(self.input_customer_phone).send_keys(customer_detail["Mobile"])
        self.find_element(self.input_customer_address).send_keys(customer_detail["Address"])

        if delivery_time is not None:
            self.find_element((By.XPATH, f'//*[text()="{delivery_time}"]')).click()
        else:
            pass

        self.driver.switch_to.frame(self.find_element(self.customer_card_number_iframe))
        self.find_element(self.input_customer_card_number).send_keys(customer_detail["Credit Card No"])
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.find_element(self.customer_card_exp_date_iframe))
        self.find_element(self.input_customer_card_exp_date).send_keys(customer_detail["Expiry Date"])
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.find_element(self.customer_card_ccv_iframe))
        self.find_element(self.input_customer_card_ccv).send_keys(customer_detail["Security Code"])
        self.driver.switch_to.default_content()
        return customer_detail

    def verify_check_out_info(self, customer_info):
        customer_name = self.find_element((By.XPATH, f'//*[text()="{customer_info["Receiver"]}"]'))
        customer_name.is_displayed()
        customer_name = self.find_element((By.XPATH, f'//*[text()="{customer_info["Email"]}"]'))
        customer_name.is_displayed()
        customer_name = self.find_element((By.XPATH, f'//*[text()="{customer_info["Mobile"]}"]'))
        customer_name.is_displayed()
        customer_name = self.find_element((By.XPATH, f'//*[text()="{customer_info["Address"]}"]'))
        customer_name.is_displayed()
        customer_info["Deliver Time"] = customer_info["Deliver Time"].replace("-", " - ")
        customer_name = self.find_element((By.XPATH, f'//*[text()="{customer_info["Deliver Time"]}"]'))
        customer_name.is_displayed()
