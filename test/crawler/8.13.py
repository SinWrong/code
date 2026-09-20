#2.2.3 模拟get和post请求
import urllib.request
import json
import ssl
get_url = "https://jsonplaceholder.typicode.com/users"
print(get_url)
get_resp = urllib.request.urlopen(get_url)#打开链接
get_result = json.loads(get_resp.read().decode('utf-8'))#json->python
# 后面的参数用于格式化JSON输出格式
get_result_format = json.dumps(get_result, indent=2,
                               sort_keys=True,  ensure_ascii=False)#python->json
print(get_result_format)