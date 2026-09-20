import requests
from lxml import etree
url="https://pixiviz.xyz/pic/148504346"
headers={
    "Host":"pixiviz.xyz",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
resp=requests.get(url,headers=headers)
print("resp:",resp)
response=resp.text
print("resp.text:",response)
resp_e=etree.HTML(response)
print("etree.html:",resp_e)
pic_tile=resp_e.xpath('//div[@class="pic-presentation-info-title"]/text()')

print(pic_tile[0])

