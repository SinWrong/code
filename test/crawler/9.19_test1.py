#项目日期9.19成功完善
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
BASE_URL = 'https://jandan.net/pic'  # 注意改成 https
PIC_SAVE_PATH = os.path.join(os.getcwd(), 'JianDan')
if not os.path.exists(PIC_SAVE_PATH):
    os.makedirs(PIC_SAVE_PATH)

# 图片下载 Headers (移除写死的 Host)
PIC_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://jandan.net/'
}


class JianDanCrawler:
    def __init__(self):
        # Redis 连接
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='123456', db=1, decode_responses=True)
        self.dan_redis = redis.StrictRedis(connection_pool=self.pool)
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
        """获取总页码：根据新版的 page-jump-input 的 max 属性提取"""
        soup = BeautifulSoup(html, 'lxml')

        # 方案1：找跳页输入框的 max 属性
        jump_input = soup.find('input', class_='page-jump-input')
        if jump_input and jump_input.get('max'):
            try:
                return int(jump_input['max'])
            except ValueError:
                pass

        # 方案2：找分页按钮中的最大值
        page_buttons = soup.find_all('button')
        max_page = 1
        for btn in page_buttons:
            if btn.text.strip().isdigit():
                max_page = max(max_page, int(btn.text.strip()))

        if max_page > 1:
            return max_page

        logging.warning("未找到分页元素，默认返回第一页。")
        return 1

    def get_meizi_url(self, html):
        """解析新版页面中的图片链接并存入 Redis"""
        soup = BeautifulSoup(html, 'html.parser')

        # 新版图片在 div.comment-row 中，原图链接在 a.img-link 的 href 中
        comment_rows = soup.find_all('div', class_='comment-row')
        if not comment_rows:
            logging.warning("未找到图片列表容器 (comment-row)")
            return

        new_count = 0
        for row in comment_rows:
            # 找原图链接
            a_link = row.find('a', class_='img-link')
            if a_link and a_link.get('href'):
                img_url = a_link.get('href')
                # 过滤非图片链接
                if not (img_url.endswith('.jpg') or img_url.endswith('.png') or img_url.endswith(
                        '.gif') or img_url.endswith('.jpeg')):
                    continue

                # 去重并存入 Redis
                if not self.dan_redis.sismember(self.redis_downloaded_set_key, img_url):
                    self.dan_redis.rpush(self.redis_url_list_key, img_url)
                    self.dan_redis.sadd(self.redis_downloaded_set_key, img_url)
                    new_count += 1

        logging.info(f"本页抓取到 {new_count} 张新图片链接")

    def browser_get(self):
        """使用 Selenium 模拟浏览器获取页面"""
        try:
            logging.info(f"正在访问首页: {BASE_URL}")
            self.browser.get(BASE_URL)

            # 等待页面加载（等待页码输入框出现）
            try:
                WebDriverWait(self.browser, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "page-jump-input"))
                )
            except Exception:
                logging.warning("等待分页元素超时，可能页面结构已改变或触发了反爬。")

            html_text = self.browser.page_source
            page_count = self.get_page_count(html_text)
            logging.info(f"获取到总页数为: {page_count}")

            # 为测试起见，限制只爬取前 3 页（避免耗时过久）
            # 如果要全站爬取，请去掉 `min(page_count, 3)`
            max_pages_to_crawl = min(page_count, 3)
            logging.info(f"本次将爬取最新的 {max_pages_to_crawl} 页")

            for page in range(max_pages_to_crawl, 0, -1):
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
            self.browser.quit()
            logging.info("浏览器已关闭。")

    def download_pic(self, url):
        """下载图片"""
        # 新版页面已经是完整的 https 链接，无需再做拼接处理
        pic_name = url.split("/")[-1].split('?')[0]
        save_path = os.path.join(PIC_SAVE_PATH, pic_name)

        if os.path.exists(save_path):
            return

        logging.info(f"开始下载: {url}")
        try:
            resp = r.get(url, headers=PIC_HEADERS, timeout=15)
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
            else:
                logging.warning(f"下载失败，状态码 {resp.status_code}: {url}")
        except Exception as reason:
            logging.error(f"下载图片出错 {url}: {reason}")

    def run(self):
        """运行主流程"""
        self.browser_get()

        logging.info("开始从 Redis 读取 URL 并下载图片...")
        urls = self.dan_redis.lrange(self.redis_url_list_key, 0, -1)

        if not urls:
            logging.warning("Redis 中没有找到待下载的图片链接，请检查解析逻辑是否正常。")
            return

        for url in urls:
            self.download_pic(url)

        logging.info("图片下载完毕！")


if __name__ == '__main__':
    crawler = JianDanCrawler()
    crawler.run()