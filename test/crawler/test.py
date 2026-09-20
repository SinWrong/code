import urllib.request as ur

url = "http://ip.chinaz.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
req = ur.Request(url, headers=headers)

try:
    resp = ur.urlopen(req, timeout=10)
    print("无代理访问成功，状态码:", resp.getcode())
    # 可以打印部分内容确认
    print(resp.read().decode('utf-8')[:200])
except Exception as e:
    print("无代理访问失败:", e)