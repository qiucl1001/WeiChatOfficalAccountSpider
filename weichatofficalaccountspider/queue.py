# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import redis
from .settings import REDIS_URI, REDIS_KEY
from pickle import loads, dumps
from .request import WeiChatRequest


class RedisQueue(object):
    """使用redis数据库实现一个请求队列"""

    def __init__(self, redis_uri=REDIS_URI, redis_key=REDIS_KEY):
        """初始化"""
        self.redis_uri = redis_uri
        self.redis_key = redis_key
        self.pool = redis.ConnectionPool.from_url(self.redis_uri)
        self.db = redis.StrictRedis(connection_pool=self.pool)

    def add(self, request):
        """
        序列化之后的请求对象入请求队列
        :param request: 待入队列的请求对象
        :return: 返回添加后的结果
        """
        if isinstance(request, WeiChatRequest):
            return self.db.rpush(self.redis_key, dumps(request))
        else:
            return False

    def pop(self):
        """
        反序列化之后的请求对象出队列
        :return: Request请求对象 or None
        """
        if self.db.llen(self.redis_key):
            return loads(self.db.lpop(self.redis_key))
        else:
            return False

    def empty(self):
        """
        判断请求队列是否为空
        :return: True or False
        """
        return self.db.llen(self.redis_key) == 0
