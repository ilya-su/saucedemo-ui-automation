import allure
from selenium.webdriver.common.by import By

from config.settings import CART_URL
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


class CartPage(BasePage):
    """页面元素"""
    PAGE_TITLE = (By.XPATH, "//span[text()='Your Cart']")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    INVENTORY_NAME = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    REMOVE_BUTTON = (By.XPATH, '//button[text()="Remove"]')
    CONTINUE_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("进入购物车页面中")
    def open(self):
        super().open(CART_URL)
        self.is_loaded()
        allure.step("成功进入购物车页面")
        return self

    # 是否成功进入页面
    def is_loaded(self):
        return self.is_displayed(self.PAGE_TITLE)

    @allure.step("点击continue shopping按钮,返回inventory页面")
    def continue_shopping(self):
        self.click(self.CONTINUE_BUTTON)
        return InventoryPage(self.driver)

    @allure.step("点击checkout按钮")
    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver)

    # 获取购物车信息
    def get_item_count(self):
        items = self.find_all(self.CART_ITEM)
        return len(items)

    def get_item_names(self):
        return [el.text for el in self.find_all(self.INVENTORY_NAME)]

    def get_item_price(self):
        return [float(el.text.replace("$", "")) for el in self.find_all(self.INVENTORY_PRICE)]

    def get_quantities(self):
        return [int(el.text) for el in self.find_all(self.ITEM_QUANTITY)]

    # 购物车操作
    def remove_from_cart(self, product_name):
        """按商品名移除（id 格式: remove-sauce-labs-backpack）"""
        with allure.step(f"从购物车移除: {product_name}"):
            btn_id = f"remove-{self._slug(product_name)}"
            self.click((By.ID, btn_id))

    # ---- 工具方法 ----
    @staticmethod
    def _slug(name):
        """Sauce Labs Backpack → sauce-labs-backpack"""
        return name.lower().replace(" ", "-").replace("'", "")
