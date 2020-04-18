# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

# 网络请求超时时间 单位：秒
TIMEOUT = 10

# redis数据库连接配置 "redis://[:password]@ip:port/db"
REDIS_URI = "redis://localhost@6379/1"

# 存储请求队列的redis_key 这里使用redis的list列表做请求队列
REDIS_KEY = "wei_chat"

# mysql数据库相关连接
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "qcl123"
MYSQL_DATABASE = "wei_chat"
MYSQL_TABLE = "wei_tbl"

# 代理池url地址
PROXY_POOL_URL = "http://127.0.0.1:5000/random"

# 有效的响应状态码列表集合
VALID_STATUS_CODES = [200]

# 每个请求允许的最大失败重新请求次数阈值
MAX_FAIL_NUMS = 5


