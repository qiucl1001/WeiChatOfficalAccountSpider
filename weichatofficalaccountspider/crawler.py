# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import requests
from lxml import etree
from requests import Session
from .queue import RedisQueue
from urllib import parse
from .db import WeiChatMySQL
from .request import WeiChatRequest
from requests import ConnectionError, ReadTimeout
from .settings import PROXY_POOL_URL, VALID_STATUS_CODES, MAX_FAIL_NUMS


class Spider(object):
    """抓取类"""
    base_url = "https://weixin.sogou.com/weixin"
    keywords = "python"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/"
                  "signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "SUV=1550661577753145; SMYUV=1550661577754888; SUID=A6A828754D238B0A5C8797C500074491;"
                  " wuid=AAEIyaXdKAAAAAqLMXI5fwQAGwY=; IPLOC=CN3611; ssuid=732965242; ABTEST=0|1587193326|v1;"
                  " weixinIndexVisited=1; SNUID=1ACFA8C5181DBA93278D93D4190F524D; JSESSIONID=aaavGDO1NDry1dTeN99fx;"
                  " ppinf=5|1587200978|1588410578|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMDolRTUlQjAlOEZRfG"
                  "NydDoxMDoxNTg3MjAwOTc4fHJlZm5pY2s6MTA6JUU1JUIwJThGUXx1c2VyaWQ6NDQ6bzl0Mmx1S1FLN3N0bUNEMDRqSFVGTm4"
                  "0SEQzOEB3ZWl4aW4uc29odS5jb218; pprdig=g0paLcoo7jK8NqF-C8JqZvSnSx_yKu3tPPsLESawOf3aWKItcK_oWu0LKSqX"
                  "Q5LWjCA3pERz9FA9HQZghcWp0uoBc_pbgv8Qiq5hHHlvx2vVE4FrfVcJAFuEJha5Bbsk12bNjaLxFCfghtjtwcLlMppxzGiYja"
                  "VfHxdlLqIfJcM; sgid=07-45337203-AV6aw9JiamZWF488mdy4RHEA; ppmdig=15872009790000004ec169435e735442d"
                  "29d641bac0c80e1; sct=4",
        "Host": "weixin.sogou.com",
        "Referer": "https://weixin.sogou.com/weixin?query=python&_sug_type_=&sut=2028&lkt=7%2C1587201134473%2C15872011"
                   "36528&s_from=input&_sug_=y&type=2&sst0=1587201136632&page=12&ie=utf8&w=01019900&dr=1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.132 Safari/537.36",
    }
    session = Session()
    queue = RedisQueue()
    mysql = WeiChatMySQL()

    def start(self):
        """初始化"""
        # 更新全局配置
        self.session.headers.update(self.headers)

        # 拼接第一个请求url https://weixin.sogou.com/weixin?type=1&query=NBA
        start_url = self.base_url + "?" + parse.urlencode({"type": 2, "query": self.keywords})

        # 构建第一个请求对象并入请求队列
        wei_chat_request = WeiChatRequest(url=start_url, callback=self.parse_list_page, need_proxy=True)
        self.queue.add(wei_chat_request)

    def parse_list_page(self, response):
        """
        解析列表页
        :param response: 响应内容
        :return: 新的响应内容
        """
        html = etree.HTML(response.text)
        detail_urls = html.xpath('//ul[@class="news-list2"]/li//p[@class="tit"]/a/@href')
        for detail_url in detail_urls:
            full_detail_url = "https://weixin.sogou.com" + detail_url
            wei_chat_request = WeiChatRequest(url=full_detail_url, callback=self.parse_detail_page)
            yield wei_chat_request

        # 下一页链接
        next_element = html.xpath('//a[@id="sogou_next"]/@href')
        if next_element:
            full_next_url = self.base_url + next_element[0]
            wei_chat_request = WeiChatRequest(url=full_next_url, callback=self.parse_list_page, need_proxy=True)
            yield wei_chat_request

    def parse_detail_page(self, response):
        """
        解析详情页数据
        :param response: 详情页响应源代码
        :return: 响应数据
        """
        html = etree.HTML(response.text)
        # 标题
        title = "".join(html.xpath('//h2[@id="activity-name"]/text()')).strip()
        # 类别
        category = html.xpath('//a[@id="js_name"]/text()')[0]
        # 来源
        source_from = html.xpath('//div[@id="js_content"]/section[2]/span/text()')[0]
        # 内容
        content = "\n".join(html.xpath('//div[@id="js_content"]//p/span/text()'))

        data = {
            "title": title,
            "category": category,
            "source_from": source_from,
            "content": content
        }
        yield data

    @staticmethod
    def get_proxy():
        """
        从搭建的代理池中随机获取一个代理
        :return:
        """
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError as e:
            print(e.args)
            return None

    def download_page_source(self, wei_chat_request):
        """
        下载网页源代码
        :param wei_chat_request: 请求对象
        :return:
        """
        try:
            if wei_chat_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        "http": "http://" + proxy,
                        "https": "https://" + proxy
                    }
                    return self.session.send(
                        wei_chat_request.prepare(),
                        timeout=wei_chat_request.timeout,
                        proxies=proxies,
                        allow_redirects=False
                    )
            return self.session.send(wei_chat_request.prepare(), timeout=wei_chat_request.timeout, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def error(self, wei_chat_request):
        """
        错误处理
        :param wei_chat_request: 请求对象
        :return:
        """
        print("Request Failed {}times, Requests of url: {}".format(wei_chat_request.fail_time, wei_chat_request.url))
        wei_chat_request.fail_time = wei_chat_request.fail_time + 1
        if wei_chat_request.fail_time < MAX_FAIL_NUMS:
            self.queue.add(wei_chat_request)

    def scheduler(self):
        """
        调度请求
        :return:
        """
        if not self.queue.empty():
            wei_chat_request = self.queue.pop()
            # 发送请求给下载器下载
            response = self.download_page_source(wei_chat_request)
            if response and response.status_code in VALID_STATUS_CODES:
                callback = wei_chat_request.callback
                results = list(callback(response))
                if results:
                    if isinstance(results, WeiChatRequest):
                        self.queue.add(results)
                    if isinstance(results, dict):
                        self.mysql.insert(results)
                else:
                    self.error(wei_chat_request)
            else:
                self.error(wei_chat_request)

    def run(self):
        """程序入口"""
        self.start()
        self.scheduler()


if __name__ == '__main__':
    s = Spider()
    s.run()
