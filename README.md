# SauceDemo UI 自动化测试框架

基于 **Selenium + Pytest + Allure** 的 UI 自动化测试框架，以 [SauceDemo](https://www.saucedemo.com) 电商平台为被测对象，覆盖登录、商品浏览、购物车、结账四大核心模块。

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 开发语言 |
| Selenium 4.x | Web UI 自动化驱动 |
| Pytest 9.x | 测试框架（fixture / parametrize / hook） |
| Allure 2.x | 可视化测试报告 |
| PyYAML 6.x | 测试数据驱动 |
| webdriver-manager | ChromeDriver 版本自动管理 |

---

## 框架分层

```
┌─────────────────────────────────┐
│         Allure 报告层            │  ← 可视化报告：步骤、截图、日志
├─────────────────────────────────┤
│        Test Cases 测试层         │  ← 业务场景组装，关注"测什么"
├─────────────────────────────────┤
│        Test Data 数据层          │  ← YAML 数据驱动，新增用例不改代码
├─────────────────────────────────┤
│        Page Object 页面层        │  ← 每个页面独立管理元素定位与操作
├─────────────────────────────────┤
│        Base 基础层               │  ← WebDriverWait 封装、公共操作、失败截图
├─────────────────────────────────┤
│        Config 配置层             │  ← URL、账号、浏览器，全部支持环境变量覆盖
└─────────────────────────────────┘
```

**核心设计理念：** 元素定位、页面操作、测试逻辑、测试数据四层分离。改 UI 只改 Page Object，改数据只改 YAML，用例代码不动。

---

## 目录结构

```
saucedemo-ui-automation/
├── config/
│   ├── settings.py           # 全局配置（URL / 账号 / 浏览器 / 超时）
│   └── driver_manager.py     # WebDriver 工厂
├── pages/
│   ├── base_page.py          # 基础页（等待、点击、输入、截图）
│   ├── login_page.py         # 登录页
│   ├── inventory_page.py     # 商品列表页
│   ├── cart_page.py          # 购物车页
│   └── checkout_page.py      # 结账页（Step 1 / 2 / 3）
├── test_data/
│   ├── login_data.yaml       # 登录用例数据
│   ├── inventory_data.yaml   # 商品模块用例数据
│   ├── cart_data.yaml        # 购物车模块用例数据
│   └── checkout_data.yaml    # 结账模块用例数据
├── test_cases/
│   ├── conftest.py           # fixture（driver / logged_in_driver / 失败截图 hook）
│   ├── test_login.py         # 登录模块（5 条用例，数据驱动）
│   ├── test_inventory.py     # 商品模块（8 条用例：计数 / 排序 / 购物车操作）
│   ├── test_cart.py          # 购物车模块（4 条用例：查看 / 移除 / 跳转）
│   └── test_checkout.py      # 结账模块（5 条用例：完整流程 / 必填校验 / 取消）
├── common/
│   └── read_yaml.py          # YAML 读取工具
├── reports/                  # Allure 报告输出目录
├── pytest.ini                # Pytest 配置
├── requirements.txt          # 依赖
└── README.md
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行全部用例

```bash
pytest
```

### 3. 生成 Allure 报告

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### 4. 只跑某个模块

```bash
pytest test_cases/test_login.py        # 登录
pytest test_cases/test_inventory.py    # 商品
pytest test_cases/test_cart.py         # 购物车
pytest test_cases/test_checkout.py     # 结账
```

---

## 测试覆盖

| 模块 | 用例数 | 覆盖场景 |
|------|--------|----------|
| 登录 | 5 条 | 正常登录、错误密码、锁定用户、空用户名、空密码 |
| 商品列表 | 8 条 | 商品数量验证、4 种排序（价格升降序 / 名称升降序）、添加商品、批量添加、移除商品 |
| 购物车 | 4 条 | 验证商品名称与数量、移除商品、跳转商品页、跳转结账页 |
| 结账 | 5 条 | 完整下单流程、3 项必填校验（First Name / Last Name / Postal Code）、取消结账 |
| **合计** | **22 条** | |

数据驱动设计：登录 5 条用例共用 1 个测试函数，排序 4 种方式共用 1 个测试函数。新增用例只需在 YAML 文件中加一组数据。

---

## 配置说明

所有配置项在 `config/settings.py` 中，均支持环境变量覆盖：

```bash
# 切换浏览器为无头模式（CI 环境使用）
HEADLESS=true pytest

# 更换被测环境
BASE_URL=https://staging.example.com pytest
```

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `BASE_URL` | `https://www.saucedemo.com` | 被测系统地址 |
| `BROWSER` | `chrome` | 浏览器类型 |
| `HEADLESS` | `false` | 无头模式（true = 不显示浏览器窗口） |
| `EXPLICIT_WAIT` | `10` | 显式等待超时秒数 |
| `SCREENSHOT_ON_FAILURE` | `true` | 用例失败自动截图 |

---

## 设计决策（面试可能被问）

### Q: 为什么用 PO 模式？
元素定位集中在 Page Object 类属性中。前端改 DOM 结构时，只需改一处定位符，不影响测试用例代码。

### Q: 为什么 YAML 而不是 Excel/JSON？
YAML 可读性最好，非技术人员也能维护测试数据。pytest parametrize 原生支持字典列表，和 YAML 天然匹配。

### Q: driver fixture 为什么 scope=function？
每个用例独立的浏览器实例，用例间数据不污染。如果 scope=class 虽然更快，但一个用例的残留数据可能让另一个用例误判通过。

### Q: 失败截图怎么处理的？
`conftest.py` 注册了 `pytest_runtest_makereport` hook。任何用例在 call 阶段失败，自动截取当前页面写入 Allure 报告，不需要在每个用例里写 try/except。

---

## 被测对象说明

[SauceDemo](https://www.saucedemo.com) 是 SauceLabs 官方提供的测试练习站，有 6 个预置账号（正常、锁定、图片异常等），适合验证自动化框架的健壮性。

---

## License

MIT
