#6.5 实战:反爬应用
import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

TARGET_URL = "https://pixiviz.xyz/search/%E5%88%9D%E9%9F%B3%E6%9C%AA%E6%9D%A5"
DOWNLOAD_FOLDER = "pixiviz_images"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def extract_image_urls_from_page(html):
    """提取所有图片直链，重点抓取 data-src 属性（适用于 div 等非 img 标签）"""
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()

    # 1. 查找所有带有 data-src 的元素（div, img 等）
    for elem in soup.find_all(attrs={'data-src': True}):
        src = elem.get('data-src')
        if src and src.startswith('http'):
            urls.add(src)

    # 2. 常规 img 标签的 src（备用）
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src.startswith('http'):
            urls.add(src)
        # 有些 img 也可能有 data-src
        data_src = img.get('data-src')
        if data_src and data_src.startswith('http'):
            urls.add(data_src)

    # 3. 正则补充捕获（以防漏网）
    pattern = r'https?://[^\s"\']+\.(jpg|jpeg|png|gif|webp|bmp)(\?[^\s"\']*)?'
    for match in re.finditer(pattern, html, re.I):
        full_url = match.group(0)
        if full_url.startswith('http'):
            urls.add(full_url)

    return list(urls)


def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 可注释掉以观察
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(TARGET_URL)

    # 等待至少一个带 data-src 的元素出现
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-src]"))
        )
        print("页面初始内容加载成功")
    except:
        print("等待超时，可能页面结构有变，继续尝试...")

    last_count = 0
    no_new_count = 0
    max_no_new = 5

    while no_new_count < max_no_new:
        # 滚动一屏高度
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1.5)  # 等待懒加载

        # 获取当前所有 data-src 元素的数量（更精确）
        current_elements = driver.find_elements(By.CSS_SELECTOR, "[data-src]")
        current_count = len(current_elements)
        print(f"当前找到 {current_count} 个带 data-src 的元素")

        if current_count > last_count:
            last_count = current_count
            no_new_count = 0
            print("检测到新图片，继续滚动...")
        else:
            no_new_count += 1
            print(f"未发现新图片，尝试第 {no_new_count}/{max_no_new} 次")

        # 尝试点击“加载更多”按钮（如果存在）
        try:
            load_btn = driver.find_element(By.XPATH, "//button[contains(.,'加载更多') or contains(.,'Load more')]")
            if load_btn.is_displayed():
                load_btn.click()
                time.sleep(1.5)
                no_new_count = 0  # 点击后重置计数
                print("点击了'加载更多'按钮")
        except:
            pass

        # 检测结束标记
        if "没有更多图片" in driver.page_source or "no more" in driver.page_source.lower():
            print("检测到'没有更多图片'，停止加载")
            break

    # 最终提取所有图片 URL
    final_urls = extract_image_urls_from_page(driver.page_source)
    driver.quit()

    print(f"共提取到 {len(final_urls)} 张不重复的图片")

    # 下载
    for idx, url in enumerate(final_urls):
        try:
            filename = os.path.basename(url.split('?')[0])
            if not filename or '.' not in filename:
                filename = f"image_{idx}.jpg"
            save_path = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.exists(save_path):
                print(f"已存在: {filename}")
                continue
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            print(f"下载成功: {filename}")
            time.sleep(0.5)
        except Exception as e:
            print(f"下载失败 {url}: {e}")

    print("全部完成！")


if __name__ == "__main__":
    main()