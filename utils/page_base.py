import logging
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageBase:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def find_element(self, locator, clickable=True):
        if not clickable:
            return self.wait.until(EC.visibility_of_element_located(locator))
        else:
            return self.wait.until(EC.element_to_be_clickable(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def scroll_down(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

    def get_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        return alert_text

    def get_jwt_token(self):
        jwt_token = self.driver.execute_script("return window.localStorage.getItem('jwtToken');")
        logging.info(jwt_token)
        return jwt_token

    def set_jwt_token(self, jwt_token):
        logging.info(jwt_token)
        self.driver.execute_script(f"return window.localStorage.setItem('jwtToken', '{jwt_token}');")
