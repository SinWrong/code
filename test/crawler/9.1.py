#5.3.4  redis实战:获取b站弹幕
import redis
#r=redis.StrictRedis(host="127.0.0.1",port=6379,db=0)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='123456')
r = redis.StrictRedis(connection_pool=pool)
import requests as r
from bs4 import BeautifulSoup
import re
video_url = 'https://www.bilibili.com/video/BV1xcdaBMEkS'
cid_regex = re.compile(r'.*?//space.bilibili.com/.*', re.S)
xml_base_url = 'http://comment.bilibili.com/'
# 获取弹幕的cid
def get_cid():
    resp = r.get(video_url).text
    print(resp)
    bs = BeautifulSoup(resp, 'lxml')
    src = bs.select('div a')[1].input
    cid = cid_regex.match(str(src)).group(1)
    return cid

    # 解析获取弹幕
def analysis_d(cid):
    count = 1
    url = xml_base_url + cid + '.xml'
    resp = r.get(url)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    d_s = bs.find_all('d')
    for d in d_s:
        dan_redis.set(str(count), d.text)
        count += 1
    print("写入完毕~")
if __name__ == '__main__':
    # 连接redis
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='123456', db=0)
    dan_redis = redis.StrictRedis(connection_pool=pool)
    analysis_d(get_cid())