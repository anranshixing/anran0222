import json
import re


class CheckUtils:
    def __init__(self, response_data=None):
        self.response_data = response_data
        self.check_types = {
            'none': self.__none_check,
            'json_key': self.__json_key_check,
            'json_key_value': self.__json_key_value_check,
            'body_regexp': self.__body_regexp_check,
            'response_code': self.__response_code_check,
            'header_key': self.__header_key_check,
            'header_key_value': self.__header_key_value_check
        }
        self.pass_result = {
            'code': 0,
            'response_code': self.response_data.status_code,
            'response_reason': self.response_data.reason,
            'response_headers': self.response_data.headers,
            'response_body': self.response_data.text,
            'message': '测试用例执行通过',
            'check_result': True
        }
        self.fail_result = {
            'code': 2,
            'response_code': self.response_data.status_code,
            'response_reason': self.response_data.reason,
            'response_headers': self.response_data.headers,
            'response_body': self.response_data.text,
            'message': '测试用例断言失败，执行不通过',
            'check_result': False
        }

    def __none_check(self):
        return self.pass_result

    def __json_key_check(self, check_data):
        ''' 当响应正文为json时，比对是否包含键，支持多个键比较 '''
        key_list = check_data.split(",")
        tmp_result = []
        for key in key_list:
            if key in self.response_data.json().keys():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def __json_key_value_check(self, check_data):
        ''' 当响应正文为json时，比对是否包含键值对，支持多个键值对比较 '''
        check_data_dict = json.loads(check_data)
        tmp_result = []
        for item in check_data_dict.items():
            if item in self.response_data.json().items():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def __body_regexp_check(self, check_data):
        if re.findall(check_data, self.response_data.text):
            return self.pass_result
        else:
            return self.fail_result

    def __response_code_check(self, check_data):
        if self.response_data.status_code == int(check_data):
            return self.pass_result
        else:
            return self.fail_result

    def __header_key_check(self, check_data):
        key_list = check_data.split(",")
        tmp_result = []
        for key in key_list:
            if key in self.response_data.headers.keys():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def __header_key_value_check(self, check_data):
        check_data_dict = json.loads(check_data)
        tmp_result = []
        for item in check_data_dict.items():
            if item in self.response_data.headers.items():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
        if False in tmp_result:
            return self.fail_result
        else:
            return self.pass_result

    def run_check(self, check_type, check_data):
        if check_type == 'none' or check_data == '':
            result = self.check_types['none']()
            return result
        elif check_type in self.check_types.keys():
            result = self.check_types[check_type](check_data)  # self.json_key_check()
            return result
        else:
            return self.fail_result


if __name__=='__main__':
    import requests
    url_params = {"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}
    response = requests.get(url='https://api.weixin.qq.com/cgi-bin/token',
                            params= url_params )
    # result = CheckUtils(response).json_key_check( 'access_token' )
    # print( result )
    # result = CheckUtils(response).json_key_value_check( '{"expires_in":7200}' )
    # print( result )
    # result = CheckUtils(response).body_regexp_check('"access_token":"(.+?)"')
    # print( result )

    result = CheckUtils(response).run_check( 'header_key_value','{"Connection":"keep-alive"}' )
    print( result )

    # data['json']['access_token'] = token
    # res = self.experience_order.create_user(**data)
    # self.experience_order.check(res, data)
    # if res['errmsg'] == 'created':
    #     data11 = {'json': {'access_token': token, 'userid': data['json']['userid']}}
    #     assert self.experience_order.get_user(**data11)['userid'] == data['json']['userid']