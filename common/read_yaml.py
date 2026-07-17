import yaml

from config.settings import ROOT_DIR

"""读取yaml文件的方法，直接填yaml文件的名字 ， 如：login.yaml"""
def read(file):
    file = ROOT_DIR / 'test_data' / file
    with open(file, 'r', encoding='utf-8') as f:
        values = yaml.safe_load(f)
    return values