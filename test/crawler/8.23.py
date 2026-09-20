#3.7 实战：爬取市级编码列表
import re
import requests as r
from bs4 import BeautifulSoup

base_url = 'http://www.weather.com.cn'
city_referer_url = 'http://www.weather.com.cn/textFC/hb.shtml'


# 获取所有的城市列表
def fetch_city_url_list():
    city_url_list = []
    resp = r.get(city_referer_url)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    content = bs.find('div', attrs={'class': 'lqcontentBoxheader'})
    if content is not None:
        a_s = content.find_all('a')
        if a_s is not None:
            for a in a_s:
                city_url_list.append(base_url + a.get('href'))
    return city_url_list


def fetch_city_weather_url_list(url):
    resp = r.get(url)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    a_s = bs.select('div.conMidtab a')
    for a in a_s:
        if a.get("href") is not None and a.text != '详情' and a.text != '返回顶部':
            print(a.text + "-" + a.get("href"))

code_regex = re.compile('^.*?weather/(.*?).shtml$', re.S)
result = code_regex.match('http://www.weather.com.cn/weather/101280101.shtml')
print(result.group(1))


if __name__ == '__main__':
    fetch_city_weather_url_list('http://www.weather.com.cn/textFC/guangdong.shtml')




if __name__ == '__main__':
    city_list = fetch_city_url_list()
    for city in city_list:
            print(city)