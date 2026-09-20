#项目日期9.4煎蛋网爬虫项目完善
import os
import time
import logging
import redis
import requests as r
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 基础配置
BASE_URL = 'http://jandan.net/pic'
PIC_SAVE_PATH = os.path.join(os.getcwd(), 'JianDan')
debugpage_html=os.path.join(os.getcwd(),'debug_page.html')
if not os.path.exists(PIC_SAVE_PATH):
    os.makedirs(PIC_SAVE_PATH)


# 图片下载 Headers (补充 Referer 防盗链)
PIC_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'http://jandan.net/'
}


class JianDanCrawler:
    def __init__(self):
        # Redis 连接
        self.pool = redis.ConnectionPool(host='localhost', port=6379, password='123456', db=1, decode_responses=True)
        self.dan_redis = redis.StrictRedis(connection_pool=self.pool)
        # Redis 存储键
        self.redis_url_list_key = 'jandan_pic_urls'
        self.redis_downloaded_set_key = 'jandan_downloaded_set'

        # Selenium 配置
        self.browser = self._init_browser()

    def _init_browser(self):
        """初始化浏览器配置"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 调试时建议注释掉，正式运行开启无头模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')

        browser = webdriver.Chrome(options=chrome_options)
        return browser

    def get_page_count(self, html):
        """获取总页码，增加容错机制"""
        soup = BeautifulSoup(html, 'lxml')
        # 尝试旧版查找方式
        page_count_span = soup.find('span', attrs={'class': 'current-comment-page'})

        if page_count_span:
            try:
                return int(page_count_span.get_text().strip()[1:-1]) - 1
            except ValueError:
                pass

        # 兜底：如果找不到，尝试通过找最后一个分页链接来推算，或者直接返回固定页数（防崩溃）
        logging.warning("未找到分页元素，可能是网页改版或未加载完成。默认返回第一页。")
        return 1  # 返回 1，只爬第一页作为降级方案

    def get_meizi_url(self, html):
        """解析页面中的图片链接并存入 Redis"""
        soup = BeautifulSoup(html, 'html.parser')
        ol = soup.find('ol', attrs={'class': 'commentlist'})
        if not ol:
            logging.warning("未找到图片列表容器 (commentlist)")
            return

        hrefs = ol.findAll('a', attrs={'class': 'view_img_link'})
        for a in hrefs:
            img_url = a.get('href')
            if img_url:
                # 使用 Redis 的 Set 进行去重，List 进行存储
                if not self.dan_redis.sismember(self.redis_downloaded_set_key, img_url):
                    self.dan_redis.rpush(self.redis_url_list_key, img_url)
                    self.dan_redis.sadd(self.redis_downloaded_set_key, img_url)

    def browser_get(self):
        """使用 Selenium 模拟浏览器获取页面"""
        try:
            logging.info(f"正在访问首页: {BASE_URL}")
            self.browser.get(BASE_URL)

            # 显式等待：等待分页元素加载出来（最多等 10 秒）
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "current-comment-page"))
                )
            except Exception:
                logging.warning("等待分页元素超时，可能页面结构已改变或触发了反爬。")

            # 在 browser_get 方法中，browser.get(BASE_URL) 和 WebDriverWait 之后添加：
            with open(debugpage_html, 'w', encoding='utf-8') as f:
                f.write(self.browser.page_source)
            logging.info("已将页面源码保存到 debug_page.html，请用浏览器打开查看")
            html_text = self.browser.page_source
            page_count = self.get_page_count(html_text)
            logging.info(f"获取到总页数为: {page_count}")

            # 循环拼接URL访问
            for page in range(page_count, 0, -1):
                page_url = f"{BASE_URL}/page-{page}"
                logging.info(f"正在解析: {page_url}")
                self.browser.get(page_url)

                # 随机延时，防止触发反爬
                time.sleep(2 + (page % 3))

                html = self.browser.page_source
                self.get_meizi_url(html)

        except Exception as e:
            logging.error(f"浏览器请求发生异常: {e}")
        finally:
            # 确保浏览器在任何情况下都能关闭，避免进程残留
            self.browser.quit()
            logging.info("浏览器已关闭。")

    def download_pic(self, url):
        """下载图片"""
        correct_url = url
        if url.startswith('//'):
            correct_url = 'http:' + url
        elif not url.startswith('http'):
            correct_url = 'http://' + correct_url

        pic_name = correct_url.split("/")[-1].split('?')[0]  # 去除URL参数防止文件名非法
        save_path = os.path.join(PIC_SAVE_PATH, pic_name)

        # 检查是否已经下载过
        if os.path.exists(save_path):
            return

        logging.info(f"开始下载: {correct_url}")
        try:
            resp = r.get(correct_url, headers=PIC_HEADERS, timeout=10)
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
            else:
                logging.warning(f"下载失败，状态码 {resp.status_code}: {correct_url}")
        except Exception as reason:
            logging.error(f"下载图片出错 {correct_url}: {reason}")

    def run(self):
        """运行主流程"""
        self.browser_get()

        # 从 Redis List 中获取所有 URL 进行下载
        logging.info("开始从 Redis 读取 URL 并下载图片...")
        # 注意：如果数据量极大，建议分批次 lrange，避免内存溢出
        urls = self.dan_redis.lrange(self.redis_url_list_key, 0, -1)

        for url in urls:
            self.download_pic(url)

        logging.info("图片下载完毕！")


if __name__ == '__main__':
    crawler = JianDanCrawler()
    crawler.run()