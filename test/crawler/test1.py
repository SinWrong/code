import requests
from urllib.parse import quote,unquote
url='https://pixiviz.xyz/' #url:统一资源定位符 网址 链接
#输入--初音 明文   /  发送请求--%E5%88%9D%E9%9F%B3 密文
#quote() 明转密 unquote() 密转明
print(quote('初音')) #传入参数类型：字符串
print(unquote("%E5%88%9D%E9%9F%B3")) #传入参数类型：%xx%xx
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'}
#UAlist={}(反爬UA池) random.choice(UAlist) import random
#User-Agent.random() from fake_useragent import UserAgent (与UA池一个效果，但可能异常)
response=requests.get(url,headers=headers) #request.get:发送http请求 response:响应结果
print(response) #状态码
print(response.reason)

#print(response.text) #响应内容（text：str）
print(response.content.decode()) #解码响应内容（content：byte 文本如果乱码可用；decode()：解码）
print(len(response.content.decode()))
print(response.request.headers)
with open(r'E:/新建文件夹/pixiviz.html','w',encoding='utf-8')as f: #用于保存响应内容
    f.write(response.content.decode())