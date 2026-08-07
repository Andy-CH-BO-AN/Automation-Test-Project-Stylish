from utils.page_base import PageBase
from selenium.webdriver.common.by import By


class LoginPage(PageBase):
    input_email = (By.ID, "email")
    input_password = (By.ID, "pw")
    btn_login = (By.XPATH, "//button[text()='Login']")
    btn_logout = (By.XPATH, "//button[text()='登出']")
    btn_profile = (By.CLASS_NAME, "header__link-icon-profile")

    def go_to_profile(self):
        self.find_element(self.btn_profile).click()

    def login(self, email, password):
        self.find_element(self.input_email).send_keys(email)
        self.find_element(self.input_password).send_keys(password)
        self.find_element(self.btn_login).click()

    def logout(self):
        self.find_element(self.btn_logout).click()


