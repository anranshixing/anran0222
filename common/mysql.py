import pandas as pd
import pymysql

from common.config import cf
from common.get_log import log


class Mysql:
    """
    操作mysql的类
    """

    def __init__(self):
        """
        初始化mysql的db对象，连接数据库
        """
        # 通过配置文件获取数据库的host，port，username，password，charset，database
        host = cf.get_key("mysql", "host")
        # 从配置文件获取的值是str，需要转化成int
        port = int(cf.get_key("mysql", "port"))
        user = cf.get_key("mysql", "user")
        password = cf.get_key("mysql", "password")
        database = cf.get_key("mysql", "database")
        # 字符集暂不传
        # charset = self.cf.get_key("mysql", "charset")
        # 当无法连接数据库，走异常处理
        try:
            self._db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
            # 定义游标
            self._cur = self._db.cursor()
            # 让查询结果以字典的形式展示 {'id': 8, 'name': 'joker', 'age': 24}
            # self._cur = self._db.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            log.error(f"无法登陆数据库，错误原因：{e}")

    def select(self, query):
        """
        运行mysql的select语句
        :param query: select语句
        :return: select_data：返回全部的select语句的数据
        """
        log.info(f"select语句为：{query}")
        try:
            # 定义游标后通过execute执行sql语句
            self._cur.execute(query)
            # fetchall读取游标中的所有select数据:(()) fetchone:()
            select_data = self._cur.fetchall()
            log.info("数据查询成功")
            # 返回select数据
            return select_data
        except pymysql.err.InterfaceError as e:
            log.error(f'数据库连接错误，错误原因是：{e}')  # 数据库关闭后在定义游标会报这个错
        except Exception as e:
            log.error(f"select语句错误，错误原因是：{e}")

    def insert(self, query):
        """
        运行mysql的insert语句
        :param query: insert语句
        """
        log.info(f"insert语句为：{query}")
        try:
            # 定义游标，并通过execute执行insert语句
            self._cur.execute(query)
            # insert执行成功后commit提交数据
            self._cur.execute("commit")
            log.info(f"数据插入成功")
        except Exception as e:
            log.error(f"insert 语句错误，原因是{e}")
            # insert失败后rollback回滚数据
            self._cur.execute("rollback")

    def delete(self, query):
        """
        运行mysql的delete语句
        :param query: delete语句
        """
        log.info(f"delete语句为：{query}")
        try:
            # 定义游标，并通过execute执行delete语句
            self._cur.execute(query)
            # delete执行成功后commit提交数据
            self._cur.execute("commit")
            log.info("数据删除成功")
        except Exception as e:
            log.error(f"delete语句失败，原因：{e}")
            # delete失败后rollback回滚数据
            self._cur.execute("rollback")

    def close_db(self):
        try:
            self._db.close()
        except pymysql.err.Error:
            log.warning('数据库已经关闭,请不要重复关闭！')

    def test(self):
        """
        使用pandas来读取数据库
        :return: 测试用
        """
        data = pd.read_sql(sql='select * from ys_user where uid = 50', con=self._db)
        print(data)


# 定义对象为单例模式，其他模块可方便使用
sql = Mysql()

if __name__ == "__main__":
    print(sql.select('select * from ys_user where uid < 50'))
    sql.close_db()
    # sql.select('select * from ys_user where uid > 1120')
    # a.delete("delete from schedule_id where schedule_id='abc'")
    # a.insert(f"insert into schedule_id(userid,schedule_id) values('{organizer}','{cal_id}')")
    # a.insert(f"insert into cal_id(userid,cal_id) values('calendar','hehehda')")
    # print(a.select("select * from schedule_id"))
    # b=a.select("select cal_id from cal_id")
    # b=[i[0] for i in b ]
    # print(b)
