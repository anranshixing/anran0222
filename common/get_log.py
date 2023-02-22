import datetime
import logging
import os

from common.config import cf


class MyLog:
    """
    获取Log日志封装的类
    formatter：设置日志输出格式
    BASE_PATH：项目的根路径
    log_mode: 通过配置文件，获取log是w模式还是a的追加模式
    name: 生成日期：创造log_2020-12-03.log文件
    filename: 最终的文件名称和路径，在根路径的logs文件夹下
    """
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息:%(message)s')
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_mode = cf.get_key("logs", "file_mode")
    name = "log_" + str(datetime.date.today()) + ".log"
    filename = os.path.join(BASE_PATH, "logs", name)

    def __init__(self, name='test'):
        """
        定义和对接收集器，输出渠道
        :param name: 名称
        """
        # 定义一个日志收集器 my_logger, 设置收集日志级别
        self.logger = logging.getLogger(name)
        self.logger.setLevel('DEBUG')
        # 创建输出渠道 StreamHandler, 设置输出日志级别和格式
        self.ch = logging.StreamHandler()
        self.ch.setLevel('DEBUG')
        self.ch.setFormatter(self.formatter)
        # 创建输出渠道 FileHandler, 设置输出日志级别, 设置输出格式
        self.fh = logging.FileHandler(filename=self.filename, mode=self.log_mode, encoding='utf-8')
        self.fh.setLevel('DEBUG')
        self.fh.setFormatter(self.formatter)
        # 两者对接--指定输出渠道
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)

    def get_log(self):
        # 返回记录器, 拥有文件和流的处理器和格式，可以输出日志了
        return self.logger

    def close_log(self):
        # 关闭日志收集器, 单例模式需全部测试结束后再用
        self.logger.removeHandler(self.ch)
        self.logger.removeHandler(self.fh)

    # def my_log(self, msg, level):
    #     # 收集日志
    #     if level == 'DEBUG':
    #         self.logger.debug(msg)
    #     if level == 'INFO':
    #         self.logger.info(msg)
    #     if level == 'WARNING':
    #         self.logger.warning(msg)
    #     if level == 'ERROR':
    #         self.logger.error(msg)
    #     if level == 'CRITICAL':
    #         self.logger.critical(msg)
    #
    # def debug(self, msg):
    #     self.my_log(msg, 'DEBUG')
    #
    # def info(self, msg):
    #     self.my_log(msg, 'INFO')
    #
    # def warning(self, msg):
    #     self.my_log(msg, 'WARNING')
    #
    # def error(self, msg):
    #     self.my_log(msg, 'ERROR')
    #
    # def critical(self, msg):
    #     self.my_log(msg, 'CRITICAL')

    # def __init__(self, name="logs"):
    #     """
    #     初始化生成器
    #     :param name: 生成器的名称
    #     """
    #     self.log_name = name
    #     # 生成记录器，名字为"tong",其实是用logger调用，这里估计是给配置文件用的
    #     self.logger = logging.getLogger(name)
    #     # 默认等级都是最低级别的DEBUG，因为记录器的默认等级优先级高于处理器的
    #     self.logger.setLevel(logging.DEBUG)
    #
    # def set_stream(self):
    #     """
    #     初始化流处理器
    #     """
    #     # 生成处理器流处理器
    #     console_handle = logging.StreamHandler()
    #     # 默认等级为DEBUG
    #     console_handle.setLevel(logging.DEBUG)
    #     # 处理器添加格式，这里都添加同一个
    #     console_handle.setFormatter(self.formatter)
    #     # 记录器添加处理器，就拥有了屏幕输出的和文件输出的日志了
    #     self.logger.addHandler(console_handle)
    #
    # def set_file(self):
    #     """
    #     初始化文件处理器
    #     """
    #     # 生成日期：创造Log_2020-12-03.log文件
    #     a = self.log_name + "_" + str(datetime.date.today()) + ".log"
    #     # b是最终的文件路径，在根路径的logs文件夹下
    #     b = os.path.join(self.BASE_PATH, "logs", a)
    #     # 通过配置文件，获取log是w模式还是a的追加模式
    #     file_mode = cf.get_key("logs", "file_mode")
    #     # 文件处理器，文件名为demo.logs
    #     file_handle = logging.FileHandler(filename=b, mode=file_mode)
    #     # 默认等级为INFO
    #     file_handle.setLevel(logging.INFO)
    #     # 处理器添加格式，这里都添加同一个
    #     file_handle.setFormatter(self.formatter)
    #     # 记录器添加处理器，就拥有了屏幕输出的和文件输出的日志了
    #     self.logger.addHandler(file_handle)
    #
    # def get_log(self):
    #     """
    #     运行创建文件处理器和流处理器的代码，最终返回一个logger对家
    #     :return: logger对象
    #     """
    #     # 创建了文件处理器
    #     self.set_file()
    #     # 创建流处理器
    #     self.set_stream()
    #     # 返回记录器，拥有文件和流的处理器和格式，可以输出日志了
    #     return self.logger


"""
python的单例模式
其实python的模块就是天然的单例模式,因为模块在第一次导入的时候,会生成.pyc文件
当第二次导入的时候,就会直接加载.pyc文件,而不是再次执行模块代码.如果我们把相关的函数和数据定义在一个模块中
就可以获得一个单例对象了
"""
log = MyLog().get_log()
# log1 = MyLog()

# if __name__ == '__main__':
    # log.debug('stone1 今天有点萌萌滴')
    # log.info('stone2 今天有点萌萌滴')
    # log1.close_log()
    # MyLog().my_log('stone1 今天有点萌萌滴', 'ERROR')
    # MyLog().my_log('stone2 今天有点萌萌滴', 'ERROR')

# import logging
# import os
# from api_test_demo2.common.config import cf
# import datetime
#
#
# class Log:
#     """
#     获取Log日志封装的类
#
#     formatter：格式化器
#     BASE_PATH：项目的根路径
#     """
#
#     # 生成的格式化器
#     formatter = logging.Formatter("%(asctime)s|%(levelname)-6s|%(filename)s:%(lineno)-3s|%(message)s", "%Y-%m-%d-%H:%M")
#     # 获取项目的根路径
#     BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#
#     def __init__(self, name="logs"):
#         """
#         初始化生成器
#         :param name: 生成器的名称
#         """
#         self.log_name = name
#         # 生成记录器，名字为"tong",其实是用logger调用，这里估计是给配置文件用的
#         self.logger = logging.getLogger(name)
#         # 默认等级都是最低级别的DEBUG，因为记录器的默认等级优先级高于处理器的
#         self.logger.setLevel(logging.DEBUG)
#
#     def set_stream(self):
#         """
#         初始化流处理器
#         """
#         # 生成处理器流处理器
#         console_handle = logging.StreamHandler()
#         # 默认等级为DEBUG
#         console_handle.setLevel(logging.DEBUG)
#         # 处理器添加格式，这里都添加同一个
#         console_handle.setFormatter(self.formatter)
#         # 记录器添加处理器，就拥有了屏幕输出的和文件输出的日志了
#         self.logger.addHandler(console_handle)
#
#     def set_file(self):
#         """
#         初始化文件处理器
#         """
#         # 生成日期：创造Log_2020-12-03.log文件
#         a = self.log_name + "_" + str(datetime.date.today()) + ".log"
#         # b是最终的文件路径，在根路径的logs文件夹下
#         b = os.path.join(self.BASE_PATH, "logs", a)
#         # 通过配置文件，获取log是w模式还是a的追加模式
#         file_mode = cf.get_key("logs", "file_mode")
#         # 文件处理器，文件名为demo.logs
#         file_handle = logging.FileHandler(filename=b, mode=file_mode)
#         # 默认等级为INFO
#         file_handle.setLevel(logging.INFO)
#         # 处理器添加格式，这里都添加同一个
#         file_handle.setFormatter(self.formatter)
#         # 记录器添加处理器，就拥有了屏幕输出的和文件输出的日志了
#         self.logger.addHandler(file_handle)
#
#     def get_log(self):
#         """
#         运行创建文件处理器和流处理器的代码，最终返回一个logger对家
#         :return: logger对象
#         """
#         # 创建了文件处理器
#         self.set_file()
#         # 创建流处理器
#         self.set_stream()
#         # 返回记录器，拥有文件和流的处理器和格式，可以输出日志了
#         return self.logger
#
# """
# 由于这是python的单例模式
# 其实,python的模块就是天然的单例模式,因为模块在第一次导入的时候,会生成.pyc文件,
# 当第二次导入的时候,就会直接加载.pyc文件,而不是再次执行模块代码.如果我们把相关的函数和数据定义在一个模块中,
# 就可以获得一个单例对象了.
# """
# log = Log().get_log()
#
# if __name__ == "__main__":
#     # logs=Log().get_log()
#     log.error("abc")
