#6.4 selenium
"""
6.4.1  Selenium 简介
Selenium 是一个用于Web应用程序测试的工具，通过它我们可以编写代码，让浏览器
完成如下任务：
 自动加载网页，获取当前呈现页面的源码。
·166·
第6章  Python应对反爬虫策略
 模拟单击和其他交互方式，最常用的是模拟表单提交（如模拟登录）。
 页面截屏。
 判断网页某些动作是否发生等。
Selenium 是不支持浏览器功能的，需要和第三方的浏览器一起搭配使用，支持下述浏
览器，需要把对应的浏览器驱动下载到Python的对应路径下。
 Chrome：https://sites.google.com/a/chromium.org/chromedriver/home
 Firefox：https://github.com/mozilla/geckodriver/releases
 PhantomJS：http://phantomjs.org/
 IE：http://selenium-release.storage.googleapis.com/index.html
 Edge：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
 Opera：https://github.com/operasoftware/operachromiumdriver/releases
"""
from selenium import webdriver
browser = webdriver.Chrome()  # 调用本地的Chrome浏览器
browser.get('http://www.baidu.com')  # 请求页面，会打开一个浏览器窗口
html_text = browser.page_source  # 获得页面代码
browser.quit()  # 关闭浏览器
print(html_text)