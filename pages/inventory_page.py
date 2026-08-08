from pexpect import TIMEOUT
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils.slug import _slug
from pages.base_page import BasePage
from conf.settings import INVENTORY_URL, EXPLICIT_WAIT
import allure

class InventoryPage(BasePage):
    # ---- 页面元素 ----
    """由于商品数量少，且页面结构稳定才这样写元素定位
       每次调用方法，先一次性查找页面全部同类元素，存成列表，再按下标取对应元素
    """
    PAGE_TITLE      = (By.XPATH, "//span[text()='Products']")
    SORT_DROPDOWN   = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE      = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK       = (By.CLASS_NAME, "shopping_cart_link")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME       = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE      = (By.CLASS_NAME, "inventory_item_price")
    ITEM_DESC       = (By.CLASS_NAME, "inventory_item_desc")

    #创建对象自动进入商品列表页，并确认是否成功
    def __init__(self, driver,timeout=EXPLICIT_WAIT):
        super().__init__(driver,timeout)

    # ---- 页面级操作 ----
    @allure.step("进入商品列表页中")
    def open(self):
        super().open(INVENTORY_URL)
        self.is_loaded()
        allure.step("成功进入商品列表页")
        return self

    def is_loaded(self):
        return self.is_displayed(self.PAGE_TITLE)

    # ---- 商品信息获取 ----
    def get_item_count(self):
        items = self.find_all(self.INVENTORY_ITEMS)
        return len(items)

    def get_all_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_all_prices(self):
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICE)]

    # ---- 排序 ----
    @allure.step("选择排序方式: {sort_value}")
    def sort_by(self, sort_value):
        """
        sort_value 可选:
          'az'    → Name (A to Z)
          'za'    → Name (Z to A)
          'lohi'  → Price (low to high)
          'hilo'  → Price (high to low)
        """
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(sort_value)
        return self

    # ---- 购物车操作 ----
    def add_to_cart(self, product_name):
        """按商品名称点 Add to cart（SauceDemo 的 add 按钮 id 基于产品名）"""
        with allure.step(f"添加商品到购物车: {product_name}"):
            btn_id = f"add-to-cart-{_slug(product_name)}"
            self.click((By.ID, btn_id))

    def remove_from_cart(self, product_name):
        with allure.step(f"从购物车移除: {product_name}"):
            btn_id = f"remove-{_slug(product_name)}"
            self.click((By.ID, btn_id))

    def go_to_cart(self):
        self.click(self.CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    # ---- 购物车角标 ----
    def get_cart_count(self):
        if self.is_displayed(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0
