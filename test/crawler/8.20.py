#3.3.4 爬取视频
import requests
from lxml import etree
import time
"""url=""
headers={
    "Host":"www.bilibili.com",
    "User-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

         }
resp=requests.get(url,headers=headers).text
html=etree.HTML(resp)

"""
test_url = 'https://www.bilibili.com/video/BV1XUhK6QETJ/'
# 视频获取的接口URL
video_parse_url = 'http://v.ranks.xin/video-parse.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
# 视频获取接口的请求头
video_parse_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko)',
'Host': 'v.ranks.xin',
'Referer': 'http://v.ranks.xin/',
'X-Requested-With': 'XMLHttpRequest'
}
save_path=r"E:/savepath/video/"
# 解析获得视频链接
def get_video_url(content):
    video_list = content.xpath("//iframe/@data-src")
    print(video_list)
    for video in video_list:
        download_video(video)
    # 下载视频的方法
def download_video(url):
    print("开始解析视频链接：" + url)
    video_resp = requests.get(video_parse_url, headers=video_parse_headers, params=
    {'url': url})
    if video_resp is not None:
        video_url = video_resp.json()['data'][0]['url']
        print("解析完成，开始下载视频:" + video_url)
        try:
            video_name = str(int(time.time())) + '.mp4'  # 使用当前时间戳作为视频名称
            video_resp = requests.get(video_url).content
            if video_resp is not None:
                with open(save_path+video_name, "wb+") as f:
                    f.write(video_resp)
                    print("视频下载完成:" + video_name)
        except Exception as reason:
            print(str(reason))


if __name__ == '__main__':
    resp = requests.get(url=test_url, headers=headers).text
    print(resp)
    html = etree.HTML(resp)
    get_video_url(html)