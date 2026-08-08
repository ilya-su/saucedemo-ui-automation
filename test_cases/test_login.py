import allure
import pytest
from utils.read_yaml import read_yaml
from config.settings import BASE_URL
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.epic("saucedemo 测试")
@allure.feature("login 模块测试")
@pytest.mark.parametrize("case", read_yaml("login_data.yaml")["login_tests"], ids=lambda c: c["case_id"])
def test_login(driver, case):
    driver.get(BASE_URL)
    login_page = LoginPage(driver)
    login_page.login(case["username"], case["password"])

    if case["expected"] == "success":
        # 登录成功：商品页面标题可见
        assert login_page.is_displayed(InventoryPage.PAGE_TITLE)
    else:
        # 登录失败：校验错误提示文案是否符合预期
        assert case["error_msg"] in login_page.get_error_message()
