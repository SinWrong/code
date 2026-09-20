#4.1 用CSV文件存储数据
"""
CSV（Comma-Separated Values）其实就是纯文本，用逗号分隔值，可以分隔成多个单
元格。CSV文件除了可以用普通的文本编辑工具打开，还能用Excel打开，但CSV和Excel
有以下不同：
 所有值都是字符串类型。
 不支持设置字体颜色和样式。
 不能指定单元格宽、高或合并单元格。
Python网络爬虫从入门到实践
 ·86·
没有多个工作表。
不能嵌入图片、图表。
Python中内置了一个csv模块用来处理CSV文件。
"""
#4.1.1 CSV写入
"""
csv模块提供了两个写入的函数。 
writerow：写入一行。 
writerows：写入多行。
"""
import os
import csv
save_path=r"E:/savepath/csv/"
save_file_name1=os.path.join(os.getcwd(),"1.csv")
save_file_name2=os.path.join(os.getcwd(),"2.csv")
save_file_name3=save_path+"3.csv"
data_1 = [['id', '姓名', '性别', '年龄', '工作'],
          [1, '小明', '男', '18', '学生'],
          [2, '小红', '女', '24', '老师'],
          [3, '小光', '男', '25', 'Python工程师']]
headers= ['id', '姓名', '性别', '年龄', '工作']
data_2= [{'id': 1, '姓名': '小明', '性别': '男', '年龄': '18', '工作': '学生'},
          {'id': 2, '姓名': '小红', '性别': '女', '年龄': '24', '工作': '老师'},
          {'id': 3, '姓名': '小光', '性别': '男', '年龄': '25', '工作': 'Python工程师'}]
with open(save_file_name1,"w")as f1:#不加newline会写入空行
    writer1=csv.writer(f1)
    for row in data_1:
        writer1.writerow(row)
        print(row)

with open(save_file_name2,"w",newline="")as f2:
    writer2=csv.writer(f2)
    writer2.writerows(data_1)

with open(save_file_name3,"w",newline="")as f3:
    writer3=csv.DictWriter(f3,headers)
    writer3.writeheader()
    writer3.writerows(data_2)