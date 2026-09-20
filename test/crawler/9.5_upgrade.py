import os
import re
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# ================== 配置区 ==================
BASE_URL = "https://pixiviz.xyz/search/{}"
DOWNLOAD_ROOT = "pixiviz_images"          # 根目录
METADATA_FILE = "image_metadata.csv"      # 元数据CSV路径（在根目录下）

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://pixiviz.xyz/',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

# ================== 核心函数 ==================

def clean_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith('http'):
        return None
    if 'pixiv-image.pwp.link' not in url:
        return None
    return url

def convert_to_original(url):
    if '/c/540x540_70/' in url:
        return url.replace('/c/540x540_70/', '/img-original/')
    return url

def extract_image_urls_from_page(html, download_original=False):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for elem in soup.find_all(attrs={'data-src': True}):
        src = elem.get('data-src')
        clean = clean_url(src)
        if clean:
            if download_original:
                clean = convert_to_original(clean)
            urls.add(clean)
    for elem in soup.find_all(style=True):
        match = re.search(r'url\(["\']?(https?://[^"\'\)]+)["\']?\)', elem['style'])
        if match:
            clean = clean_url(match.group(1))
            if clean:
                if download_original:
                    clean = convert_to_original(clean)
                urls.add(clean)
    pattern = r'https?://[^\s"\']+\.(jpg|jpeg|png|gif|webp|bmp)(\?[^\s"\']*)?'
    for match in re.finditer(pattern, html, re.I):
        clean = clean_url(match.group(0))
        if clean:
            if download_original:
                clean = convert_to_original(clean)
            urls.add(clean)
    return list(urls)

def download_image(img_url, index, save_folder, retries=3):
    """下载图片到指定文件夹"""
    filename = os.path.basename(img_url.split('?')[0])
    if not filename or '.' not in filename:
        filename = f"image_{index}.jpg"
    save_path = os.path.join(save_folder, filename)
    if os.path.exists(save_path):
        print(f"已存在: {filename}")
        return save_path
    for attempt in range(retries):
        try:
            resp = requests.get(img_url, headers=HEADERS, timeout=15)
            if resp.status_code == 403 and attempt == 0:
                # 尝试不带Referer
                headers_no_ref = HEADERS.copy()
                headers_no_ref.pop('Referer', None)
                resp = requests.get(img_url, headers=headers_no_ref, timeout=15)
            resp.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            print(f"下载成功: {filename}")
            return save_path
        except requests.exceptions.RequestException as e:
            print(f"下载失败 (尝试 {attempt+1}/{retries}) {img_url}: {e}")
            time.sleep(2 ** attempt)
    return None

def save_metadata(metadata_list, csv_file=METADATA_FILE):
    if not metadata_list:
        return
    keys = metadata_list[0].keys()
    file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
    with open(csv_file, 'a', newline='', encoding='utf-8-sig') as f:  # 改为 utf-8-sig
        writer = csv.DictWriter(f, fieldnames=keys)
        if not file_exists:
            writer.writeheader()
        writer.writerows(metadata_list)

def crawl_keyword(keyword, download_original=False, max_scrolls=15, scroll_distance=600):
    print(f"\n========== 开始关键词: {keyword} ==========")
    target_url = BASE_URL.format(keyword)
    keyword_folder = os.path.join(DOWNLOAD_ROOT, keyword)
    os.makedirs(keyword_folder, exist_ok=True)

    # 配置Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")   # 如需无头取消注释
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    print("正在加载页面...")
    driver.get(target_url)
    time.sleep(8)  # 等待初始渲染

    # 初始元素
    initial_elements = driver.find_elements(By.CSS_SELECTOR, "[data-src]")
    print(f"初始加载找到 {len(initial_elements)} 个图片元素")

    # ========== 滚动循环（修正版） ==========
    last_count = len(initial_elements)
    scroll_count = 0
    no_new_count = 0
    MAX_NO_NEW = 6  # 连续无新图次数阈值

    while scroll_count < max_scrolls:
        # 滚动指定距离
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(3.5)  # 适当增加等待，确保加载
        scroll_count += 1

        current_elements = driver.find_elements(By.CSS_SELECTOR, "[data-src]")
        current_count = len(current_elements)
        print(f"滚动 {scroll_count}/{max_scrolls}，当前图片数：{current_count}")

        if current_count > last_count:
            last_count = current_count
            no_new_count = 0
            print("发现新图片")
        else:
            no_new_count += 1
            print(f"未发现新图片（连续 {no_new_count} 次）")
            # 连续无新图达到阈值时，再检查是否真正没有更多
            if no_new_count >= MAX_NO_NEW:
                # 此时再检测“没有更多图片”文本（此时才可靠）
                if "没有更多图片" in driver.page_source or "no more" in driver.page_source.lower():
                    print("检测到'没有更多图片'，停止滚动")
                    break
                else:
                    print("虽然无新图，但未出现结束标记，继续尝试...")
                    # 如果还未达到最大滚动次数，可以继续（但为避免死循环，可再尝试几次）
                    # 也可以设置一个额外尝试次数，这里我们让循环继续，但会因为 no_new_count 过大而退出循环
                    # 所以我们重置 no_new_count 为阈值-1，允许再滚动几次
                    if no_new_count >= MAX_NO_NEW + 2:  # 再给两次机会
                        print("多次无新图且无结束标记，停止滚动")
                        break
                    # 否则，让 no_new_count 保持为阈值，但继续滚动
                    # 我们可以把 no_new_count 置为 MAX_NO_NEW - 1，以便再尝试几次
                    # 这里简单处理：如果无新图但无结束标记，且滚动次数未满，继续滚动
                    # 但我们要避免死循环，所以设置一个额外计数器
                    # 更简洁：直接让循环继续，直到达到 max_scrolls
                    # 但为了避免无限，我们让 no_new_count 不超过 MAX_NO_NEW+2，否则退出
                    pass
            # 如果连续无新图但尚未达到阈值，继续滚动

    # 滚动结束后，再额外检查一次是否真的没有更多（用于最终提取）
    # 注意：上面循环可能因为达到 max_scrolls 或结束标记而退出

    # 提取最终URL
    final_urls = extract_image_urls_from_page(driver.page_source, download_original)
    driver.quit()
    print(f"共提取到 {len(final_urls)} 张不重复的图片")

    # 下载图片并记录元数据
    metadata = []
    for idx, url in enumerate(final_urls):
        saved_path = download_image(url, idx, keyword_folder)
        if saved_path:
            metadata.append({
                'keyword': keyword,
                'filename': os.path.basename(saved_path),
                'url': url,
                'download_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_original': download_original
            })
        time.sleep(0.5)

    if metadata:
        save_metadata(metadata)
        print(f"关键词 '{keyword}' 共下载 {len(metadata)} 张图片，元数据已记录")

    return metadata

# ================== 主程序 ==================
if __name__ == "__main__":
    # 配置
    keywords = ["初音未来"]   # 可自由修改
    DOWNLOAD_ORIGINAL = False        # True下载原图，False下载缩略图
    MAX_SCROLLS = 25               # 最大滚动次数
    SCROLL_DISTANCE = 700           # 每次滚动像素

    os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

    for kw in keywords:
        crawl_keyword(
            keyword=kw,
            download_original=DOWNLOAD_ORIGINAL,
            max_scrolls=MAX_SCROLLS,
            scroll_distance=SCROLL_DISTANCE
        )

    print("\n全部关键词处理完毕！")