"""
7.5.3  选择器
Scrapy内置了一个Selector提取模块，支持Xpath选择器、CSS选择器和正则表达式，
使用下述对应的方法解析即可。
# 下述两种方法返回一个SelectorList变量，是一个列表类型的数据，可以利用索引取出某个
# Selector元素，但是并不是真正的文本内容，可以调用extract()提取具体内容列表，或者调用
# extract_first()专门提取单一元素
response.xapth('xxx')   # Xpath选择器
response.css('xxx') # CSS选择器
# 输出结果是正则表达式的分组，顺序输出，如果只想选取第一个元素，可以调用re_first()函数，
# 和普通正则表达式的find_all和find有点类似，另外要注意Response对象不能直接调用re()和
re_first()，
# 可以先调用xpath()函数再进行正则匹配
response.xpath('xxx').re(xxx)    # 正则表达式
# 另外Xpath选择器和CSS选择器支持嵌套选择，比如
response.Xpath("//tr").css("td")
Xpath和正则表达式的语法在前面的章节已经介绍过了，这里着重介绍CSS选择器语
法，CSS三大类的选择器写法如下。
标签选择器：div{ color:red; border:1px; }
类选择器：.text{ color:red; border:1px; }
id选择器：#id { color:red; border:1px; }
"""