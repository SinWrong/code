import pymysql
def create_db(database):
    conn = pymysql.connect(host="localhost", port=3306, user='root', password='root')
    cursor = conn.cursor()
    cursor.execute("Create Database If Not Exists {database} Character Set UTF8MB4".format(database=database))
    conn.close()

def create_table(c,table,attri):
    c.execute("CREATE TABLE IF Not Exists test1.{table} ({attribute})".format(table=table,attribute=attri))

def insert_into(c,database,table,attri,value):
    l_a=attri.split(',')
    l_v=value.split(',')
    equal={}
    value_n=""
    for i in range(0,len(l_a)):
        if l_a[i]=='id' or l_a[i]=='age':
            l_v[i]=int(l_v[i])
        equal[l_a[i]]=l_v[i]
        equal.setdefault(l_a[i],l_v[i])

        if l_a[i]=="name" or l_a[i]=="sex":
            value_n+="'"+str(l_v[i])+"'"+","
        else:
            value_n+= str(l_v[i])+','
    value_n = value_n.rstrip(',')
    print(equal)
    print(value_n)
    l_v=value_n.split(",")
    print(l_v)
    data=c.execute('select* from {db}.{table} where {l_a}={l_v}'.format(db=database, table=table,l_a=l_a[0],l_v=l_v[0]))
    print("查询出%s条数据"%data)
    if data==0:
        print(value_n)
        c.execute('INSERT INTO {db}.{table} ({attri}) VALUES ({value})'.format(db=database,table=table,attri=attri,value=value_n))
        print("插入成功")
    else:
        print(data)


conn = pymysql.connect(host="localhost", port=3306, user='root', password='root')
cursor = conn.cursor()
insert_into(cursor,"test1","person","name,age,sex","小王,30,男")