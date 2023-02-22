# -*- coding: utf-8 -*-
# @Time    : 2022/5/13 11:10
# @Author  : SHIXING
# @FileName: conftest.py
# @Software: PyCharm



# 解决pytest参数化的标题,修改测试用例名称中文编码,utf-8转换为unicode;
# 自动添加标签
import pytest


def pytest_collection_modifyitems(session, config, items: list):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        if 'get_user' in item.nodeid:
            item.add_marker(pytest.mark.get_user)
        if 'create_user' in item.nodeid:
            item.add_marker(pytest.mark.create_user)