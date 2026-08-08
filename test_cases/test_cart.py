import allure
import pytest

from common.read_yaml import read_yaml
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


# ====================================================================
# CART-001 ~ CART-002：购物车模块
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("cart 模块测试")
@allure.story("购物车模块")
@pytest.mark.parametrize("case", read_yaml("cart_data.yaml")["cart_tests"],
                         ids=lambda c: c["case_id"])
def test_cart(logged_in_driver, case):
    """购物车操作：添加商品→进入购物车→验证"""
    inv = InventoryPage(logged_in_driver)
    # 添加商品
    for p in case.get("add_products", []):
        inv.add_to_cart(p)

    # 进入购物车
    cart = inv.go_to_cart()
    assert cart.is_loaded(), "应成功进入购物车页"

    # 移除商品
    if "remove" in case:
        cart.remove_from_cart(case["remove"])

    # 验证
    count = cart.get_item_count()
    assert count == case["expected_count"], f"""
        期望{case["expected_count"]}件商品，实际{count}件
    """

    # 不实用，实际上商品名称的顺序可能填反
    # if "expected_names" in case:
    #     names = cart.get_item_names()
    #     assert names == case["expected_names"], \
    #         f"商品名称不匹配: 期望{case['expected_names']}，实际{names}"

    if "expected_names" in case:
        names = set(cart.get_item_names())
        expect_names = set(case["expected_names"])
        assert names == expect_names, f"""
            商品名称不匹配：期望{expect_names},实际{names}
        """


# ====================================================================
# CART-003 ~ CART-004：购物车状态跳转
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("cart 模块测试")
@allure.story("购物车的状态流转")
@pytest.mark.parametrize("case", read_yaml("cart_data.yaml")["cart_flow"],
                         ids=lambda c: c["case_id"])
def test_cart_flow(logged_in_driver, case):
    """购物车页面的状态跳转：返回商品列表，结账跳转"""
    cart = CartPage(logged_in_driver)
    cart.open()
    if case["do"] == "check":
        cart.checkout()
        check = CheckoutPage(logged_in_driver)
        assert check.is_loaded(), "进入结账页面失败"
    elif case["do"] == "continue":
        cart.continue_shopping()
        inve = InventoryPage(logged_in_driver)
        assert inve.is_loaded(), "返回商品列表页面失败"
