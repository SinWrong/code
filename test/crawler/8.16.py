#3.2 Requests HTTP请求库
import requests
"""
r1 = requests.get("http://xxx", params={"x": 1, "y": 2})
r2 = requests.post("http://xxx", data={"x": 1, "y": 2})
r3 = requests.put("http://xxx")
r4 = requests.delete("http://xxx")
r5 = requests.head("http://xxx")
r6 = requests.options("http://xxx")"""
#设置请求头：headers={'xxx':'yyy'}
#代理：proxies={'https':'xxx'}
#超时(单位秒)：timeout=15
r = requests.get('https://pixiviz.xyz/pic/148504346')
print(r,"\n")
# 直接根据键获得值
print(r.headers.get('Date'))

# 遍历获得请求头里所有键值
for key, value in r.headers.items():
    print(key + " : " + value)