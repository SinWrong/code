#3.4 Beautiful Soup解析库
#Beautiful Soup是一个用于解析HTML和XML结构文档的功能强大的Python库
#3.4.2 Beautiful Soup对象实例化
"""
网站 soup = BeautifulSoup(resp.read(), 'html.parser')
本地 soup = BeautifulSoup(open('index.html')，'lxml')
"""
#3.4.3 Beautiful Soup 的四大对象
"""
属性or元素or变量
1. Tag（标签）
如果查找的标签是在所有内容中第一个符合要求的标签，比较常用的两个属性如下。
 tag.name：获得标签的名称。
 tag.attrs：获取标签内的所有属性，返回一个字典，可以根据键取值，也可以直接
调用 get('xxx')获到属性。还有一个方法是根据标签层级的形式查找到标签，如
soup.body.div.div.a 就是绝对定位，实用性不高。
2. NavigableString（内部文字）
如果想获取标签的内部文字，可直接调用.string。
3. BeautifulSoup（文档的全部内容）
可以把它当作一个Tag对象，只是可以分别获取它的类型、名称，具有一级属性。
4. Comment（特殊的NavigableString）
这种对象调用.string来输出内容，会把注释符号去掉，直接把注释里的内容打印出来
"""
#3.4.4  Beautiful Soup 的各种节点
"""
当目标节点不好定位时，我们可以找到目标节点附近的节点，然后顺藤摸瓜找到目标
节点。可以通过下述字段获取附近节点。
1. 子节点与子孙节点
 contents：把标签下的所有子标签存入列表，返回列表。
 children：和 contents 一样，但是返回的不是一个列表，而是一个迭代器，只能通
过循环的方式获取信息，类型是list_iterator，仅包含tag的直接子节点，如果想找
出子孙节点，可以使用descendants，会把所有节点都剥离出来，生成一个生成器
对象<class 'generator'>。
2. 父节点与祖先节点
 parent：返回父节点tag。
 parents：返回祖先节点，返回一个生成器对象。
3. 兄弟节点
兄弟节点是处于同一层级的节点，节点不存在则返回None。
 next_sibling：下一个兄弟节点。
 previous_sibling：上一个兄弟节点。
所有兄弟节点next_siblings 和previous_sibling，返回一个生成器对象。
4. 前后节点
 next_element：下一个节点。
 previous_element：上一个节点。
所有前后节点next_elements和previous_elements，返回一个生成器对象。
"""
#3.4.5 Beautiful Soup 文档树搜索
""" 
最常用的当属find_all方法，方法定义如下：
find_all (self, name=None, attrs={}, recursive=True, text=None, limit=None, kwargs)
参数解释如下。
 name：通过HTML标签名直接搜索，会自动忽略字符串对象，参数可以是字符串、
正则表达式、列表、True或自定义方法。
 keyword：通过HTML标签的id、href（a标签）和title（class要写成class_），可
以同时过滤多个，对于不能用的tag属性，可以直接使用一个attrs字典，如find_
all(attrs={'data-foo': 'value'}。
·69·
Python 网络爬虫从入门到实践
 text：搜索文档中的字符串内容。
 limit：限制返回的结果数量。
 recursive：是否递归检索所有子孙节点。

其他方法如下。
 find(self, name=None, attrs={}, recursive=True, text=None, kwargs)：和 find_all 作用
一样，只是返回的不是列表，而是直接返回结果。
 find_parents()和 find_parent()：find_all() 和 find() 只搜索当前节点的所有子节点、
子孙节点等。find_parents() 和 find_parent()用来搜索当前节点的父辈节点，搜索
方法与普通tag的搜索方法相同，搜索文档包含的内容。
 find_next_sibling()和 find_next_siblings()：这两个方法通过 next_siblings 属性对当
前tag 的所有后面解析的兄弟 tag 节点进行迭代，find_next_siblings()方法返回所
有符合条件的后面的兄弟节点，find_next_sibling()只返回符合条件的后面的第一
个tag节点。
 find_previous_siblings()和 find_previous_sibling()：这两个方法通过 previous_
siblings 属性对当前 tag 的前面解析的兄弟 tag 节点进行迭代，find_previous_
siblings()方法返回所有符合条件的前面的兄弟节点，find_previous_sibling()方法返
回第一个符合条件的前面的兄弟节点。
 find_all_next()和 find_next()：这两个方法通过 next_elements 属性对当前 tag 之后
的tag和字符串进行迭代，find_all_next() 方法返回所有符合条件的节点，find_next()
方法返回第一个符合条件的节点。
 find_all_previous()和 find_previous()：这两个方法通过 previous_elements 属性对当
前节点前面的tag和字符串进行迭代，find_all_previous()方法返回所有符合条件的
节点，find_previous()方法返回第一个符合条件的节点。
"""
#3.4.6 css选择器
"""
Beautiful Soup 支持大部分CSS选择器，Beautiful Soup 对象调用select()方法传入字符
串参数，即可使用CSS选择器的语法来找到对应的tag。
"""
#3.5 实战爬取壁纸
import requests as r
from bs4 import BeautifulSoup

base_url = "http://www.win4000.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
theme_base_url = "http://www.win4000.com/zt/dongman.html"

# 利用列表表达式生成每页链接列表
theme_url_list = [theme_base_url + str(x) + '.html' for x in range(1, 6)]

# 套图链接列表
series_url_lists = []


# 获取所有套图的链接列表
def get_series_url_lists(url):
    resp = r.get(url,headers=headers)
    if resp is not None:
        result = resp.text
        bs = BeautifulSoup(result, 'html.parser')
        ul = bs.find('div', attrs={'class': 'tab_tj'})
        a_s = ul.find_all('a')
    for a in a_s:
            series_url_lists.append(a.get('href'))


if __name__ == '__main__':
    for url in theme_url_list:
        get_series_url_lists(url)
    print(len(series_url_lists))