from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """WebDriver驱动管理，按配置创建驱动实例"""
    @staticmethod
    def create_driver(browser="chrome", headless=True):
        if browser == "chrome":
            # service = Service(ChromeDriverManager().install())
            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            # ========== 禁用保存密码弹窗 ==========
            prefs = {
                # 关闭密码管理器
                "profile.password_manager_enabled": False,
                # 关闭凭据存储服务
                "credentials_enable_service": False,
                # 额外：关闭密码泄露安全提示（可选）
                "profile.enabled_password_breach_detection": False,
                # 关闭自动填充地址、信用卡弹窗（可选）
                "autofill.profile_enabled": False,
                "autofill.credit_card_enabled": False
            }
            options.add_experimental_option("prefs", prefs)
            # 去掉 "Chrome正在被自动化测试软件控制" 提示条
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            return webdriver.Chrome(options=options)
        # 扩展：可加 Firefox、Edge
        raise ValueError(f"Unsupported browser: {browser}")