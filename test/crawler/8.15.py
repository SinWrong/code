#2.3 用lxml库解析网页节点
#通过 urllib 库可以模拟请求，得到网页的内容，但是在大多数情况下我们并不需要整个网页，而只需要网页中某部分的信息。
#可以利用解析库 lxml 迅速、灵活地处理 HTML或XML，提取需要的信息。
#另外，该库支持XPath的解析方式，效率也非常高。lxml库的官方文档为https://lxml.de/tutorial.html。

#XPath（XML Path Language，XML 路径语言），用于在XML文档中查找信息。
#它既适用于XML文档的搜索，又适用于HTML。
#其核心是按照规则，通过编写路径选择表达式来筛选节点。
"""
1. 绝对路径和相对路径
绝对路径：用/表示从根节点开始选取。
相对路径：用//表示选择任意位置的节点，而不考虑它们的位置。
另外，可以使用*（通配符）来表示未知的元素。除此之外，还有两个选取节点的标
记（.和..），前者用于选取当前节点，后者用于选取当前节点的父节点。
"""
import random

"""
2. 选择分支定位 
比如存在多个元素，想唯一定位，可以使用[]来选择分支，分支的下标从 1 开始，相
关的规则如下。 
/tr/td[1]：取第一个td 
/tr/td[last()]：取最后一个td 
/tr/td[last()-1]：取倒数第二个td 
/tr/td[position()<3]：取第一个和第二个td 
/tr/td[@class]：选取拥有class属性的td 
/tr/td[@class='xxx']：选取拥有class属性为xxx的td 
/tr/td[count>10]：选取 price 元素的值大于10的td
"""
"""
3. 选择属性 
还可以通过多个属性定位，比如可以这样写： 
/tr/td[@class='xxx'][@value='yyy']或者/tr/td[@class='xxx' and @value='yyy']
"""
"""
4. 常用函数 
除了last()、position()，还有以下常用函数。 
contains(string1,string2)：如果前后匹配则返回 True；否则返回 False。 
text()：获取元素的文本内容。 
starts-with()：从起始位置匹配字符串。 
更多的函数可以访问http://www.w3school.com.cn/xpath/xpath_functions.asp 自行查阅。
"""
"""
5. 轴 
当上面的操作都不能定位时，可以考虑根据元素的父节点或兄弟节点来定位，这时就
会用到XPath轴，利用轴可定位某个相对于当前节点的节点集，语法为轴名称::标签名.

ancestor :选取当前节点的所有先辈（父、祖父等） 
ancestor-or-self :选取当前节点的所有先辈（父、祖父等）及当前节点本身 
attribute :选取当前节点的所有属性 
child :选取当前节点的所有子元素
descendant :选取当前节点的所有后代元素（子、孙等） 
descendant-or-self :选取当前节点的所有后代元素（子、孙等）及当前节点本身 
following :选取文档中当前节点的结束标签之后的所有节点 
following-sibling :选取当前节点之后的所有兄弟节点 
namespace :选取当前节点的所有命名空间节点
parent :选取当前节点的父节点
preceding :选取文档中当前节点的开始标签之前的所有节点 
preceding-sibling :选取当前节点之前的所有同级节点 
self :选取当前节点 
"""
#2.4 爬取小说
import urllib
import urllib.request
import urllib.parse
from lxml import etree
from urllib import error
import lxml.html
import os
import time
r=0
novel_base_url="https://www.wenku8.net/novel/1/1973/" #小说站点链接
novel_url=urllib.parse.urljoin(novel_base_url,"index.htm")
print(novel_url)
chapter_url_list=[]#用于存储每章小说的链接
headers={
    "Host":"www.wenku8.net",
    "Referer":"https://www.wenku8.net",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0"

}
bookname="实力至上主义教室"
novel_save_path=r"E:/savepath/novel/%s/"%bookname
def round(x,y):
    i=0
    a=5
    a_l=[]
    time.sleep(y)
    for i in range(0,x):
        a+=5
        a_l.append(a)
    return a_l


def clawer_chapter_link(x,y,h,r):
    time.sleep(0.6)
    req = urllib.request.Request(url=x, headers=h)
    html = lxml.html.parse(urllib.request.urlopen(req))
    print(html)
    hrefs = html.xpath('//td/a/@href')
    for href in hrefs[r*5:r*5+5]:
        chapter_url_list.append(urllib.parse.urljoin(y, href))
    print(chapter_url_list)

clawer_chapter_link(novel_url,novel_base_url,headers,2)

def save_novel(t,c):
    try:
        if not os.path.exists(novel_save_path):
            os.mkdir(novel_save_path)
        with open(novel_save_path+t+'.txt',"w+",encoding="utf-8") as f:
            f.write(c.strip())
    except(error.HTTPError,OSError) as reason:
        print(str(reason))
    else:
        print("Download finished:",t)

def get_novel_content(x,h):
    time.sleep(random.randint(1,10))
    req = urllib.request.Request(url=x, headers=h)
    html = lxml.html.parse(urllib.request.urlopen(req))
    title=html.xpath('//*[@id="title"]/text()')[0]
    print(title)
    contents=html.xpath('//*[@id="content"]/text()')
    content=""
    for i in contents:
        content+=i+"\r"
    save_novel(title,content)

for chapter in chapter_url_list:
    r+=1
    print(r)
    get_novel_content(chapter,headers)
    if r%4==0:
        time.sleep(random.randint(1,10))

