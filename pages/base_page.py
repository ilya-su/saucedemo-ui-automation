import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf.settings import EXPLICIT_WAIT


class BasePage:
    ##基础页面父类（封装公共操作）
    def __init__(self, driver, timeout=EXPLICIT_WAIT):
        self.driver = driver
        self.timeout = timeout

    @property
    def wait(self):
        return WebDriverWait(self.driver, self.timeout)

    def open(self, url):
        with allure.step(f"打开页面：{url}"):
            self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def find(self, locator):
        """等待元素可见后返回"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        with allure.step(f"点击元素：{locator}"):
            self.wait.until(EC.element_to_be_clickable(locator)).click()

    def input_text(self, locator, text):
        with allure.step(f"输入文本: {text}"):
            element = self.find(locator)
            element.clear()
            element.send_keys(text)

    def get_text(self, locator):
        """获取元素后返回文本"""
        return self.find(locator).text

    def is_displayed(self, locator):
        """
        等待元素可见，返回布尔值
        :param locator: 定位元组 (by, value)
        :return: True可见 / False不可见/不存在
        """
        try:
            # 等待元素可见，最多等self.timeout秒
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            # 超时、找不到、元素隐藏都会进这里
            return False

    def screenshot(self, name):
        """截屏捕获"""
        with allure.step("截屏："):
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=name,
                          attachment_type=allure.attachment_type.PNG)
