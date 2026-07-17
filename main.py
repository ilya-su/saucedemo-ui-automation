import os
import time
import pytest

if __name__ == '__main__':


    # 1. 生成时间戳文件夹：年月日_时分秒
    time_str = time.strftime("%Y%m%d_%H%M%S")
    root_report_dir = os.path.join("reports", time_str)
    data_dir = os.path.join(root_report_dir, "allure_data")
    html_dir = os.path.join(root_report_dir, "allure_report")

    # 自动创建文件夹
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)

    # 2. 执行 pytest，动态指定 allure_dir
    # -sv 打印日志，--allure_dir 指定本次时间目录下的数据文件夹
    pytest_cmd = f"pytest -sv --alluredir={data_dir}"
    print("执行命令：", pytest_cmd)
    os.system(pytest_cmd)

    # 3. 根据本次时间目录生成 allure html 报告
    allure_cmd = f"allure generate {data_dir} -o {html_dir} --clean"
    print("生成报告命令：", allure_cmd)
    os.system(allure_cmd)