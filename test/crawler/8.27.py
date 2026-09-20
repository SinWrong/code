#5.1.9 MySQL数据库语法速成
"""
1. MySQL 数据类型
数据类型就是定义存储什么类型的数据，如数字、日期、字符串等。举个简单的例子，
你想保存一个数字，就要定义一个数字类型的字段，而不能定义一个数字类型的字段，然
后往里面放字符串。
MySQL中支持以下几种数据类型：
①整型（取值范围如果加了unsigned，则最大值翻倍）
 TINYINT(m)：1字节，范围为-128~127。
 SMALLINT(m)：2字节，范围为-32 768~32 767。
 MEDIUMINT(m)：3字节，范围为-8 388 608~8 388 607。
 INT(m)：4字节，范围为-2 147 483 648~2 147 483 647。
 BIGINT(m)：8字节，范围为±9.22×1018。
②浮点型
 FLOAT(m,d)：单精度浮点型，8位精度（4字节），m为总个数，d为小数位。
 DOUBLE(m,d)：双精度浮点型，16位精度（8字节），m为总个数，d为小数位。
③字符串
 CHAR类型的字符串检索速度要比VARCHAR类型快。
 TEXT类型不能有默认值，VARCHAR查询速度快于TEXT。
 CHAR(n)：固定长度，最多255个字符。
 VARCHAR(n)：可变长度，最多65 535个字符。
 TINYTEXT：可变长度，最多255个字符。
 TEXT：可变长度，最多65 535个字符。
 MEDIUMTEXT：可变长度，最多224-1个字符。
 LONGTEXT：可变长度，最多232-1个字符。
④二进制数据
 _BLOB：以二进制方式存储，不分大小写，不用指定字符集，只能整体读出。
 _TEXT：以文本方式存储，英文存储区分大小写，可以指定字符集。
⑤日期时间类型
 DATE：日期。
 TIME：时间。
 DATETIME：日期时间。
 TIMESTAMP：自动存储记录修改时间。
2. 数据类型的属性
数据类型的属性就是对字段加一些限定条件，如设置默认值，如果写入记录没有这个
字段，就把该字段的值设置为默认值。除此之外，还有主键和字段是否为空等，相关的属
性如下所示。
 NULL：数据列可包含NULL值，就是可以不设置值。
 NOT NULL：数据列不允许包含NULL值。
 DEFAULT：默认值。
 PRIMARY KEY：主键。
 AUTO_INCREMENT：自动递增，适用于整数类型。
 UNSIGNED：无符号。
 CHARACTER SET name：指定一个字符集。
3. 库操作
MySQL提供了如下库操作命令。
①建库。
CREATE DATABASE 数据库名;
②删库（删除的数据库无法恢复）。删除不存在的库会报database doesn't exist的错误，
故删库前要先用IF EXISTS进行判断。
DROP DATABASE IF EXISTS 数据库名;
4. 表操作
MySQL提供的与表操作相关的命令如下：
# 建表，比如
CREATE TABLE test
(
_id
VARCHAR(50)
NOT NULL PRIMARY KEY,
·107·
Python网络爬虫从入门到实践
 ·108·
  dsec     TEXT                     NULL,
  images  TEXT                     NULL,
  url      TEXT                     NULL,
  type     VARCHAR(50) DEFAULT ''   NULL
);
# 清空表数据，整体删除，速度较快，会重置Identity（标识列、自增字段）
TRUNCATE 表名
# 删除表数据，逐条删除，速度较慢，不会重置Identity，配合WHERE关键字可以删除部分数
据
DELETE FROM 表名
# 删表
DROP TABLE 表名
# 重命名表
ALTER TABLE 原表名 RENAME 新表名;
RENAME TABLE 原表名 TO 新表名;
# 增加列
ALTER TABLE 表名 Add column 新字段 数据类型 AFTER 在哪个字段后添加
# 删除列
ALTER TABLE 表名 DROP 字段名;
# 重命名列/数据类型
ALTER TABLE 表名 CHANGE 原列名 新列名 数据类型;
# 增加主键
ALTER TABLE 表名 ADD PRIMARY KEY (主键名);
# 删除主键
ALTER TABLE 表名 DROP PRIMARY KEY;
# 添加唯一索引
ALTER TABLE 表名 ADD UNIQUE 索引名 (列名);
# 添加普通索引
ALTER TABLE 表名 ADD INDEX 索引名 (列名);
# 删除索引
ALTER TABLE 表名 DROP INDEX 索引名;
# 把表默认的字符集和所有字符列（CHAR, VARCHAR, TEXT）改为新的字符集
ALTER TABLE 表名 CONVERT TO CHARACTER SET utf8;
# 修改表某一列的编码
ALTER TABLE 表名 CHANGE 列名 varchar(255) CHARACTER SET utf8;
# 仅仅改变一个表的默认字符集
ALTER TABLE 表名 DEFAULT CHARACTER SET utf8;
5. 实例
下面通过一个实例来帮助读者快速上手。
# 建新数据库
CREATE DATABASE test

# 新建一个表person，字段有(自增id、名字、年龄、性别)
CREATE TABLE person(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(30) NOT NULL DEFAULT '',
  age INT,
  sex CHAR(2)
);

# 在表中插入5条数据
INSERT INTO person (name, age, sex) VALUES ('小明', 8, '男');
INSERT INTO person (name, age, sex) VALUES ('小红', 14, '女');
INSERT INTO person (name, age, sex) VALUES ('小白', 4, '男');
INSERT INTO person (name, age, sex) VALUES ('小宝', 6, '男');
INSERT INTO person (name, age, sex) VALUES ('小莉', 16, '女');

# 更新表中的数据(不添加WHERE子句筛选，更新的会是整个表的某列)
UPDATE person SET age = 10, sex = '女' WHERE name = '小明'；

# 在表中插入数据，如果已存在则更新数据
INSERT INTO person (id,name, age, sex) VALUES (1,'小明', 20, '男') ON DUPLICATE KEY
UPDATE age = '20'；

# 删除特定记录
DELETE FROM person WHERE age < 10;

# 查询数据
SELECT * FROM person;   # 查询所有数据
SELECT name,age FROM person;    # 查询特定列
SELECT name AS '姓名',age AS '年龄'FROM person; # 为检索出来的列设置别名
SELECT name FROM person WHERE age > 15 AND age <=20;    # 条件查询
SELECT name FROM person WHERE age BETWEEN 15 AND 20;    # 范围查询

# 数据求总和,平均值,最大值,最小值,记录数
SELECT SUM(age),AVG(age), MAX(age),MIN(age), COUNT(age) FROM person;

# 查询的时候排序：升序(ASC)，降序(DESC)
SELECT * FROM person ORDER BY age ASC;
6. 事务
事务就是一系列数据库的操作，要么完全执行，要么完全不执行。举个简单的例子：
银行转账，转账后数据库对你的余额扣钱，别人收到钱，数据库对他的余额加钱，如果转
账失败，则保证两个人的余额不变，而不是你的钱扣了，他余额没变，或者你的钱没扣，
他的钱反而多了。可以通过下述命令开启事务、确认事务或回滚事务。
BEGIN # 开始一个事务
COMMIT  # 确认事务
ROLLBACK # 回滚事务
"""
#5.1.10 Python连接MySQL数据库
"""
Python中可以使用pymysql库来连接MySQL数据库，通过pip命令安装即可： 
pip install pymysql 
MySQL服务默认的端口号是3306，可以输入下述命令查看端口号： 
show global variables like 'port' 
"""
import pymysql
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306)
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    # 获取第一条数据
    data = cursor.fetchone()
    print('数据库版本号：', data)

    db.close()