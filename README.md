# WeiChatOfficalAccountSpider
## 微信公众号数据抓取: url地址链接[https://weixin.sogou.com/weixin]

备注：
* 使用redis数据库的list列表数据结构构建一个请求队列，用来进行请求的存取
* 实现请求的异常处理，将失败的请求地址才重新放回请求队列，等待下次被调度
* 实现翻页并将并将列表页中详情url地址入请求队列，等待被调度
* 实现详情页数据的抓取
* 实现将详情页提取的相关数据存入mysql数据库
* 修改搭建的代理池检测连接为搜狗微信站点的连接

# 安装
## 开发环境安装
* Python Versions: 3.0+
* MySQL Versions: 5.7.21+

## 三方库安装
```
cd weichatofficalaccountspider
pip install -r requirements.txt
```
# 创建数据库和数据表
### mysql数据库创建
create database wei_chat default charset="utf8";

### 数据表创建
create table wei_tbl(
    id unsigned int auto_increment primary key not null,
    title varchar(255) not null,
    category varchar(255) not null,
    source_from varchar(64) not null,
    content text not null
    ) default charset=utf8;
   # alter table `wei_tbl` add primary key(`id`);
   
   
# 启动程序
1. 先下载ip代理池：'clone git git@github.com:qiucl1001/IP_PROXY_POOL.git'
2. 修改搭建的代理池检测连接为搜狗微信站点的连接
3. cd ip_pool
4.  python run.py
5. 让程序运行一段时间
```
cd WeiChatOfficalAccountSpider
python start.py
```