import os
from pathlib import Path

# ── 项目根目录 ──
ROOT_DIR = Path(__file__).resolve().parent.parent

# ── 被测环境 ──
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
INVENTORY_URL = os.getenv("INVENTORY_URL", "https://www.saucedemo.com/inventory.html")
CART_URL = os.getenv("CART_URL", "https://www.saucedemo.com/cart.html")
CHECKOUT_ONE_URL = os.getenv("CHECKOUT_URL", "https://www.saucedemo.com/checkout-step-one.html")
CHECKOUT_TWO_URL = os.getenv("CHECKOUT_TWO_URL", "https://www.saucedemo.com/checkout-step-two.html")
CHECKOUT_COMPLETE_URL = os.getenv("CHECKOUT_TWO_URL", "https://www.saucedemo.com/checkout-complete.html")


# ── 测试账号 ──
TEST_USER = os.getenv("TEST_USER", "standard_user")
TEST_PASS = os.getenv("TEST_PASS", "secret_sauce")

# ── 浏览器配置 ──
BROWSER  = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# ── 超时配置（秒） ──
IMPLICIT_WAIT  = int(os.getenv("IMPLICIT_WAIT",  "10"))
EXPLICIT_WAIT  = int(os.getenv("EXPLICIT_WAIT",  "10"))
PAGE_LOAD_WAIT = int(os.getenv("PAGE_LOAD_WAIT", "30"))

# ── 报告路径 ──
ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", str(ROOT_DIR / "reports" / "allure-results"))
HTML_REPORT_PATH   = os.getenv("HTML_REPORT_PATH",   str(ROOT_DIR / "reports" / "report.html"))

# ── 截图配置 ──
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"