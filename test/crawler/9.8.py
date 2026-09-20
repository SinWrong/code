#7.4 Spider详解
"""
在实战案例中，我们利用Scrapy Genspider生成了一个爬虫项目，默认生成了一个爬虫
类，然后可以执行scrapy crawl 爬虫名命令来运行爬虫。其实还可以把Spider当作单独的
Python 文件执行，直接使用scrapy runspider 爬虫文件命令即可执行单个爬虫文件，示例
如下：
scrapy runspider BingWallpaper.py
这也说明了Spider的重要性，其他的Item和Pipline可有可无，而Settings等也可以采
用默认配置，唯独Spider需要我们自行编写，爬取站点的链接配置、抓取和解析逻辑都在
Spider 中完成。
7.4.1  Spider 的主要属性和函数
前面已经介绍过name、allowed_domains、start_urls 这三个属性和parse()函数，下面介
绍其他内容。
 start_requests()函数：对于固定的URL，可以用start_urls 存储，而有时我们需要对
请求进行一些定制，比如使用POST请求、动态拼接参数、设置请求头等，就需
要借助 start_requests()函数了。该函数必须返回一个可迭代对象（iterable），该对
象包含用于爬取的第一个Request。另外，要注意Spider 中未指定start_urls 时，
该函数才会生效。
 custom_settings：字典，专属于本Spider类的配置，该配置会覆盖项目中的settings.py
的值，慎用。有些值覆盖了也不一定会起作用，该设置须在初始化前被更新，并
且必须定义成类变量。
 settings：settings 对象，利用它可以直接获取项目的全局设置变量。
 crawler：定义 Spider 实例绑定的 crawler 对象，该属性在初始化 Spider 类时由
from_crawler()函数设置，crawler 对象包含了很多项目组件，利用它可以获取项目
的一些配置信息。
 closed(reason)：Spider 关闭时，该函数会被调用，参数是一个字符串，即结束原
因，一般会在这个函数里写一些释放资源的收尾代码。
另外还有一点要注意，parse()函数作为默认的回调函数，在Request没有指定回调方法
时会调用它，该回调方法的返回值只能是Request、字典和 Item 对象，或者它们的可迭代
对象。
"""
#7.5 request类和response类
"""
在Spider 中生成Request后，经过一系列的调度传递到Downloader（下载器），下载器
执行后返回一个Response对象，返回到发出请求的爬虫程序，然后在回调方法中解析这个
Response，接下来我们详细介绍这两个类。 
7.5.1  Request 详解 
常用参数与方法如下。 
 url：设置请求的URL。 
 method：设置请求方法，默认为GET。 
 body：设置请求体。 
 callback：设置请求完成后返回的Response类的回调函数。 
 headers：设置请求的Headers数据。 
 cookies：设置页面的Cookies，可以是dict或list[dict]。 
 encoding：设置请求的转换编码。 
 priority：链接优先级，优先级越高，越优先爬取。 
 dont_filter：指定请求是否被Scheduler过滤（Scheduler 默认过滤重复请求），慎用。 
 errback：设置处理异常的回调函数。 
 copy()：复制当前Request。 
 replace()：对 Request 对象参数进行替换。 
 meta：一个包含Request任意元数据的dict，主要用于解析函数间的值传递、浅拷贝。 
举个简单的例子：prase_1 函数中给 Item 某些字段提取了值，但另外一些值需要在
parse_2 中提取，这时就需要把parse_1中的Item传递给parse_2进行处理，因为parse_2是
回调函数，显然无法只以设置外参的方式传递，此时就可以利用meta这个属性了，最典型
的就是爬取电商站点，大图都需要打开，能拿到商品名称和价格，但是还想获得单击商品
后显示的大图，假设大图的链接在代码中，
"""
