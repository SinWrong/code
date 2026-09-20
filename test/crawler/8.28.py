import pymysql
db=pymysql.connect(host="localhost",port=3306,user="root",password="root")
cursor=db.cursor()
cursor.execute("Create Database If Not Exists test1 Character Set UTF8")
cursor.execute("CREATE TABLE IF Not Exists test1.person (id INT AUTO_INCREMENT PRIMARY "
          "KEY,name VARCHAR(30) NOT NULL DEFAULT '',age INT,sex CHAR(2)) ")
def insert_data(c, name, age, sex):
    data=c.execute("select * from test1.person where name=%s and age=%s and sex=%s",(name,age,sex))

    if data == 0 :
        c.execute('INSERT INTO test1.person (name, age, sex) VALUES (%s, %s, %s)', (name, age,sex))
        print("插入%s,%s,%s"%(name,age,sex))
    else:
        print("this data has existed")
insert_data(cursor, '小明', '8', '男')
insert_data(cursor, '小红', '14', '女')
insert_data(cursor, '小白', '4', '男')
insert_data(cursor, '小宝', '6', '男')
insert_data(cursor, '小莉', '16', '女')
insert_data(cursor, '小王', '20', '男')
insert_data(cursor, '小王', '21', '男')
cursor.execute("update test1.person set name='小k' where name='小王' and age='22'")
db.commit()
cursor.execute("select * from test1.person")
data=cursor.fetchall()
l_d=list(data)
print(data)
db.close()