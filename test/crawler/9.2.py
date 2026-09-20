#6.3.1  Ajax 动态加载数据
"""
Ajax 是在不重新加载整个网页的情况下，对网页的某部分进行更新的技术。这在采用
瀑布流布局或内容分页的站点中很常见，访问网页时将网页框架返回给浏览器，浏览器在
交互过程中产生异步Ajax请求获取数据包，解析后呈现到网页上。
应对策略是抓包，比如Chrome浏览器会过滤XHR（XML HTTP Request）的请求，这
是浏览器后台与服务之间交换数据的文件，一般为JSON或XML格式，当然有些站点会对
这个链接进行加密，如参数加密或返回加密。我们通过下面这个实例来了解Ajax动态加载
数据，以及如何提取数据。
"""
#6.3.2 Ajax实战:素材网内容分析
import requests as r
import os
import re
import json
# 图片URL拼接的前缀和后缀
img_start_url = 'http://img.hb.aicdn.com/'
img_end = '_fw658'
# 图片key的保存文件
pic_key_file = 'pin_ids.txt'
# 获取pins的正则
boards_pattern = re.compile(r'pins":(.*)};')
# 修改pin_id的正则
max_pattern = re.compile(r'(?<=max=)\d*(?=&limit)')
# 图片保存路径
pic_download_dir = os.path.join(os.getcwd(), 'HuaBan/')
# Ajax模拟的请求头
ajax_headers = {
    'Host': 'huaban.com',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}


# 以追加的形式向文件中写入内容
def write_str_data(content, file_path):
    try:
        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write(content + "\n", )
    except OSError as reason:
        print(str(reason))

    # 按行读取文件里的内容，添加到列表中，返回


def load_data(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        return data_list

    # 获得borads页数据，提取key列表写入文件，并返回最后一个pid_id用于后续查询


def get_boards_index_data(url):
    print("请求：" + url)
    resp = r.get(url).text
    result = boards_pattern.search(resp)
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        write_str_data(item['file']['key'], pic_key_file)
        # 返回最后一个pin_id
    pin_id = json_dict[-1]['pin_id']
    return pin_id


# 模拟Ajax请求更多数据
def get_json_list(url):
    print("请求：" + url)
    resp = r.get(url, headers=ajax_headers)
    if resp is None:
        return None
    else:
        json_dict = json.loads(resp.text)
        pins = json_dict['board']['pins']
        if len(pins) == 0:
            return None
        else:
            for item in pins:
                write_str_data(item['file']['key'], pic_key_file)
    return pins[-1]['pin_id']


# 下载图片的方法
def download_pic(key):
    url = img_start_url + key + img_end
    resp = r.get(url).content
    try:
        print("下载图片：" + url)
        pic_name = key + ".jpg"
        with open(pic_download_dir + pic_name, "wb+") as f:
            f.write(resp)
    except (OSError, r.HTTPError, r.ConnectionError, Exception) as reason:
        print(str(reason))


if __name__ == '__main__':
    if not os.path.exists(pic_download_dir):
        os.makedirs(pic_download_dir)
        # 判断图片key的保存文件是否存在，存在的话删除
    if os.path.exists(pic_key_file):
        os.remove(pic_key_file)
        # 一个画板链接，可自行替换
    boards_url = 'http://huaban.com/boards/279523/'
    board_last_pin_id = get_boards_index_data(boards_url)
    board_json_url = boards_url + '?jl58nz3i&max=43131274&limit=20&wfl=1'
    while True:
        board_last_pin_id = get_json_list(max_pattern.sub(str(board_last_pin_id),
                                                          board_json_url))
        if board_last_pin_id is None:
            break
    pic_url_list = load_data(pic_key_file)
    for key in pic_url_list:
        download_pic(key)
    print("所有图片下载完成～")