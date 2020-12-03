数据库：
一定方式储存在一起、能予多个用户共享、具有尽可能小的冗余度、与应用程序彼此独立的数据集合。

作用：存放、管理数据

技术：
- DBMS （Database Management System）
- SQL语言
- 数据访问接口：ODBC ADO.net JDBC

数据库分类：
- 关系型数据库、MG级别
- 非关系型数据库、TP级别


sql是所有数据库查询的语言，sql本身具备结构化的特点，非常容易入手。针对不同数据库mysql、sqlserver、oracle等，sql语法大同小异。

课前准备
- 安装MySQL服务端
- 安装MySQL图形界面客户端navicate

学习目标
- 了解RDBMS系统和相关数据库
- 了解MySQL数据库的特点
- 了解SQL常用类型
- 熟悉编写数据库增删改查的SQL语句

数据行=记录
数据列=字段
数据表=数据行的集合
数据库=数据表的集合


RDBMS 
> Relational Database Management System 关系型数据库管理系统是建立在关系模型基础上的数据库，借助于集合代数等数学概念和方法来处理数据库中的数据。

关系模型：
- 借助于集合代数等数学概念和方法来处理数据库中的数据，由**关系数据结构、关系操作集合、关系完整性约束**三部分组成。
- 简单说，关系型数据库是由**多张能互相联接的二维行列表格**组成的数据库。
- 通过表来表示关系型。

查看数据库排名：https://db-engines.com/en/ranking

关系型数据库的主要产品：
- oracle：在以前的项目中使用，银行、电信等
- mysql：web时代使用最广泛的关系型数据库
- ms sql server：在微软的项目中使用
- sqlite：轻量级数据库，主要应用在移动平台，物联网设备上，临时转储用的数据库

非关系型数据库：
|  分类   | 举例  | 典型应用场景  | 数据模型  |
|  ----  | ----  | ----  | ----  |
| 键值  | Redis，Oracle BDB | 内容缓存，主要用于处理大量数据的高访问负载，也用于一些日志系统。| Key指向Value的键值对，通过常用的hash table实现 |
| 列存储数据库  | Hbase | 分布式文件系统，速度快，上亿数据一秒查询 | 以列簇式存储，将同一列数据存在一起 |
| 文档型数据库 | MongoDB | Web应用功能（与Key-Value类似，Value是结构化的，不同的是数据库能够了解Value的内容） | Key-Value对应的键值对，Value为结构化数据 |
| 图形数据库| Neo4J | 社交网络，推荐系统等。专注于构建关系图谱| 图结构 |

通过客户端给数据库发送sql指令完成数据库、数据表和数据的基本操作。

SQL 
>Structural Query Language, SQL 是结构化查询语言，是一种用来操作RDBMS的数据库语言。

SQL语句主要分为：
- DQL:数据查询语言，select
- DML:数据操作语言，insert，update, delete
- TPL:事务处理语言，begin, transaction, commit, rollback
- DCL:数据控制语言，进行授权与权限回收，grant, revoke
- DDL:数据定义语言，create，drop
- CCL:指针控制语言，declare, cursor

对于web程序员，重点是crud（增删改查），熟练编写DQL、DML，能够编写DDL完成数据库、表操作。其余TPL/ DCL/ CCL了解即可

- SQL语句关键字不区分大小写

学习要求
- 熟练掌握数据增删改查相关的SQL语句编写
- 在Python中操作数据就是通过SQL语句来操作数据
```python
# 创建Connection连接
conn = connect(host='localhost', port=3006, user='root', password='mysql', database='demo')
# 得Cursor对象
cs = conn.cursor()
# 更新
# sql = 'update students set name="liubang" where id=6'
# 删除
# sql = 'delete from students where id=6'
# 执行select语句，并返回受影响的行数：查询一条学生数据
# sql = 'SELECT id,name FROM students WHERE id=7'
count = cs.execute(sql)
# 打印受影响的行数
print(count)
```

数据库连接工具
>数据库服务器：在本机启动RDBMS系统

>数据库客户端：在终端或者图形界面连接RDBMS

一、启动RDBMS服务

windows下启动
1. 点击搜索框，输入：服务
2. 找到MySQL57（MySQL网络服务的进程）启动
mac平台下启动
1. 找到系统偏好设置
2. 点击mysql，单击Start MySQL Server

二、连接RMDBS
- 使用Navicat连接
- 命令行：mysql -uroot -pmysql -hlocalhost -P3306

三、Navicat的基本操作

新建数据库
1. 选中服务器，右键新建数据库; 

    - 数据库名：使用英文
    - 字符集：utf8
    - 排序规则：utf8_general_ci 通用general排序规则

utf8: 是通用字符集，比如商品数据

utf8mb4: 是通用字符集的扩展，能够存储emoji，比如社交网站，如果用utf8，emoji都会变成口。

2. 新建表

字段：
- 名：id
- 类型：int
- 长度：0，系统会自动根据数据计算长度
- 小数点：0
- 虚拟：不用管
- 不是null：勾选
- 键：点击出现小钥匙，标识数据唯一（主键）
- 注释：标识数据唯一性
- 自动递增：勾选上，每一行数据自动编号，且升序，不一定连续。
- 无符号：勾选上，没有负数的可能

添加字段：
- 名：name
- 类型：varchar (指不定长字符串)
- 长度：10，字符串长度不超过10
- 小数点：0
- 不是null：勾选
- 虚拟：不用管
- 键：不勾选，有一个标识唯一性的键就够了
- 注释：可写可不写
- 默认：未知（如果没有存储名字，采用的默认值）
- 字符集：之前设置了utf8，这边就不用设置了

保存表，输入表名。

如果想编辑表，右击表>设计表。

编辑表
- id：不用管，自动编号，只会越来越大。当然也可以手动输入。
- name：输入数据
- 加号：增加字段

## 常用数据类型

数据完整性

- 一个数据库就是一个完整的业务单元，可以包含多张表，数据被存储在表中
- 在表中为了更加准确的存储数据，保证数据的正确有效，可以在创建表的时候，为表添加一些强制性的验证，包括数据字段的类型、约束

1、数据类型

- 可以通过查看帮助文档查看所有支持的类型
- 使用数据类型原则：够用就行
- 常用数据类型
    - 整数：int，bit
    - 小数：decimal
    - 字符串：varchar，char
    - 日期时间：date，time，datetime
    - 枚举类型：enum
- 特别说明的类型如下
    - decimal表示浮点数，如decimal(5,2)表示共存5位数，小数占2位
    - char表示固定长度的字符串，如char(3)，如果填充'ab'时会补一个空格'ab '
    - varchar表示可变长度的字符串，如varchar(3)，填充'ab'时就会存储ab
    - 字符串text表示存储大文本，当字符大于4000时推荐使用
    - 对于图片、音频、视频等文件，不存储在数据库中，而是上传到某个服务器上，然后在表中存储这个文件的保存路径

2、约束
- 主键 primary key: 物理上的存储顺序
- 非空 not null：此字段不允许填写空值
- 唯一 unique：不允许重复
- 默认default：不填写时会使用默认值
- 外键 foreign key：对关系字段进行约束，当关系字段填写值时，会到关联表中查询此值是否存在，如果存在则填写成功，如果不存在则填写失败并抛出异常
- 说明：虽然外键约束可以保证数据的有效性，但在进行数据crud时，会降低数据库的性能，所以不推荐使用。那么数据有效性怎么保证？答：可以在逻辑层控制。


## 基本操作

1. 连接数据：mysql -uroot -p
2. 退出：quit 或 exit
- 每条指令通过;或者\g结束
- 查看版本： seletct version();
- 显示当前时间：select now();
- 修改输入提示符
```sql
prompt python> 
prompt \U-\D> 
```
\U 使用用户，\D完整日期

3. 数据库操作

- 查看创建的数据库：show databases;
- 查看当前使用的数据库：select database(); # NULL指的是空
- 使用数据库：use database_name;
- 创建数据库: create database database_name;
- 指定字符集: create database database_name charset=utf8; # 必须是utf8字符集，如果是社交类网站则是utf8mb4
- 查看数据库的创建语句：show create database database_name; 
- 删除数据：drop database database_name; 如果数据库为默认latin字符集，最快的方法是直接删掉。

4. 数据表的操作
- 查看当前数据库下所有表：show tables；
- 创建表：create table table_name (字段名 字段类型 字段约束); 例：
```sql
create table students (
    id int unsigned primary key auto_increment,
    name varchar(10) not null,
    age tinyint unsigned default 0,
    high decimal(5,2) default 0.00,
    gender enum('男','女','中性','保密') default '保密',
    class_id int unsigned not null
);

# int unsigned 无符号整形
# primary key 主键
# auto_increment 自动增长
# not null 非空
# enum() 枚举
# 字段之间用逗号隔开，最后一个字段不加逗号
```

- 查看表的创建语句：show create table table_name; 
- 查看表结构：desc table_name;
- 修改表结构：alter add/modify/change
    - 添加字段 alter table table_name add 列名 类型/约束；
    - 修改字段，不重命名 alter table table_name modify 列名 类型/约束；
    - 修改字段，重命名 alter table table_name change 原列名 新列名 类型/约束；
    - 删除字段：alter table table_name drop 字段名；
- 删除表：drop table table_name;

5. 数据增删改查curd
- 增加 insert
    - insert [into] table_name values (value1,value2...)




