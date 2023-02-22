import inspect
import json
import os
import re
import time
from string import Template
import requests
import yaml
from jsonpath import jsonpath

from common.config import cf
from common.get_log import log


class BaseApi:
    """
    实现了所有公共类API的需要的东西,是其他API的父类
    env：运行测试的默认ip地址
    base_path: 根路径
    yam_path： api文件路径
    """
    # 这个是用yml文件管理env的方法 暂时不用 文件已删除
    # env = yaml.safe_load(open('../data/config/env.yml'))
    # raw = raw.replace('testing-studio', self.env['testing-studio'][self.env['default']])
    env = cf.get_key('env', cf.get_key('env', 'default'))
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    yml_path = os.path.join(base_path, 'data/address/api_address.yml')

    def send(self, data: dict):
        """
        封装requests代码，替代requests的get和post方法
        :data: 传入请求的字典数据，包括method，url，params，json
        :return: 响应体
        """
        req = requests.request(**data)
        return req

    def steps(self, path, t_data: dict, name):
        """
        使用模板技术，对yml文件中的变量进行二次转化
        对yml文件中的IP地址进行替换
        解决传入非必填字段的问题，非必填字段，只需要传入None值就好
        解决传入列表类型的数据问题
        :param path: 测试步骤yml文件路径
        :param t_data: Template模板里面，二次转化的数据
        :param name: yml文件读取对应的数据
        """
        with open(path, encoding="utf-8") as f:
            step = yaml.safe_load(f)[name]
            raw = json.dumps(step)
            raw = raw.replace('testing-ip', self.env)
            print(raw)
            try:
                res = Template(raw).substitute(t_data)
            except KeyError as e:
                log.error(f"api模板参数替换出错!!")
                raise e
            log.info(f"api模板改变的参数为：{t_data}")
            data = yaml.safe_load(res)
            try:
                for i in data['params'].keys():
                    if data['params'][i].startswith('[') and data['params'][i].endswith("]"):
                        data['params'][i] = eval(data['params'][i])
                    if data['params'][i] == 'None':
                        data['params'][i] = None
            except KeyError:
                pass
            try:
                for i in data['json'].keys():
                    if data['json'][i].startswith('[') and data['json'][i].endswith("]"):
                        data['json'][i] = eval(data['json'][i])
                    if data['json'][i] == 'None':
                        data['json'][i] = None
            except KeyError:
                pass
            # # 不知道哪个好一些.
            # if 'params' in data:
            #     for key, vaule in data['params'].items():
            #         if vaule.startswith('[') and vaule.endswith("]"):
            #             data['params'][key] = eval(data['params'][key])
            #         if vaule == 'None':
            #             data['params'][key] = None
            # if 'json' in data:
            #     for key, vaule in data['json'].items():
            #         if vaule.startswith('[') and vaule.endswith("]"):
            #             data['json'][key] = eval(data['json'][key])
            #         if vaule == 'None':
            #             data['json'][key] = None
            log.info(f"修改后的请求为：{data}")
            return data

    def send_steps(self, path, t_data):
        """
        封装 send和steps方法 进一步优化封装请求
        调用栈 取出栈中的第一个function 获取当前运行的函数名 优化传name的问题
        :param path: 测试步骤yml文件路径
        :param t_data: Template模板里面，二次转化的数据
        """
        name = inspect.stack()[1].function
        data = self.steps(path, t_data, name)
        res = self.send(data)
        log.info(f"响应为：{res.text}")
        # log.info(f"响应为：{res.raw}")
        return res.json()

    def get_token(self, corpid, corpsecret):
        """
        封装get_token方法 方便其他模块调用
        :param corpid: 企业ID
        :param corpsecret:应用的凭证密钥
        """
        t_data = {
            'corpid': corpid,
            'corpsecret': corpsecret
        }
        return self.send_steps(self.yml_path, t_data)['access_token']

    # # 用反射代替fixture处理token 暂时不用
    # corpid = cf.get_key('wwork', 'corpid')
    # corpsecret = cf.get_key('wwork', 'corpsecret')
    # aaa = BaseApi().get_token(corpid, corpsecret)

    @classmethod
    def load_yaml(cls, path, sub=None, sub2=None):
        """
        封装yaml读取的代码，通过路径直接读取yml文件并转化成python数据类型
        :param path: yml文件的相对路径
        :param sub: 读取yml文件的二级数据目录，默认为None
        :param sub2: 读取yml文件的三级数据目录，默认为None
        :return: 返回yml文件的python数据
        """
        path = os.path.join(cls.base_path, path)
        with open(path, encoding="utf-8") as f:
            if not sub and not sub2:
                return yaml.safe_load(f)
            if sub and not sub2:
                return yaml.safe_load(f)[sub]
            return yaml.safe_load(f)[sub][sub2]

    @classmethod
    def get_time(cls, date):
        """
        时间字符串转化成时间戳，格式：2013-10-10 23:40:00，转化成1605021256的时间戳
        :param date: 2013-10-10 23:40:00的时间格式
        :return: 返回时间戳1605021256
        """
        # 先转换成时间格式对象，再转化成时间戳
        time_strp = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_strp))
        return time_stamp

    @classmethod
    def json_path(cls, json, expr):
        """
        优化jsonpath代码，其他类就不用from jsonpath improt jsonpath了
        :param json: 传入json格式，发现json或者字典都ok也
        :param expr: 要获取json内容的表达式
        :return: 返回想要的字符串
        """
        return jsonpath(json, expr)

    @classmethod
    def save_yaml(cls, path, data):
        """
        封装yaml写入的代码
        :param path: yml文件的相对路径
        :param data: python的数据
        """
        # 链接根路径和yml文件的相对路径，简化文件路径
        path = os.path.join(cls.base_path, path)
        with open(path, "r+", encoding="utf-8", ) as f:
            yaml.safe_dump(data, f)

    @classmethod
    def check_assert(cls, response, data):
        """
        封装单接口断言的方法
        :param response: 接口响应信息
        :param data: yml文件测试用例数据
        :return:
        """
        for key, value in data['eq'].items():
            if key == 'errmsg':
                try:
                    assert value in response[key]
                except AssertionError as e:
                    log.error(f'断言错误：[{value}]   in   [{response[key]}]')
                    raise e
                except KeyError as e:
                    log.error(f'断言错误：--- 响应信息中没有{key}字段 ---')
                    raise e
            else:
                try:
                    assert value == response[key]
                except AssertionError as e:
                    log.error('断言错误：' + f'[{value}]' + '  ==  ' + f'[{response[key]}]')
                    raise e
                except KeyError as e:
                    log.error(f'断言错误：--- 响应信息中没有{key}字段 ---')
                    raise e
                # """这样写看不到具体的错误比较"""
                # if not response[key] == value:
                #     log.info('断言错误：' + f'[{value}]' + '  !=  ' + f'[{response[key]}]')
                #     raise AssertionError


if __name__ == '__main__':
    # BaseApi().get_token(corpid='ww1133aef8a95f85af', corpsecret='bgcMr2hlIE2jX69Pv1kO7Ey1vzUHkgf2nUpSrffeVIc')
    print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))