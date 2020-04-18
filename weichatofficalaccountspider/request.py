# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from .settings import TIMEOUT
from requests import Request


class WeiChatRequest(Request):
    """
    重写 requests 模块的Request类'def __init__()'方法

    requests模块中Request类初始化源码如下：
         def __init__(self,
                method=None, url=None, headers=None, files=None, data=None,
                params=None, auth=None, cookies=None, hooks=None, json=None):

            # Default empty dicts for dict params.
            data = [] if data is None else data
            files = [] if files is None else files
            headers = {} if headers is None else headers
            params = {} if params is None else params
            hooks = {} if hooks is None else hooks

            self.hooks = default_hooks()
            for (k, v) in list(hooks.items()):
                self.register_hook(event=k, hook=v)

            self.method = method
            self.url = url
            self.headers = headers
            self.files = files
            self.data = data
            self.json = json
            self.params = params
            self.auth = auth
            self.cookies = cookies
    """
    def __init__(self,
                 url,
                 method="GET",
                 headers=None,
                 need_proxy=False,
                 fail_time=0,
                 timeout=TIMEOUT,
                 callback=None
                 ):
        """初始化请求对象"""
        super(WeiChatRequest, self).__init__(url, method, headers)
        self.need_proxy = need_proxy  # 请求是否需要设置代理
        self.fail_time = fail_time  # 每个请求失败次数
        self.timeout = timeout  # 每个请求超时时间
        self.callback = callback  # 回调函数
