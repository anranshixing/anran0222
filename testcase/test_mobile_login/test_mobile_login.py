# -*- coding: utf-8 -*-
# @Time    : 2022/5/13 10:31
# @Author  : SHIXING
# @FileName: test_mobile_login.py
# @Software: PyCharm
import pytest

from api.mobile_login_api import MobileLogin
from common.wrapper import add_log


class TestMobileLogin:
    """
    手机号登录测试用例
    """
    mobile_login = MobileLogin()

    mobile_login_case = mobile_login.load_yaml('data/mobile_login/mobile_login_case.yml')['mobile_login']['case']
    mobile_login_ids = mobile_login.load_yaml('data/mobile_login/mobile_login_case.yml')['mobile_login']['ids']

    @pytest.mark.parametrize('case', mobile_login_case, ids=mobile_login_ids)
    @add_log('手机号登录')
    def test_mobile_login(self, case):
        res = self.mobile_login.mobile_login(**case['data'])
        self.mobile_login.check_assert(res, case)
