#7.1 Scrapy
"""
Scrapy，谐音读作西瓜皮，是用Python语言开发的一个快速、高层次的屏幕/Web抓取
框架，用于抓取Web站点并从页面中提取结构化数据。
Scrapy 使用 Twisted 异步网络请求框架来处理网络通信，不需要额外实现异步框架，
而且包含各种中间件接口，能灵活地实现各种需求。Scrapy的用途广泛，常用于数据挖掘、
监测和自动化测试。
Scrapy通过命令行运行
"""
#7.2 实战:Scrapy应用爬取壁纸
import scrapy
import time
class BingWallpaperSpider(scrapy.Spider):
    name = 'BingWallpaper'
    allowed_domains = ['cn.bing.com']
    start_urls = [
    'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=1&n=7&nc={ts}&pid=hp'.format(ts=int(time.time()))]
    def parse(self, response):
        self.logger.debug(response.body.decode('utf8'))