# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import pymysql
from .settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_TABLE


class WeiChatMySQL(object):
    """定义一个用来将微信公众号相关数据存储到mysql数据库的类"""

    def __init__(self,
                 host=MYSQL_HOST,
                 port=MYSQL_PORT,
                 user=MYSQL_USER,
                 password=MYSQL_PASSWORD,
                 database=MYSQL_DATABASE,
                 table=MYSQL_TABLE
                 ):
        """
        初始化
        :param host: 数据库宿主机所在ip地址或域名
        :param port: 数据库端口号
        :param user: 连接数据库的用户名
        :param password: 连接数据库登入密码
        :param database: 存储数据的数据库名称
        :param table: 数据表
        """
        self.table = table
        self.__sql = None
        self.keys = None
        self.values = None
        try:
            self.db = pymysql.connect(host=host,
                                      port=port,
                                      user=user,
                                      password=password,
                                      database=database,
                                      charset="utf8"
                                      )
            self.cursor = self.db.cursor()
        except Exception as e:
            print(e.args)

    def insert(self, data):
        """
        将数据写入mysql数据库
        :param data:
        :return:
        """
        self.keys = ", ".join(data.keys())
        self.values = ", ".join(["%s"]*len(data))
        try:
            self.cursor.execute(self.sql, tuple(data.values()))
            self.db.commit()
        except Exception as e:
            print(e.args)
            self.db.rollback()

    @property
    def sql(self):
        if not self.__sql:
            self.__sql = """
                insert into %s(%s) values(%s);
            """ % (self.table, self.keys, self.values)
        return self.__sql

