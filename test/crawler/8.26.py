#4.3 用Excel文件存储数据
"""
Excel相比CSV功能会多一些，比如支持设置字体颜色和样式，而Python操作Excel
可以用两个库：xlwt（写Excel） 和 xlrd（读Excel）
"""
#4.3.1 Excel写入
"""
xlwt库中有关写入的函数如下所述。 
xlwt.Workbook()：创建一个工作簿。 
Python 网络爬虫从入门到实践 
 工作簿对象.add_sheet(cell_overwrite_ok=True)：添加工作表，括号里是可选参数，
用于确认同一个cell（单元）是否可以重设值。 
 工作表对象.write(行号,列号,插入数据,风格)：第四个参数可选。 
 工作簿对象.save(Excel文件名)：保存到Excel文件中。 
"""
import xlwt #该库只能用于写入二进制xls文件
import xlrd
import os
save_path=r"E:/savepath/"
if __name__ == '__main__':
    workbook=xlwt.Workbook(encoding="utf-8")
    sheet=workbook.add_sheet("工作表1",cell_overwrite_ok=True)
    sheet.write(0,0,'学号')
    sheet.write(0,1,'姓名')
    sheet.write(1,0,'1')
    sheet.write(1,1,'ll')
    workbook.save(os.path.join(save_path,"result.xls"))

#4.3.2 Excel读取
"""
xlrd 库中有关读取的函数如下所述。 
 xlrd.open_workbook()：读取一个 Excel 文件，获得一个工作簿对象。 
 工作簿对象.sheets()[0]：根据索引获得工作簿里的一个工作表。 
 工作表对象.nrows：获得行数。 
 工作表对象.ncols：获得列数。 
 工作表对象.row_values(pos)：读取某一行的数据，返回的结果是列表类型。
"""
workbook=xlrd.open_workbook(os.path.join(save_path,"result.xls"))
sheet=workbook.sheets()[0]
print(sheet)
ncount=sheet.nrows
for i in range(0,ncount):
    print(sheet[i])
    print(sheet.row_values(i))