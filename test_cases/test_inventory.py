from time import sleep

import allure
import pytest

from common.read_yaml import read
from pages.inventory_page import InventoryPage

# ====================================================================
# INV-001：商品数量验证
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("inventory 模块测试")
@allure.story("商品数量验证")
def test_product_count( logged_in_driver):
    """验证商品列表默认展示6个商品"""
    page = InventoryPage(logged_in_driver)
    count = page.get_item_count()
    assert count == 6, f"期望6个商品，实际{count}个"


# ====================================================================
# INV-002 ~ INV-005：排序
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("inventory 模块测试")
@allure.story("排序验证")
@pytest.mark.parametrize("case", read("inventory_data.yaml")["sort_tests"],
                         ids=lambda c: c["case_id"])
def test_sort(driver, case):
    """数据驱动：4种排序方式，每种验证排列顺序"""
    # 登录
    from pages.login_page import LoginPage
    LoginPage(driver).open().login("standard_user", "secret_sauce")

    page = InventoryPage(driver)
    page.sort_by(case["sort_by"])

    if case["extract"] == "prices":
        values = page.get_all_prices()
    else:
        values = page.get_all_names()

    # 验证有序性
    if case["check"] == "asc":
        assert values == sorted(values), \
            f"价格未按升序排列: {values}"
    elif case["check"] == "desc":
        assert values == sorted(values, reverse=True), \
            f"价格未按降序排列: {values}"
    elif case["check"] == "az":
        assert values == sorted(values), \
            f"名称未按A→Z排列: {values}"
    elif case["check"] == "za":
        assert values == sorted(values, reverse=True), \
            f"名称未按Z→A排列: {values}"


# ====================================================================
# INV-006 ~ INV-008：购物车操作
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("inventory 模块测试")
@allure.story("购物车操作")
@pytest.mark.parametrize("case", read("inventory_data.yaml")["cart_actions_tests"],
                         ids=lambda c: c["case_id"])
def test_cart_actions(logged_in_driver, case):
    """添加/移除商品，验证购物车角标数字是否正确"""
    page = InventoryPage(logged_in_driver)

    # 添加商品
    for product in case.get("products", []):
        page.add_to_cart(product)
    # 如果有"先添加后移除"的场景
    if "add_first" in case:
        page.add_to_cart(case["add_first"])
    if "then_remove" in case:
        page.remove_from_cart(case["then_remove"])

    # 验证角标
    actual = page.get_cart_count()
    assert actual == case["expected_count"], \
        f"期望购物车角标={case['expected_count']}，实际={actual}"

