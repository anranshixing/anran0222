import six

from common.get_log import log

# num = 1
# test_id = set()


# # 定义测试用例的日志处理wrapper
# def add_log(name):
#     def insert_log(func):
#         @six.wraps(func)
#         def wrapper(*args, **kwargs):
#             global num
#             global test_id
#             a = len(test_id)
#             test_id.add(name)
#             if len(test_id) > a:
#                 num = 1
#             if not kwargs:
#                 num = 0
#                 log.info(f'------开始测试:--[{name}]--用例输入：{kwargs}------')
#             else:
#                 log.info(f'[{num}]------开始测试:--[{name}]--用例输入：{kwargs}------')
#             try:
#                 data = func(*args, **kwargs)
#             except AssertionError as e:
#                 log.error(f'---------{name}-用例[{num}]-测试失败------')
#                 raise e
#             else:
#                 log.info(f'---------测试通过------')
#             finally:
#                 num += 1
#             return data
#
#         return wrapper
#
#     return insert_log

#
# def add_log(name):
#     def insert_log(func):
#         @six.wraps(func)
#         def wrapper(*args, **kwargs):
#             log.info(f'------开始测试：{name}, 用例输入：{kwargs}------')
#             try:
#                 data = func(*args, **kwargs)
#             except Exception as e:
#                 log.error(f'------{name}测试失败------')
#                 raise e
#             else:
#                 log.info(f'------测试通过------')
#             return data
#         return wrapper
#     return insert_log

def add_log(name):
    def insert_log(func):
        @six.wraps(func)
        def wrapper(*args, **kwargs):
            if not kwargs:
                log.info(f'------测试前准备:{name}------')
            else:
                log.info(f'------开始测试：{name}------')
            try:
                data = func(*args, **kwargs)
            except Exception as e:
                log.error(f'------{name}测试失败------')
                raise e
            else:
                if not kwargs:
                    log.info(f'------{name}成功------')
                else:
                    log.info(f'------测试通过------')
            return data

        return wrapper

    return insert_log
