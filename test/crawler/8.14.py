#2.2.4 修改请求头
import time
import urllib.request as ur
from http import cookiejar

"""link="https://www.wenku8.net/novel/1/1973/index.htm"
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                         'AppleWebKit/537.36 (KHTML, like Gecko)' 
                         ' Chrome/63.0.3239.84 Safari/537.36',
           'Referer': 'http://www.baidu.com',
           'Connection': 'keep-alive'}
l_solve=ur.Request(link,headers=headers)
rq=ur.urlopen(l_solve)"""
#print(rq.read().decode("GBK"))

#2.2.5 设置连接超时
#rq=ur.urlopen(l_solve,timeout=20)

#2.2.6 延迟提交数据
#time.sleep()

#2.2.7 设置代理
"""
ip_query_url = "http://ip.chinaz.com/"
# 1.创建代理处理器，ProxyHandler参数是一个字典{类型:代理IP:端口}
#proxy_support = ur.ProxyHandler({'http': 'https://114.239.30.163:23358'})
# 2.定制，创建一个opener
#opener = ur.build_opener(proxy_support)
# 3.安装opener
#ur.install_opener(opener)
# 请求头
headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)' 
' AppleWebKit/537.36 (KHTML, like Gecko)' 
' Chrome/63.0.3239.84 Safari/537.36',
'Host': 'ip.chinaz.com'
}
req = ur.Request(ip_query_url, headers=headers)
resp= ur.urlopen(req)
#resp = opener.open(req)#opener用于代替urlopen，urlopen有些功能无法实现（代理，cookie等其他高级功能），如果要实现代理，需要自定义opener而不是urlopen
html = resp.read().decode('utf-8')
print(html)
#如有失败，源于代理问题"""

#2.2.8 Cookie
"""
# 1.实例化CookieJar对象
cookie = cookiejar.CookieJar()
# 2.创建Cookie处理器
handler = ur.HTTPCookieProcessor(cookie)
# 3.通过CookieHandler创建opener
opener = ur.build_opener(handler)
ck=''
# 4.打开网页
resp = opener.open("https://zh.bit.edu.cn/")
for i in cookie:
    print("Name = %s" %i.name)
    print("Value = %s" %i.value)

# ============ 保存Cookie到文件 ============
# 1.用于保存Cookie的文件
cookie_file = r"E://cookie.txt"
# 2.创建MozillaCookieJar对象保存Cookie
cookie = cookiejar.MozillaCookieJar(cookie_file)
for i in cookie:
    print("Name = %s" %i.name)
    print("Value = %s" %i.value)
# 3.创建Cookie处理器
handler = ur.HTTPCookieProcessor(cookie)
# 4.通过CookieHandler创建opener
opener = ur.build_opener(handler)
# 5.打开网页
resp = opener.open("http://www.baidu.com")
# 6.保存Cookie到文件中，参数依次是:
# ignore_discard：即使Cookie将被丢弃也将它保存下来
# ignore_expires：如果在该文件中Cookie已存在，覆盖原文件写入
cookie.save(ignore_discard=True, ignore_expires=True)

# ============ 读取Cookie文件 ============
cookie_file = r"E://cookie.txt"
# 1.创建MozillaCookieJar对象保存Cookie
cookie = cookiejar.MozillaCookieJar(cookie_file)
# 2.从文件中读取Cookie内容
cookie.load(cookie_file, ignore_expires=True, ignore_discard=True)
handler = ur.HTTPCookieProcessor(cookie)
opener = ur.build_opener(handler)
resp = opener.open("http://www.baidu.com")
print(resp.read().decode('utf-8'))
"""

#2.2.9 urllib.parse模块
#urlparse函数：将URL拆分成六大组件。
#urlsplit函数：和urlparse函数类似，只是不会单独拆分params部分。
import urllib.parse
urp = urllib.parse.urlparse('https://docs.python.org/3/search.html?q=parse&check_keywords=yes&area=default')
print('urlparse执行结果：', urp)
# 可以通过.的方式获取某个部分
print('urp.scheme：', urp.scheme)
print('urp.netloc：', urp.netloc)
urp =urllib.parse.urlsplit('https://docs.python.org/3/search.html?q=parse&check_keywords=yes&area=default')
print('urlsplit执行结果：', urp)

#urlunparse函数：接收一个可迭代的对象，长度为7，以此构造一个URL。
#urlunsplit函数：接收一个可迭代的对象，长度为6，以此构造一个URL。
#urljoin函数：比上面两种方法简单得多，只有两个参数（基础链接、新链接），该方法会分析基础链接的scheme、netloc和path的内容，并对新链接缺失的部分进行补充。
url=urllib.parse.urlunparse(['https','docs.python.org','/3/search.html','q=parse&check_keywords= yes&area=default' , '', ''])
print('urlunparse函数拼接的URL：',url)
url=urllib.parse.urlunsplit(['https','docs.python.org','/3/search.html','q=parse&check_keywords= yes&area=default',''])
print('urlunsplit函数拼接的URL：',url)
url = urllib.parse.urljoin('https://docs.python.org','/3/search.html')
url = urllib.parse.urljoin(url,'?q=parse&check_keywords=yes&area=default')
print('urljoin函数拼接的URL：',url)

#urlencode函数：将字典形式的数据转换为查询字符串，常用于构造GET请求。
from urllib import parse

params = {
    'q': 'parse',
    'check_keywords': 'yes',
    'area': 'default'
}
url = 'https://docs.python.org/3/search.html?' + parse.urlencode(params)
print("拼接后的URL：", url)

#parse_qs 函数：把GET请求后跟着的查询字符串反序列化为字典。
#parse_qsl 函数：把GET请求后跟着的查询字符串反序列化为列表。
from urllib import parse
params_str = 'q=parse&check_keywords=yes&area=default'
print("parse_qs 反序列化结果：", parse.parse_qs(params_str))
print("parse_qsl 反序列化结果：", parse.parse_qsl(params_str))

#2.2.10 urllib.error 异常处理模块
#urllib.error 模块定义由 urllib.request 引发的异常类，异常处理主要用到两个类——URLError 和 HTTPError。
#URLError类：urllib.error 异常类的父类，具有reason属性，返回错误原因。发生URLError异常的原因一般有以下几种：
# 远程地址不存在（如404 Not Found）。
# 触发了HTTPError异常（如403 Forbidden）。
# 远程服务器不存在（如[Errno 11001] getaddrinfo failed）。
# 远程服务器连接不上（如[WinError 10060]，由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败）。
#HTTPError 类：URLError 类的子类，专门处理 HTTP 和 HTTPS 请求错误。具有三个属性：code（请求返回的状态码）、headers（请求返回的响应头信息）和reason（错误原因）。
#HTTPError 类并不能处理父类支持的异常处理，建议对两种异常分开捕获
from urllib import request, error
try:
    response = request.urlopen('http://www.baidu.com/')
    print(response)
except error.HTTPError as e:
    print('HTTPError 异常')
    print('reason:'+ str(e.reason), 'code:'+str(e.code), 'headers:'+str(e.headers), sep='\n')
except error.URLError as e:
    print('URLError 异常')
    print('reason:'+ str(e.reason))
else:
    print('Request Successfully')

#2.2.11 urllib.robotparser模块
#Robots协议，又称爬虫协议，网站可以通过该协议告知搜索引擎站点内的哪些网页可以抓取，哪些不可以抓取。如果想使用这个协议，可以在网站的根目录下创建一个robots.txt文本文件。
#当搜索爬虫访问某个站点时会先检查是否有这个文件，如果有的话，会根据文件中定义的爬取范围来爬取；如果没有找到的话，便会访问所有可以直接访问的页面。
#另外有一点要注意，Robots协议只是一个道德规范，并不是强制命令或防火墙。
from urllib import robotparser

rp = robotparser.RobotFileParser()
# 设置robots.txt文件的链接
rp.set_url('http://www.taobao.com/robots.txt')
# 读取robots.txt文件并进行分析
rp.read()
url = 'https://www.douban.com'
user_agent = 'Baiduspider'
op_info = rp.can_fetch(user_agent, url)
print("Elsespider 代理用户访问情况：",op_info)
bdp_info = rp.can_fetch(user_agent, url)
print("Baiduspider 代理用户访问情况：",bdp_info)
user_agent = 'Elsespider'