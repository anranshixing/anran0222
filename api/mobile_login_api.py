# -*- coding: utf-8 -*-
# @Time    : 2022/5/13 9:40
# @Author  : SHIXING
# @FileName: mobile_login_api.py
# @Software: PyCharm
import os

from api.base_api import BaseApi


class MobileLogin(BaseApi):
    """
    手机号登录
    """

    yml_path = os.path.join(BaseApi.base_path, 'data/mobile_login/mobile_login_api.yml')

    def mobile_login(self, **kwargs):
        return self.send_steps(self.yml_path, kwargs)
