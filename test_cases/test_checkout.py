import allure
import pytest

from utils.read_yaml import read
from pages.inventory_page import InventoryPage

@allure.epic("saucedemo 测试")
@allure.feature("checkout 模块测试")
@allure.story("完整结账成功流程")
# ====================================================================
# CHK-001：完整结账成功流程
# ====================================================================
@pytest.mark.parametrize("case", read_yaml("checkout_data.yaml")["checkout_success_tests"],
                         ids=lambda c: c["case_id"])
def test_checkout_success(logged_in_driver, case):
    """完整的结账正向流程：选商品 → 结账 → 填地址 → 确认 → 下单成功"""
    inv = InventoryPage(logged_in_driver)

    # Step 0：添加商品到购物车
    for p in case["products"]:
        inv.add_to_cart(p)

    # Step 1：进入购物车 → 点击 Checkout
    cart = inv.go_to_cart()
    checkout = cart.checkout()
    assert checkout.is_loaded(), "应进入结账 Step One 页"

    # Step 2：填写收货信息 → Continue
    s = case["shipping"]
    checkout.submit_shipping(s["first"], s["last"], s["zipcode"])
    assert checkout.is_step_two_loaded(), "应进入订单总览页 Step Two"
    # Step 3：验证金额
    checkout.verify_total()

    # Step 4：确认下单
    checkout.click_finish()
    assert checkout.is_step_three_loaded(), "应进入下单成功页"


# ====================================================================
# CHK-002 ~ CHK-004：结账表单校验
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("checkout 模块测试")
@allure.story("结账表单校验")
@pytest.mark.parametrize("case", read_yaml("checkout_data.yaml")["checkout_validation_tests"],
                         ids=lambda c: c["case_id"])
def test_checkout_validation(logged_in_driver, case):
    """结账表单必填校验：空字段 → 错误提示"""
    # 需要先添加商品才能进入结账页
    inv = InventoryPage(logged_in_driver)
    inv.add_to_cart("Sauce Labs Backpack")

    cart = inv.go_to_cart()
    checkout = cart.checkout()

    # 填信息（其中一个为空）→ 提交
    checkout.fill_info(case["first"], case["last"], case["zipcode"])
    checkout.click_continue()

    # 仍在 Step One → 验证错误信息
    assert checkout.get_error_message() == case["expected_error"], \
        f"期望错误[{case['expected_error']}]，实际[{checkout.get_error_message()}]"


# ====================================================================
# CHK-005：取消结账
# ====================================================================
@allure.epic("saucedemo 测试")
@allure.feature("checkout 模块测试")
@allure.story("取消结账")
@pytest.mark.parametrize("case", read_yaml("checkout_data.yaml")["checkout_cancel_tests"],
                         ids=lambda c: c["case_id"])
def test_checkout_cancel(logged_in_driver, case):
    """取消结账 → 返回购物车页"""
    inv = InventoryPage(logged_in_driver)

    for p in case["products"]:
        inv.add_to_cart(p)

    cart = inv.go_to_cart()
    checkout = cart.checkout()

    if case["cancel_at"] == "step_one":
        cart2 = checkout.click_cancel()
        assert cart2.is_loaded(), "取消结账应返回购物车页"
