#3.3.2 爬取图片
import time

import requests
from lxml import etree

test_url = 'https://mp.weixin.qq.com/s/JHioeDcopm-98R5lGVemqw'
headers = {
    'Host': 'mp.weixin.qq.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
save_path=r"E:/savepath/picture/"
resp = requests.get(url=test_url, headers=headers)

resp_t=resp.text
html = etree.HTML(resp_t)
print(html)

def claw_title():
    resp = requests.get(url=test_url, headers=headers).text
    html = etree.HTML(resp)
    h2 = html.xpath("//span[@class='js_title_inner']/text()")
    print(h2[0])
def download_pic(url):
    print("download_pic:%s"%url)

    try:
        pic_name = url.split("/")[-2]
        print("p_c:",pic_name)
        if "="not in url:
            fmt=url.split('/')[-3]
            fmt=fmt.split('_')[1]
        else:
            fmt = url.split('=')[-1]  # 图片格式
        print("fmt:",fmt)
        time.sleep(0.5)
        img_resp = requests.get(url).content
        with open(save_path+pic_name + "." + fmt, "wb+") as f:
            f.write(img_resp)
    except Exception as reason:
        print(str(reason))
def get_pic(c):
    time.sleep(0.5)
    pic_l=c.xpath("//*/img/@data-src")
    for pic in pic_l:
        download_pic(pic)
def claw_pic():
    return 0

claw_title()
get_pic(html)