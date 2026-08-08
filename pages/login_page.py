import allure
from selenium.webdriver.common.by import By

from conf.settings import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    """元素定位"""
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    @allure.step("进入登录页面")
    def open(self):
        super().open(BASE_URL)
        return self

    def login(self, username, password):
        """登录操作：输入账号密码 -> 点击登录"""
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self  # 返回自身，支持链式调用

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
