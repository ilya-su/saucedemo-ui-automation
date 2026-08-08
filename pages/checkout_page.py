import allure
from selenium.webdriver.common.by import By

from conf.settings import CHECKOUT_ONE_URL, EXPLICIT_WAIT
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
        结账流程的三个页面：
          - Step One: 填写收货信息（/checkout-step-one.html）
          - Step Two: 确认订单总览（/checkout-step-two.html）
          - Complete:  下单成功（/checkout-complete.html）
    """
    CANCEL_BUTTON = (By.ID, 'cancel')
    CONTINUE_BUTTON = (By.ID, 'continue')
    """step-one"""
    STEP_ONE_TITLE = (By.XPATH, '//span[text()="Checkout: Your Information"]')
    FIRSTNAME_INPUT = (By.ID, 'first-name')
    LASTNAME_INPUT = (By.ID, 'last-name')
    POSTAL_CODE_INPUT = (By.ID, 'postal-code')
    ERROR_MESSAGE = (By.XPATH, '//div[@class="error-message-container error"]/h3')
    """step-two"""
    STEP_TWO_TITLE = (By.XPATH, '//span[text()="Checkout: Overview"]')
    ITEM_TOTAL = (By.CLASS_NAME, 'summary_subtotal_label')
    TAX = (By.CLASS_NAME, 'summary_tax_label')
    TOTAL = (By.CLASS_NAME, 'summary_total_label')
    FINISH_BUTTON = (By.ID, 'finish')
    """step-three"""
    STEP_THREE_TITLE = (By.XPATH, '//span[text()="Checkout: Complete!"]')
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver,timeout=EXPLICIT_WAIT):
        super().__init__(driver,timeout)

    """step-one 操作"""

    @allure.step("进入checkout页面中")
    def open(self):
        super().open(CHECKOUT_ONE_URL)
        self.is_loaded()
        allure.step("成功进入checkout-step-one页面")
        return self

    def is_loaded(self):
        return self.is_displayed(self.STEP_ONE_TITLE)

    @allure.step("填写收货信息：{firstname}/{lastname}/{postal_code}")
    def fill_info(self, firstname, lastname, postal_code):
        self.input_text(self.FIRSTNAME_INPUT, firstname)
        self.input_text(self.LASTNAME_INPUT, lastname)
        self.input_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    @allure.step("点击continue按钮")
    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    @allure.step("点击cancel按钮")
    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    """快捷操作：一次填完收获信息并提交"""

    def submit_shipping(self, firstname, lastname, postal_code):
        """填信息 + 点 Continue → 进入 Step Two"""
        self.fill_info(firstname, lastname, postal_code)
        self.click_continue()
        return self

    """step-two 操作"""

    def is_step_two_loaded(self):
        return self.is_displayed(self.STEP_TWO_TITLE)

    @allure.step("获取item_total")
    def get_item_total(self):
        return float(self.get_text(self.ITEM_TOTAL).split('$')[1])

    @allure.step("获取tax")
    def get_item_tax(self):
        return float(self.get_text(self.TAX).split('$')[1])

    @allure.step("获取total")
    def get_total(self):
        return float(self.get_text(self.TOTAL).split('$')[1])

    @allure.step("验证金额计算：total=item_total+tax")
    def verify_total(self):
        """验证明细加总是否正确"""
        item_total = self.get_item_total()
        tax = self.get_item_tax()
        total = self.get_total()
        expected = round(item_total + tax, 2)
        assert total == expected, f"""
            item_total: {item_total}
            tax: {tax}
            total: {total}
            {item_total}+{tax} != {total}
        """
        return True

    @allure.step("点击finish完成下单")
    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        return self

    """step-three 操作"""
    def is_step_three_loaded(self):
        return self.is_displayed(self.STEP_THREE_TITLE)

    @allure.step("点击back home返回首页")
    def click_back_home(self):
        self.click(self.BACK_HOME_BUTTON)
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)