import allure
import pytest
from utils.driver_manager import DriverManager
from config.settings import BASE_URL, HEADLESS, TEST_USER, TEST_PASS
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def driver():
    """每个测试用例独立的driver实例"""
    # 环境变量默认启动无头模式
    drv = DriverManager.create_driver(headless=HEADLESS)
    yield drv
    drv.quit()  # 用例结束自动关闭浏览器

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """已登录的driver —— 公共前置"""
    driver.get(BASE_URL)
    login_page = LoginPage(driver)
    with allure.step("标准账号登录"):
        login_page.login(TEST_USER,TEST_PASS)
    return driver

"""hookwrapper=True：钩子包装器，支持yield分割前后逻辑"""
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """用例失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    # 只在用例执行阶段失败才截图（排除setup/teardown阶段报错）
    if report.when == "call" and report.failed:
        # 取出当前用例的浏览器driver固件
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver:
            try:
                # 直接截图写入allure报告
                allure.attach(driver.get_screenshot_as_png(), f"报错截图_{item.name}", allure.attachment_type.PNG)
            except Exception:
                pass

