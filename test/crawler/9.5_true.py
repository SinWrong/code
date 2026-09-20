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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://pixiviz.xyz/',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

def clean_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith('http'):
        return None
    if 'pixiv-image.pwp.link' not in url:
        return None
    return url

def extract_image_urls_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for elem in soup.find_all(attrs={'data-src': True}):
        src = elem.get('data-src')
        clean = clean_url(src)
        if clean:
            urls.add(clean)
    for elem in soup.find_all(style=True):
        match = re.search(r'url\(["\']?(https?://[^"\'\)]+)["\']?\)', elem['style'])
        if match:
            clean = clean_url(match.group(1))
            if clean:
                urls.add(clean)
    pattern = r'https?://[^\s"\']+\.(jpg|jpeg|png|gif|webp|bmp)(\?[^\s"\']*)?'
    for match in re.finditer(pattern, html, re.I):
        clean = clean_url(match.group(0))
        if clean:
            urls.add(clean)
    return list(urls)

def download_image(img_url, index, retries=3):
    filename = os.path.basename(img_url.split('?')[0])
    if not filename or '.' not in filename:
        filename = f"image_{index}.jpg"
    save_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(save_path):
        print(f"已存在: {filename}")
        return True
    for attempt in range(retries):
        try:
            resp = requests.get(img_url, headers=HEADERS, timeout=15)
            if resp.status_code == 403:
                # 尝试不带 Referer 重试一次
                if attempt == 0:
                    headers_no_ref = HEADERS.copy()
                    headers_no_ref.pop('Referer', None)
                    resp = requests.get(img_url, headers=headers_no_ref, timeout=15)
                else:
                    time.sleep(2)
                    continue
            resp.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            print(f"下载成功: {filename}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"下载失败 (尝试 {attempt+1}/{retries}) {img_url}: {e}")
            time.sleep(2 ** attempt)
    return False

def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    chrome_options = Options()
    # 不开启无头模式便于观察（可以注释掉下一行）
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
    chrome_options.add_argument("--window-size=1920,1080")
    # 反检测参数
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    print("正在加载页面...")
    driver.get(TARGET_URL)

    # 关键：给页面足够的初始渲染时间（诊断证明至少需要5秒）
    print("等待页面初始渲染...")
    time.sleep(8)  # 固定等待，确保 data-src 元素出现

    # 验证一下初始元素数量
    initial_elements = driver.find_elements(By.CSS_SELECTOR, "[data-src]")
    print(f"初始加载找到 {len(initial_elements)} 个带 data-src 的元素")

    last_count = len(initial_elements)
    no_new_count = 0
    max_no_new = 5

    while no_new_count < max_no_new:
        # 滚动一屏高度
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)  # 等待懒加载触发

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

        # 检测“加载更多”按钮（可能不存在）
        try:
            load_btn = driver.find_element(By.XPATH, "//button[contains(.,'加载更多') or contains(.,'Load more')]")
            if load_btn.is_displayed():
                load_btn.click()
                time.sleep(1.5)
                no_new_count = 0
                print("点击了'加载更多'按钮")
        except:
            pass

        # 检测结束标志
        if "没有更多图片" in driver.page_source or "no more" in driver.page_source.lower():
            print("检测到'没有更多图片'，停止加载")
            break

    # 最终提取所有图片URL
    final_urls = extract_image_urls_from_page(driver.page_source)
    driver.quit()

    print(f"共提取到 {len(final_urls)} 张不重复的图片")

    # 下载
    for idx, url in enumerate(final_urls):
        download_image(url, idx)
        time.sleep(0.5)

    print("全部完成！")

if __name__ == "__main__":
    main()