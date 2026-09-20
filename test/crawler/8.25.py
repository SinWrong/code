#4.1.2 csv读取
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

with open (save_file_name2,"r")as f1: #原save_file_name1文件用于测试不使用newline会产生空行，故用save_file_name2
    reader1=csv.reader(f1)
    #print(list(reader1))       #reader1转换为list类型时，会与它reader类型本身的可迭代性产生冲突(只能迭代一次,只能使用一次)，
                                # 导致原reader类型遍历的时候无法正常打印
    #print(list(reader1)[0][1]) #list 索引超出范围，需要先将reader1转换为python可正常读取的list类型才可索引
    print(reader1)
    head_row=next(reader1)      #next一次获取一行，line_num对应行号
    print(reader1.line_num,head_row)
    for row in reader1:
        print(reader1.line_num,row)
