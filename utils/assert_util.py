import allure


class AssertUtil:

    @staticmethod
    def assert_equal(actual, expected, msg: str = None):
        """相等断言"""
        with allure.step(f"断言：预期={expected},实际={actual}"):
            message = msg or f"【相等断言失败】预期：{expected},实际：{actual}"
        assert actual == expected, message

    @staticmethod
    def assert_not_equal(actual, expected, msg: str = None):
        """不相等断言"""
        with allure.step(f"断言：实际 {actual} 不等于 {expected}"):
            message = msg or f"【不相等断言失败】不预期：{expected}，实际：{actual}"
        assert actual != expected, message

    @staticmethod
    def assert_contains(actual: str, expect_sub: str, msg: str = None):
        """断言文本包含期望值"""
        with allure.step(f"断言：预期={expect_sub}，实际={actual}"):
            message = msg or f"【包含断言失败】实际文本[{actual}] 未包含 [{expect_sub}]"
        assert expect_sub in actual, message

    @staticmethod
    def assert_not_contains(actual: str, expect_sub: str, msg: str = None):
        """实际文本不包含期望值"""
        with allure.step(f"断言：'{actual}' 不包含 '{expect_sub}'"):
            message = msg or f"【不包含断言失败】实际文本[{actual}] 意外包含 [{expect_sub}]"
        assert expect_sub not in actual, message

    @staticmethod
    def assert_true(condition: bool, msg: str = None):
        """断言为True"""
        message = msg or f"【True断言失败】条件结果为 {condition}"
        assert condition is True, message

    @staticmethod
    def assert_false(condition: bool, msg: str = None):
        """断言为False"""
        message = msg or f"【False断言失败】条件结果为 {condition}"
        assert condition is False, message

    @staticmethod
    def assert_not_none(value, msg: str = None):
        """不为None"""
        message = msg or f"【非空断言失败】值为 None"
        assert value is not None, message

    @staticmethod
    def assert_none(value: Any, msg: str = None):
        """为None"""
        message = msg or f"【None断言失败】实际值：{value}"
        assert value is None, message

    @staticmethod
    def assert_list_contains(target_list: list, item, msg: str = None):
        """列表包含某个元素"""
        message = msg or f"【列表包含断言失败】列表 {target_list} 不存在元素 {item}"
        assert item in target_list, message

    @staticmethod
    def assert_list_length(target_list: list, expect_len: int, msg: str = None):
        """校验列表长度"""
        real_len = len(target_list)
        message = msg or f"【列表长度断言失败】预期长度:{expect_len},实际:{real_len},列表:{target_list}"
        assert real_len == expect_len, message

