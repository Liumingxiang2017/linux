# EXCEL (excellent)

常见对象
- 工作簿：工作表的集合
- 工作表：数据的集合
- 字段：数据的列标题
- 记录：一行数据

数据类型
- 数字类型（默认右对齐）
- 字符类型（默认左对齐）

数据导入
- 从网站导入
- 从文本导入
- 从mysql数据库导入

创建数据库,可以用命令行，也可以用Navicat Premium

```
show databases;
create database demo charset=utf8;
use demo;
create table info (id int unsigned primary key auto_increment, name varchar(10) not null);
show tables;
insert into info values (0,'zf'), (0,'gy');
select * from info;
```

服务器：localhost:3306
数据库：demo

1.下载Power BI DeskTop软件并安装。
2.打开安装软件
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191126134644242.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3MzE5MDM1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191126134722594.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3MzE5MDM1,size_16,color_FFFFFF,t_70)
这里会弹出和Excel相同的错误！然后直接点击下面的链接，便会进入到如下界面
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191126135007239.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM3MzE5MDM1,size_16,color_FFFFFF,t_70)
直接点击下载==》》安装
3.安装完毕，重新启动Excel，即可成功！