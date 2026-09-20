import urllib.request #urlib库（是一个http请求库）的请求模块：打开和浏览url内容
from PIL import Image
import cv2
#2.2.1 发送请求
resp = urllib.request.urlopen("http://www.baidu.com") #urlopen返回http回复对象
element=['geturl','msg','status','version','reason','debuglevel','getheaders']
print(resp,"\n")
def openimg(x):
    img=Image.open(x)
    img.show()
def change(i):
    x=0
    if i=='msg':
        x=resp.msg
    if i=='status':
        x=resp.status
    if i=='version':
        x=resp.version
    if i=='reason':
        x=resp.reason
    if i=='debuglevel':
        x=resp.debuglevel
    return x
for i in element:
    a=change(i)
    if i=='geturl':
        print("resp.%s:"%i,resp.geturl(),end="\n")
    if i=='getheaders':
        print("resp.%s:" % i, resp.getheaders()[0:2],end="\n")
    else:
        print("resp.%s:"%i,"%s"%a,end="\n")
print("\n")
#print(resp.read().decode("utf-8")) #read返回二进制字符串，需要decode解码uft-8才可正常阅读
print(urllib.request.quote("http://www.baidu.com")) #url含有汉字不符合标准，需要编码
print(urllib.request.unquote("http%3A//www.baidu.com"))

#2.2.2 抓取二进制文件
pic_url = "https://www.baidu.com/img/bd_logo1.png"
pic_resp = urllib.request.urlopen(pic_url)
pic = pic_resp.read()
img_path=r"E://bd_logo.png"
with open(img_path, "wb") as f:
    f.write(pic)
openimg(img_path)
"""  
#若因ssl证书验证而报错导致无法下载图片
import ssl
# 方法一：全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context
# 方法二：使用ssl创建未经验证的上下文，在urlopen()中传入上下文参数
context = ssl._create_unverified_context()
pic_resp = urllib.request.urlopen(pic_url,context=context)
# 方法三
urllib.request.urlretrieve(pic_url, 'bd_logo.png')
"""


